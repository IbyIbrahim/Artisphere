import os

class Config:
    SECRET_KEY = 'asdfjkl'
    UPLOADED_PHOTOS_DEST = os.path.join(os.getcwd(), 'uploads')  # Absolute path to 'uploads' folder
