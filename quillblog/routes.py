import os
import secrets
from PIL import Image
from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from quillblog import app, db, bcrypt
from quillblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from quillblog.models import User


# dummy data
posts = [
    {
        'author': 'John Doe',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'August 25, 2024',
    },
    {
        'author': 'Jane Smith',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 12, 2024',
    },
    {
        'author': 'Mary Jones',
        'title': 'Blog Post 3',
        'content': 'Third post content',
        'date_posted': 'December 3, 2023',
    },
    {
        'author': 'Alex Finch',
        'title': 'Blog Post 4',
        'content': 'Fourth post content',
        'date_posted': 'June 21, 2023',
    },
    {
        'author': 'Miles Mendez',
        'title': 'Blog Post 5',
        'content': 'Fifth post content',
        'date_posted': 'January 13, 2023',
    },
    {
        'author': 'Pooja Kumar',
        'title': 'Blog Post 6',
        'content': 'Sixth post content',
        'date_posted': 'April 12, 2023',
    },
    {
        'author': 'Sydney Walsh',
        'title': 'Blog Post 7',
        'content': 'Seventh post content',
        'date_posted': 'August 5, 2023',
    },  
]

@app.route('/') # can add two routes that lead to the same url
@app.route('/home') 
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

# forms
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: # use flask login to check if the user exists and is authenticated
        return redirect(url_for('home'))
    form = RegistrationForm()
    # if the form submitted by the user is valid
    if form.validate_on_submit(): # checks if request method is POST
        # created a hashed password for security 
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # create an instance of the User
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # add the user to the db and commit the changes
        db.session.add(user)
        db.session.commit()
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
        user = User.query.filter_by(email=form.email.data).first() # 
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

def save_picture(form_image):
    random_hex = secrets.token_hex(8) # 8 bytes (create a random hex to save for the pictures name since there can be pics with duplicate names)
    _, f_ext = os.path.splitext(form_image.filename) # take the filename of the photo and split it into its name and ext (we use the extension)
    new_image_filename = random_hex + f_ext
    image_path = os.path.join(app.root_path, 'static/images', new_image_filename) # root path gives us the directory where the app is which is our quillblog package
    
    output_size = (100, 100) # width/height is set to 100/100 in css 
    img = Image.open(form_image) # create an image using pillow using the file inputted by the user
    img.thumbnail(output_size)
    img.save(image_path)
    return new_image_filename

@app.route('/account', methods=['GET', 'POST'])
@login_required # only lets those who are authenticated to access the account route
def account():
    image_file = url_for('static', filename=f'images/{current_user.image_file}')
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.image.data:
            pic_file = save_picture(form.image.data)
            current_user.image_file = pic_file
        current_user.username = form.username.data # change the username and email depending on form
        current_user.email = form.email.data
        db.session.commit() # add it to sql database
        flash(f'Your Account has been updated!', 'success')
        return redirect(url_for('account')) # makes it so we send a get method to retrive the account page, so it blocks the popup that gets sent from forms
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', image_file=image_file, form=form)