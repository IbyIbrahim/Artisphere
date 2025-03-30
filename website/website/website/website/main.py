from flask import Flask, render_template, send_from_directory, url_for, redirect
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
import os
import random
import nltk
import time
from nltk.corpus import words

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdfjkl'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'

if not os.path.exists(app.config['UPLOADED_PHOTOS_DEST']):
    os.makedirs(app.config['UPLOADED_PHOTOS_DEST'])

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Only images are allowed'),
            FileRequired('File field should not be empty')
        ]
    )
    submit = SubmitField('Upload')

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)

# Ensure the NLTK words corpus is downloaded
nltk.download('words')
english_words = words.words()

# Global variables for storing the random word and timestamp
random_word = random.choice(english_words)
last_update_time = time.time()

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    global random_word, last_update_time  # Allow modifying global variables

    # Check if 24 hours (86400 seconds) have passed
    if time.time() - last_update_time >= 86400:
        random_word = random.choice(english_words)  # Pick a new random word
        last_update_time = time.time()  # Update timestamp

    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for('get_file', filename=filename)
    else:
        file_url = None

    return render_template("index.html", form=form, file_url=file_url, word=random_word)

@app.route('/gallery')
def gallery():
    image_files = []
    for filename in os.listdir(app.config['UPLOADED_PHOTOS_DEST']):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            image = {
                'url': url_for('get_file', filename=filename),
                'title': filename,
                'description': 'Uploaded image'
            }
            image_files.append(image)
    return render_template('gallery.html', images=image_files)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)