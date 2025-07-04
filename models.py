from datetime import datetime
from flask_login import UserMixin

from init import db, login_manager

@login_manager.user_loader # reloading the user using the userId from the session (needed for flask login to function and authenticate the user)
def load_user(user_id): # we return the user based on the id
    user = db.find_user(user_id=user_id)
    user = user_class(user)
    return user

def user_class(user):
    if not user:
        return None
    user = User(user['username'], user['email'], user['password'], id=str(user['_id']), image_file=user['image_file'])
    return user

def post_class(post):
    if not post:
        return None
    post = Post(post['title'], post['content'], post['author_id'], post['date_posted'])
    return post


class User(UserMixin):
    def __init__(self, username, email, password, id=None, image_file='default.jpg'):
        super().__init__()
        
        self.id = id
        self.username= username
        self.email = email
        self.password = password
        self.image_file = image_file
        self.posts = []
    
    def jsonify(self):
        data = {'username': self.username,
                'email': self.email,
                'password': self.password,
                'image_file': self.image_file
                }
        return data
    
    def __repr__(self):
        return f'User("{self.username}, {self.email}, {self.image_file}")'
    
class Post:
    def __init__(self, title, content, author_id, date_posted=datetime.now()):
        self.id = -1
        self.title = title
        self.content = content
        self.author_id = author_id
        self.date_posted = date_posted
        
    def jsonify(self):
        data = {'title': self.title,
                'content': self.content,
                'author_id': str(self.author_id),
                'date_posted': self.date_posted
                }
        return data
    
    def __repr__(self):
        return f'Post("{self.title}, {self.date_posted}")'
    
    
# class User(db.Model, UserMixin): # UserMixin is a class inherited from flaskLogin that gives us the 4 necessary methods to use flask login (is_authenticated, is_active, is_anonymous, get_id)
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
#     password = db.Column(db.String(60), nullable=False)
#     posts = db.relationship('Post',  backref='author', lazy=True) # one user can have multiple posts and backref means that the post model can access the user by using post.author
     
#     def __repr__(self):
#         return f'User("{self.username}, {self.email}, {self.image_file}")'

# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     # relationship with User 
#     # author = db.Column()
    
#     def __repr__(self):
#         return f'User("{self.title}, {self.date_posted}")'