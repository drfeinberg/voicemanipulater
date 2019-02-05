import manipulate
import measure

import os

from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename



UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/upload/'
ALLOWED_EXTENSIONS = set(['wav', 'mp3'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/static/<filename>')
def pitchManipulation(filename):
    fullpath = UPLOAD_FOLDER + '/' + filename
    newsound = manipulate.maniuplatePitch(wav_file = fullpath, gender="female", factor=-0.5, unit="ERB")
    newsound.save("upload/newsound.wav", "WAV")
    #playit = '<audio controls><source src=' + url_for('upload', filename='newsound.wav') + ' type="audio/wav"></audio>\n'
    playit = '<audio controls><source src=newsound.wav type="audio/wav"></audio>\n'
    return playit


@app.route('/upload/<filename>')
def uploaded_file(filename):
    fullpath = UPLOAD_FOLDER + '/' + filename
    (duration, meanF0, stdevF0, hnr, localJitter, localabsoluteJitter, rapJitter, ppq5Jitter, ddpJitter, localShimmer,
     localdbShimmer, apq3Shimmer, aqpq5Shimmer, apq11Shimmer, ddaShimmer) = \
        measure.measurePitch(fullpath, 75, 500, "Hertz")
    (f1_mean, f2_mean, f3_mean, f4_mean) = measure.measureFormants(fullpath)
    stuff = f"File Name: {filename} </br>\n"\
        f"Duration: {duration} </br>\n" \
        f"Mean F0: {meanF0} </br>\n" \
        f"Standard Deviation: {stdevF0} </br>\n" \
        f"Jitter Local: {localJitter} </br>\n" \
        f"Jitter Local Absolute: {localabsoluteJitter} </br>\n"\
        f"Jitter Rap: {rapJitter} </br>\n" \
        f"Jitter PPQ5: {ppq5Jitter} </br>\n" \
        f"Jitter DDP: {ddpJitter} </br>\n" \
        f"Shimmer Local: {localShimmer} </br>\n" \
        f"Shimmer Local dB: {localdbShimmer} </br>\n" \
        f"Shimmer aqp3: {apq3Shimmer} </br>\n" \
        f"Shimmer apq5: {aqpq5Shimmer} </br>\n" \
        f"Shimmer apq11: {apq11Shimmer} </br>\n" \
        f"Shimmer dda: {ddaShimmer} </br>\n" \
        f"F1: {f1_mean} </br>\n" \
        f"F2: {f2_mean} </br>\n" \
        f"F3: {f3_mean} </br>\n" \
        f"F4: {f4_mean} </br>\n"
    logo = '<img src=' + url_for('static', filename='logo.png') + '>'
    play = pitchManipulation(filename)
    website = logo + '</br>' + play + '</br>' + stuff
    return website


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    website = """<!doctype html>
    <title>Upload new File</title>
    <img src='static/logo.png'>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>"""
    return website


