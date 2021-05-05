import logging
import os
import shutil
import requests
import threading
import json
import re

_folder_lock = threading.Lock()
_stats_lock = threading.Lock()
stats = {}


def get_config():
    with open('config.json', 'r') as config:
        return json.load(config)


def cache_config():
    host = get_config()["server"]["host"]
    port = get_config()["server"]["port"]

    if ping_server()["online"] == True:
        with open('server_config.json', 'w') as config:
            server_config = requests.get(
                f"{host}:{port}/api/get_config").json()
            json.dump(server_config, config)


def get_server_config():
    if 'server_config.json' not in os.listdir():
        cache_config()

    with open('server_config.json', 'r') as config:
        return json.load(config)


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

    os.remove('server_config.json')

    with open('config.json', 'w') as config:
        json.dump(config_dict, config)


def write_log(exploit_name, team_name, stream):
    folder = os.path.join(
        get_config()["logs"]["folder"], exploit_name.strip('.py'))

    with _folder_lock:
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

    with _folder_lock:
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


def store_result(exploit_name, result):
    with _stats_lock:
        if exploit_name not in stats:
            stats[exploit_name] = {}

        if result not in stats[exploit_name]:
            stats[exploit_name][result] = 1
        else:
            stats[exploit_name][result] += 1


def process_stats():
    states = ["fail", "success"]

    with _stats_lock:
        for exploit in stats:
            for state in states:
                stats[exploit][state] = 0 if state not in stats[exploit]else stats[exploit][state]

        # uniform data representation
        for exploit in stats:
            stats[exploit] = dict([(state, stats[exploit].get(state))
                                   for state in states])

    return stats
