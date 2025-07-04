import os
from pymongo import MongoClient, DESCENDING
from bson.objectid import ObjectId

class QuillDB:
    def __init__(self):
        self.client = MongoClient(os.environ.get('MONGODB_URI'))
        self.db = self.client['quill']
        
        self.users = self.db['users']
        self.posts = self.db['posts']
            
    def find_user(self, user_id=None, username=None, email=None, post_author_id=None):
        if user_id:
            user = self.users.find_one({'_id': ObjectId(user_id)})
        if username:
            user = self.users.find_one({'username': username})
        if email:
            user = self.users.find_one({'email': email})
        if post_author_id:
            user = self.users.find_one({'_id': ObjectId(post_author_id)})
        return user
         
    def update_user_image(self, user_id, image_file):
        self.users.update_one({'_id': ObjectId(user_id)}, {'$set': {'image_file': image_file}})
        
    def update_user_info(self, user_id, username, email):
        self.users.update_one({'_id': ObjectId(user_id)}, {'$set': {'username': username, 'email': email}})
    
    def add_user(self, user):
        result = self.users.insert_one(user.jsonify())
        user.id = str(result.inserted_id)
    
    def add_post(self, post):
        result = self.posts.insert_one(post.jsonify())
        post.id = str(result.inserted_id)
    
    def update_post_info(self, post_id, title, content):
        self.posts.update_one({'_id': ObjectId(post_id)}, {'$set': {'title': title, 'content': content}})
       
    def delete_post(self, post_id):
       self.posts.delete_one({'_id': ObjectId(post_id)})

    def get_posts_per_page(self, curr_page, per_page=3, user_id=None):
        if not user_id:
            posts = list(self.posts.find({}).sort('date_posted', DESCENDING).skip((curr_page - 1) * per_page).limit(per_page))
        else:
            posts = list(self.posts.find({'author_id': str(user_id)}).sort('date_posted', DESCENDING).skip((curr_page - 1) * per_page).limit(per_page))
        return posts
    
    def find_user_img_by_post(self, post_id):
        img = self.users.find_one({'posts._id': ObjectId(post_id)}, {'image_file': 1})
        if not img:
            return None
        return img['image_file']
    
    def find_post(self, post_id):
        post = self.posts.find_one({'_id': ObjectId(post_id)})
        return post
        
