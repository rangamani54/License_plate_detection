from matplotlib.pyplot import show
from flask import Flask, flash, request, redirect, url_for, render_template
import os
from werkzeug.utils import secure_filename
from plate_detector import plate_detector
from find_contour import segment_characters
from modelorgtest import show_results
from modelorgtest import vehicle_info
app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/after', methods=['POST'])
def after():
    if 'file1' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file1']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and owner details are displayed below')
        location = 'static/uploads/' + filename

        photo_out, plate_ = plate_detector(location)
        char = segment_characters(plate_)
        data = show_results(char)
        print(data)
        veh_info = vehicle_info(data)
        return render_template("after.html", vehInfo=veh_info)

    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)



if __name__ == "__main__":
    app.run(debug=True, port=1234)
