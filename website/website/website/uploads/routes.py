from flask import Blueprint, render_template, send_from_directory, url_for, current_app
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

# Define Blueprint
uploads_bp = Blueprint('uploads', __name__)

# Define Upload Set
photos = UploadSet('photos', IMAGES)

# Upload Form
class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Only images are allowed'),
            FileRequired('File field should not be empty')
        ]
    )
    submit = SubmitField('Upload')

@uploads_bp.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(current_app.config['UPLOADED_PHOTOS_DEST'], filename)

@uploads_bp.route('/', methods=['GET', 'POST'])
def upload_image():
    form = UploadForm()
    file_url = None  # Initialize file_url

    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for('uploads.get_file', filename=filename)

    return render_template('index.html', form=form, file_url=file_url)
