import logging
import os
import shutil
import requests
import threading
import json
import re

_lock = threading.RLock()


def get_config():
    with open('config.json', 'r') as config:
        return json.load(config)


def get_server_config():
    host = get_config()["server"]["host"]
    port = get_config()["server"]["port"]
    return requests.get(f"{host}:{port}/api/get_config").json()


def get_logger():
    format = "%(asctime)s: %(message)s"
    datefmt = "%H:%M:%S"
    logging.basicConfig(format=format, level=logging.INFO, datefmt=datefmt)


def get_teams():
    return get_server_config()["TEAMS"]


def allowed_extension(filename):
    return True if filename.split('.')[-1] == 'py' else False


def parse_flag(input):
    regex = get_server_config()["FLAG_FORMAT"]
    result = re.findall(regex, input)
    return result[0] if result else None


def scan_folder():
    '''
    We use a tuple to distinguish exploit status:
    0: running
    1: stopped
    '''

    folder = get_config()['client']['exploit_path']
    files = []

    for file in os.listdir(folder):
        path = os.path.join(folder, file)

        if os.path.isfile(path):
            files.append((file, 0))

        elif os.path.isdir(path):
            for subfile in os.listdir(path):
                files.append((subfile, 1))

    files.sort(key=lambda file: file[0])

    return files


def update_settings(data):
    config_dict = {}

    with open('config.json', 'r') as config:
        config_dict = json.load(config)
        config_dict["server"]["host"] = data["host"]
        config_dict["server"]["port"] = int(data["port"])

    with open('config.json', 'w') as config:
        json.dump(config_dict, config)


def write_log(exploit_name, team_name, stream):
    folder = os.path.join(
        get_config()["logs"]["folder"], exploit_name.strip('.py'))

    with _lock:
        if not os.path.exists(folder):
            os.makedirs(folder)

    with open(f"{folder}/{team_name}.log", 'w') as log:
        log.write(stream)


def process_logs(exploit_name):
    exploit = {}
    folder = os.path.join(
        get_config()["logs"]["folder"], exploit_name.strip('.py'))

    # handle the case when all exploits work
    try:
        # .strip('.log') is bugged! WTF
        logs = [log[:-4] for log in os.listdir(folder)]
    except:
        logs = []

    for team in get_teams():
        exploit[team] = False if team in logs else True

    return exploit


def clear_logs(subfolder=""):
    folder = os.path.join(get_config()["logs"]["folder"], subfolder)

    with _lock:
        if os.path.exists(folder):
            shutil.rmtree(folder)


def ping_server():
    response = {}

    response["host"] = get_config()['server']['host'].strip("http://")
    response["port"] = get_config()['server']['port']

    try:
        req = requests.head(f"http://{response['host']}:{response['port']}")
        response["online"] = True
    except:
        response["online"] = False

    return response
