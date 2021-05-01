import os
from flask import Flask, render_template, request, flash, redirect
from utils import allowed_extension, get_config
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('index.html')


@app.route('/send_exploit', methods=['GET', 'POST'])
def send_exploit():
    if request.method == 'POST':

        file = request.files['exploit']

        if len(file.filename) > 0 and allowed_extension(file.filename):
            file.save(os.path.join(
                get_config()["client"]["exploit_path"], secure_filename(file.filename)))

        return redirect('/')
