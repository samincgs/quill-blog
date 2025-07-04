import pymongo
import math
from flask import render_template, url_for, redirect, flash, request, abort
from flask_login import login_user, logout_user, current_user, login_required

from init import app, db, bcrypt
from forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from models import User, Post, user_class, post_class
from operations import save_picture, clean_img_folder

from bson.objectid import ObjectId

PER_PAGE = 3

# cant have same function name from multiple posts
@app.route('/') # can add two routes that lead to the same url
@app.route('/home') 
def home():
    page = request.args.get(key='page', default=1, type=int)
    
    
    total_posts = db.posts.count_documents({})
    total_pages = math.ceil(total_posts / PER_PAGE)
    
    posts = db.get_posts_per_page(page, per_page=PER_PAGE)
    
    for post in posts: # add author id
        author_id = ObjectId(post['author_id'])
        post['id'] = str(post['_id'])
        user = db.users.find_one({'_id': author_id}, {'username': 1, 'image_file': 1})
        post['author_username'] = user['username']
        post['author_image_file'] = user['image_file']
    
    return render_template('home.html', posts=posts, total_posts=total_posts, total_pages=total_pages, page=page)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

# forms
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: # extraa check to make sure a user cannot register again if they are already logged in
        return redirect(url_for('home'))
    form = RegistrationForm()
    # if the form submitted by the user is valid
    if form.validate_on_submit(): # checks if request method is POST
        # created a hashed password for security 
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # create an instance of the User
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # add the user to the db and commit the changes
        db.add_user(user)
        # create a flash message so that user knows that they have been properly signed in
        flash(f'Account created for {form.username.data}, You are now able to log in!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: # use flask login to check if the user is authenticated
        return redirect(url_for('home')) # if user is authenticated send them to the home page
    form = LoginForm() # if they are not ask them to login 
    if form.validate_on_submit(): # if valid form data was submitted
        user = db.find_user(email=form.email.data)
        user = user_class(user) # convert back into class for it to have session properties
        # user = User.query.filter_by(email=form.email.data).first() # 
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data) # logs in the user using flask login and start their session, this stores their userid in the session which flask login uses to keep user loggin in accross different requests
            next_page = request.args.get('next') # if the query parameter of next exists (requests.args is a dictionary with the queries, so we use .get() to ensure out python program doesnt crash instead it returns a None)
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful, Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout') 
def logout():
    logout_user() # flask login logs out the user by clearing the session data
    return redirect(url_for('home'))

@app.route('/account', methods=['GET', 'POST'])
@login_required # only lets those who are authenticated to access the account route
def account():
    image_file = url_for('static', filename=f'images/{current_user.image_file}')
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.image.data:
            pic_file = save_picture(form.image.data)
            current_user.image_file = pic_file
            db.update_user_image(current_user.id, pic_file)
        db.update_user_info(current_user.id, username=form.username.data, email=form.email.data)
        clean_img_folder()
        flash(f'Your Account has been updated!', 'success')
        return redirect(url_for('account')) # makes it so we send a get method to retrive the account page, so it blocks the popup that gets sent from forms
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    return render_template('account.html', title='Account', image_file=image_file, form=form)

# new post route
@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author_id=current_user.id)
        db.add_post(post)
        # db.session.add(post)
        # db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, form_title='Create Post')

@app.route('/post/<post_id>') # get an integer number from the query
def post(post_id):
    post = db.find_post(post_id) # get the post if there is one else throw a 404 error meaning resource could not be found
    if not post:
        abort(404)
    
    user = db.find_user(post_author_id=post['author_id'])   
    post['id'] = str(post['_id']) 
    
        
    return render_template('post.html', title=post['title'], post=post, user=user)

@app.route('/post/<post_id>/update', methods=['GET', 'POST']) # get an integer number from the query
@login_required
def update_post(post_id):
    post = db.find_post(post_id)
    if not post:
        abort(404)
    if post['author_id'] != current_user.id:
        abort(403) # 403 is the http response for a forbidden route/unauthorized
    form = PostForm()
    if form.validate_on_submit():
        db.update_post_info(post['_id'], title=form.title.data, content=form.content.data)
        # db.session.commit()
        flash('Your Post has been updated!', 'success')
        return redirect(url_for('post', post_id=str(post['_id'])))
    elif request.method == 'GET':
        form.submit.label.text = 'Update'
        form.title.data = post['title']
        form.content.data = post['content']
    
    return render_template('create_post.html', title='Update Post', form=form, form_title='Update Post')

@app.route('/post/<post_id>/delete', methods=['GET', 'POST']) # get an integer number from the query
@login_required
def delete_post(post_id):
    post = post = db.find_post(post_id) # get the post if there is one else throw a 404 error meaning resource could not be found
    if not post:
        abort(404)
    if post['author_id'] != current_user.id:
        abort(403) # 403 is the http response for a forbidden route/unauthorized
    db.delete_post(post['_id'])
    # db.session.delete(post)
    # db.session.commit()
    flash('Your Post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route('/user/<string:username>') 
def user_posts(username):
    page = request.args.get('page', default=1, type=int)
    
    user = db.find_user(username=username) # get the first user with this username and return a 404 Not Found if it doesnt exist
    if not user:
        abort(404)
        
    total_posts = len(list(db.posts.find({'author_id': str(user['_id'])})))
    total_pages = math.ceil(total_posts / PER_PAGE)
    
    posts = db.get_posts_per_page(page, per_page=PER_PAGE, user_id=user['_id'])
    for post in posts:
        post['id'] = str(post['_id'])
    
    return render_template('user_post.html', user=user, posts=posts, total_posts=total_posts, total_pages=total_pages, page=page)