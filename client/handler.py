#!/usr/bin/python3

import threading
import logging
import requests
import sploiter
from os import listdir
from os.path import isfile, join
from utils import get_config, get_logger
from client import app
import time

active_exploits = []


def post_flags(data):
    url = f"{config['server']['host']}:{config['server']['port']}/api/post_flags"

    for team_name, exploit_name, flag in data:
        data = [{'flag': flag,
                'sploit': exploit_name, 'team': team_name}]

        headers = {"Content-Type": "application/json"}

        request = requests.post(url, json=data, headers=headers)


def scan_folder():
    global active_exploits
    folder = get_config()['client']['exploit_path']

    while True:
        active_exploits = [file for file in listdir(
            folder) if isfile(join(folder, file))]
        time.sleep(5)


def run_exploits():

    while True:

        exploits = []
        threads = []

        for file_name in active_exploits:
            exploits.append(sploiter.Exploit(file_name))

        for exploit in exploits:
            thread = threading.Thread(target=exploit.run)
            thread.start()
            threads.append(thread)
            thread.join()

        for exploit in exploits:
            flags = exploit.get_flags()
            post_thread = threading.Thread(target=lambda: post_flags(flags))
            post_thread.start()

        time.sleep(get_config()['client']['post_sleep'])


def run_flask(host, port):
    app.run(host=host, port=port, threaded=True)


def start_services():

    scan_daemon = threading.Thread(target=scan_folder, daemon=True)
    scan_daemon.start()
    logging.info("Scanner daemon started")

    flask_daemon = threading.Thread(target=run_flask, args=(
        config["client"]["host"], config["client"]["port"]))
    flask_daemon.start()
    logging.info("Flask daemon started")

    runner_daemon = threading.Thread(target=run_exploits, daemon=True)
    runner_daemon.start()
    logging.info("Exploits daemon started")


if __name__ == '__main__':

    config = get_config()
    get_logger()
    start_services()
