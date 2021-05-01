#!/usr/bin/python3

import threading
import logging
import requests
import sploiter

from utils import get_config, get_logger

from client import app


def post_flags():

    url = f"{config['server']['host']}:{config['server']['port']}/api/post_flags"
    data = [{'flag': "CCIT{ban4n4_ctf_ciao_ciao_ciao}",
             'sploit': "bomberone", 'team': "ciupalo"}]
    token = config["server"]["exploit"]["token"]
    headers = {"Content-Type": "application/json"}

    if token is not None:
        headers["X-Token"] = token

    request = requests.post(url, json=data, headers=headers)

    print(request.text)


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

    # post_flags()
    exploit = sploiter.Exploit('ciao.py')

    exploit.run_exploit()
