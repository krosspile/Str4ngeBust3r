#!/usr/bin/python3

import threading
import logging
import requests
import sploiter
from utils import get_config, get_logger
from client import app


def post_flags(data):

    url = f"{config['server']['host']}:{config['server']['port']}/api/post_flags"

    for team_name, expoloit_name, flag in data:

        data = [{'flag': flag,
                'sploit': expoloit_name, 'team': team_name}]

        headers = {"Content-Type": "application/json"}

        request = requests.post(url, json=data, headers=headers)

    

def run_flask(host, port):
    app.run(host=host, port=port, threaded=True)


if __name__ == '__main__':

    config = get_config()

    get_logger()
    logging.info("Loaded configs")

    flask_thread = threading.Thread(target=run_flask, args=(
        config["client"]["host"], config["client"]["port"]))

    flask_thread.start()

    logging.info("Flask started")

    exploit = sploiter.Exploit('ciao.py')

    exploit.run_exploit()

    while True:
        post_flags(exploit.get_flags())
