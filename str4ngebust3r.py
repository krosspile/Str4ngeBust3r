#!/usr/bin/python3

import threading
import logging
import requests
import sploiter
import utils
from client import app
import time


def post_flags(data):
    server_host = utils.get_config()['server']['host']
    server_port = utils.get_config()['server']['port']

    url = f"{server_host}:{server_port}/api/post_flags"

    for team_name, exploit_name, flag in data:
        data_json = [{'flag': flag,
                      'sploit': exploit_name, 'team': team_name}]

        headers = {"Content-Type": "application/json"}

        try:
            requests.post(url, json=data_json, headers=headers)
            utils.store_result(exploit_name, "success")
        except:
            utils.store_result(exploit_name, "fail")
            continue


def run_exploits():
    while True:
        if utils.ping_server()["online"] == True:
            exploits = []
            threads = []

            for file_name, status in utils.scan_folder():
                if status == 0:  # not stopped
                    exploits.append(sploiter.Exploit(file_name))

            for exploit in exploits:
                thread = threading.Thread(target=exploit.run)
                thread.start()
                threads.append(thread)
                thread.join()

            for exploit in exploits:
                flags = exploit.get_flags()

                if flags:
                    post_thread = threading.Thread(
                        target=lambda: post_flags(flags))
                    post_thread.start()

            time.sleep(utils.get_config()["timeout"])


def run_flask(host, port):
    app.run(host=host, port=port, threaded=True)


def start_services():
    flask_service = threading.Thread(target=run_flask, args=(
        utils.get_config()["client"]["host"], utils.get_config()["client"]["port"]))
    flask_service.start()
    logging.info("Flask service started")

    runner_daemon = threading.Thread(target=run_exploits, daemon=True)
    runner_daemon.start()
    logging.info("Exploits daemon started")


if __name__ == '__main__':
    config = utils.get_config()
    utils.get_logger()

    # clear old execution logs first!
    utils.clear_logs()
    start_services()
