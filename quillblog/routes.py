from flask import render_template, url_for, redirect, flash
from quillblog import app
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

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

# forms
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful, Please check username and password', 'danger')
            
    return render_template('login.html', title='Login', form=form)

