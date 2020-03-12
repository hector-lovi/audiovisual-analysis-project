from flask import Flask, flash, request, send_from_directory, render_template, json, redirect, url_for, session
from werkzeug.utils import secure_filename


app = Flask(__name__, static_folder='./templates/')


@app.route('/')
def showmain():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug='True')
