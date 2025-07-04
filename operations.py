import secrets
import os
from PIL import Image
from init import app, db

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

def clean_img_folder():
    user_imgs = set([user['image_file'] for user in db.users.find({})])
    
    for img_name in os.listdir('static/images/'):
        if img_name not in user_imgs:
            os.remove(os.path.join('static', 'images', img_name))
            
