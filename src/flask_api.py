import os
from flask import Flask, flash, request, redirect
from flask import render_template
import video_analyze as v
import extract_text as e
import text_analyze as t
import extract_time as ti
from werkzeug.utils import secure_filename


app = Flask(__name__, static_folder='./templates/')

# instancia del objeto Flask
app.config['UPLOAD_FOLDER'] = 'input/test'


@app.route('/')
def showmain():
    return render_template('index.html')


@app.route('/analysis', methods=['POST'])
def spot_analysis():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)

        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        video = v.videoAnalyze(os.path.join(
            app.config['UPLOAD_FOLDER'], filename))
        time = ti.extractTime(os.path.join(
            app.config['UPLOAD_FOLDER'], filename))
        text1 = e.extractAudio(os.path.join(
            app.config['UPLOAD_FOLDER'], filename))
        text2 = t.textAnalyze(text1)

        return render_template('analysis.html', video=video, time=time, text1=text1, text2=text2)


if __name__ == "__main__":
    app.run("0.0.0.0", 5000)
