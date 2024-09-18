from quillblog import db, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader # reloading the user using the userId from the session (needed for flask login to function and authenticate the user)
def load_user(user_id): # we return the user based on the id
    return User.query.get(int(user_id)) # query the user using their primary ID (sqlalchemy uses .get() for ids)

class User(db.Model, UserMixin): # UserMixin is a class inherited from flaskLogin that gives us the 4 necessary methods to use flask login (is_authenticated, is_active, is_anonymous, get_id)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post',  backref='author', lazy=True) # one user can have multiple posts and backref means that the post model can access the user by using post.author
    
    def __repr__(self):
        return f'User("{self.username}, {self.email}, {self.image_file}")'
    
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'User("{self.title}, {self.date_posted}")'