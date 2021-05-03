import logging
import os
import shutil
import threading
import json
import re

_lock = threading.RLock()


def get_config():
    with open('config.json') as config:
        return json.load(config)


def get_logger():
    format = "%(asctime)s: %(message)s"
    datefmt = "%H:%M:%S"
    logging.basicConfig(format=format, level=logging.INFO, datefmt=datefmt)


def get_teams():
    with open('teams.json') as teams:
        return json.load(teams)


def allowed_extension(filename):
    return True if filename.split('.')[-1] == 'py' else False


def parse_flag(input):
    regex = get_config()["flag_regex"]
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


def write_log(exploit_name, team_name, stream):
    folder = os.path.join(
        get_config()["logs"]["folder"], "last", exploit_name.strip('.py'))

    with _lock:
        if not os.path.exists(folder):
            os.makedirs(folder)

    with open(f"{folder}/{team_name}.log", 'w') as log:
        log.write(stream)


def process_logs(exploit_name):
    exploit = {}
    folder = os.path.join(
        get_config()["logs"]["folder"], "last", exploit_name.strip('.py'))

    # handle the case when all exploits work
    try:
        logs = [log.strip('.log') for log in os.listdir(folder)]
    except:
        logs = []

    for team in get_teams()["teams"]:
        if team in logs:
            exploit[team] = False
        else:
            exploit[team] = True

    return exploit


def clear_logs():
    folder = get_config()["logs"]["folder"]

    if os.path.exists(folder):
        for subfolder in os.listdir(folder):
            shutil.rmtree(os.path.join(folder, subfolder))


def push_log(round):
    folder = get_config()["logs"]["folder"]
    target = os.path.join(folder, "last")

    if os.path.exists(target):
        os.rename(target, os.path.join(folder, f"round_{round}"))
