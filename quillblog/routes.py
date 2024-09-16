from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from quillblog import app, db, bcrypt
from quillblog.forms import RegistrationForm, LoginForm
from quillblog.models import User, Post

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
        'author': 'Mary Jones',
        'title': 'Blog Post 3',
        'content': 'Third post content',
        'date_posted': 'December 3, 2023',
    },
    {
        'author': 'Mary Jones',
        'title': 'Blog Post 3',
        'content': 'Third post content',
        'date_posted': 'December 3, 2023',
    },
    {
        'author': 'Mary Jones',
        'title': 'Blog Post 3',
        'content': 'Third post content',
        'date_posted': 'December 3, 2023',
    },
    {
        'author': 'Mary Jones',
        'title': 'Blog Post 3',
        'content': 'Third post content',
        'date_posted': 'December 3, 2023',
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
    if form.validate_on_submit():
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
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful, Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout') 
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required # add a decorator to invoke flask login functionality
def account():
    return render_template('account.html', title='Account')