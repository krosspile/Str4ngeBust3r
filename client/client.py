import os
from flask import Flask, render_template, request, flash, redirect, jsonify
from utils import allowed_extension, get_config, scan_folder, process_logs, ping_server
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('index.html', exploits=scan_folder(), srv_status=ping_server())


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

    return jsonify(result="Ok")


@app.route('/stop/<exploit>')
def stop_exploit(exploit):
    filename = secure_filename(exploit)

    stopped_path = os.path.join(
        get_config()["client"]["exploit_path"], f"stopped/{filename}")

    os.rename(os.path.join(
        get_config()["client"]["exploit_path"], filename), stopped_path)

    return jsonify(result="Ok")


@app.route('/delete/<exploit>/<status>')
def delete_exploit(exploit, status):
    filename = secure_filename(exploit)

    if status == "0":
        os.remove(os.path.join(
            get_config()["client"]["exploit_path"], filename))

    elif status == "1":
        os.remove(os.path.join(
            get_config()["client"]["exploit_path"], f"stopped/{filename}"))

    return jsonify(result="Ok")


@app.route('/log/<exploit>')
def view_log(exploit):
    return jsonify(result=process_logs(exploit))


@app.route('/status')
def get_status():
    return jsonify(result=ping_server())
