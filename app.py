import os
from flask import Flask, request, redirect, url_for, render_template, send_file, flash
from werkzeug.utils import secure_filename
from certify import *

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg'}
app = Flask(__name__, static_url_path="/static")


# APP CONFIGURATIONS
app.config['SECRET_KEY'] = 'opencv'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# limit upload size upto 6mb
app.config['MAX_CONTENT_LENGTH'] = 6 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file attached in request')
            return redirect(request.url)
        file0 = request.files['file']
        file1 = request.files['file1']
        if file0.filename == '':
            flash('No file selected')
            return redirect(request.url)
        if file0 and allowed_file(file0.filename):
            filename = secure_filename(file0.filename)
            list_filename = secure_filename(file1.filename)
            file0.save(os.path.join(UPLOAD_FOLDER, filename))
            file1.save(os.path.join(UPLOAD_FOLDER, list_filename))
            if os.path.exists('output.zip'):
                os.remove('output.zip')
            process_file(os.path.join(UPLOAD_FOLDER, filename),os.path.join(UPLOAD_FOLDER, list_filename))
            return send_file('output.zip', as_attachment=True)
    
    return render_template('index.html')


def process_file(path, list_path):
    certificateGen(path, list_path)

if __name__ == '__main__':
    app.run()
