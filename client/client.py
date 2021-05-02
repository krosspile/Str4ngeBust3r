import os
from flask import Flask, render_template, request, flash, redirect
from utils import allowed_extension, get_config, scan_folder
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    all_exploits = scan_folder()
    print(all_exploits)
    return render_template('index.html', exploits=scan_folder())


@app.route('/send_exploit', methods=['GET', 'POST'])
def send_exploit():
    if request.method == 'POST':

        file = request.files['exploit']

        if len(file.filename) > 0 and allowed_extension(file.filename):
            file.save(os.path.join(
                get_config()["client"]["exploit_path"], secure_filename(file.filename)))

        return redirect('/')


@app.route('/start/<exploit>')
def start_exploit(exploit):
    filename = secure_filename(exploit)

    stopped_exploit = os.path.join(
        get_config()["client"]["exploit_path"], f"stopped/{filename}")

    os.rename(stopped_exploit, os.path.join(
        get_config()["client"]["exploit_path"], filename))

    return redirect('/')


@app.route('/stop/<exploit>')
def stop_exploit(exploit):
    filename = secure_filename(exploit)

    stopped_path = os.path.join(
        get_config()["client"]["exploit_path"], f"stopped/{filename}")

    os.rename(os.path.join(
        get_config()["client"]["exploit_path"], filename), stopped_path)

    return redirect('/')


@app.route('/delete/<exploit>')
def delete_exploit(exploit):
    filename = secure_filename(exploit)
    os.remove(os.path.join(get_config()["client"]["exploit_path"], filename))

    return redirect('/')
