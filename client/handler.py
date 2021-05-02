#!/usr/bin/python3

import threading
import logging
import requests
import sploiter
from utils import get_config, get_logger, scan_folder
from client import app
import time


def post_flags(data):
    url = f"{config['server']['host']}:{config['server']['port']}/api/post_flags"

    for team_name, exploit_name, flag in data:
        data = [{'flag': flag,
                'sploit': exploit_name, 'team': team_name}]

        headers = {"Content-Type": "application/json"}

        request = requests.post(url, json=data, headers=headers)


def run_exploits():
    while True:

        exploits = []
        threads = []

        for file_name, status in scan_folder():
            if status == 0:  # not stopped
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
    flask_daemon = threading.Thread(target=run_flask, args=(
        config["client"]["host"], config["client"]["port"]))
    flask_daemon.start()
    logging.info("Flask service started")

    runner_daemon = threading.Thread(target=run_exploits, daemon=True)
    runner_daemon.start()
    logging.info("Exploits daemon started")


if __name__ == '__main__':
    config = get_config()
    get_logger()
    start_services()
