import os
from flask import Flask, render_template, request, redirect, jsonify
from werkzeug.utils import secure_filename
import utils

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('index.html', exploits=utils.scan_folder(), srv_status=utils.ping_server())


@app.route('/send_exploit', methods=['GET', 'POST'])
def send_exploit():
    if request.method == 'POST':

        file = request.files['exploit']

        if len(file.filename) > 0 and utils.allowed_extension(file.filename):
            file.save(os.path.join(
                utils.get_config()["client"]["exploit_path"], secure_filename(file.filename)))

        return redirect('/')


@app.route('/start/<exploit>')
def start_exploit(exploit):
    filename = secure_filename(exploit)

    stopped_exploit = os.path.join(
        utils.get_config()["client"]["exploit_path"], f"stopped/{filename}")

    os.rename(stopped_exploit, os.path.join(
        utils.get_config()["client"]["exploit_path"], filename))

    return jsonify(result="Ok")


@app.route('/stop/<exploit>')
def stop_exploit(exploit):
    filename = secure_filename(exploit)

    stopped_path = os.path.join(
        utils.get_config()["client"]["exploit_path"], f"stopped/{filename}")

    os.rename(os.path.join(
        utils.get_config()["client"]["exploit_path"], filename), stopped_path)

    return jsonify(result="Ok")


@app.route('/delete/<exploit>/<status>')
def delete_exploit(exploit, status):
    filename = secure_filename(exploit)

    if status == "0":
        os.remove(os.path.join(
            utils.get_config()["client"]["exploit_path"], filename))

    elif status == "1":
        os.remove(os.path.join(
            utils.get_config()["client"]["exploit_path"], f"stopped/{filename}"))

    return jsonify(result="Ok")


@app.route('/log/<exploit>')
def view_log(exploit):
    return jsonify(utils.process_logs(exploit))


@app.route('/status')
def get_status():
    return jsonify(utils.ping_server())


@app.route('/settings', methods=['POST'])
def set_server():
    if request.method == 'POST':
        data = {}

        if request.form['host'] and request.form['port']:
            data["host"] = request.form['host']
            data["port"] = request.form['port']
            
            utils.update_settings(data)
        return redirect('/')


@app.route('/stats')
def get_stats():
    return jsonify(utils.process_stats())
