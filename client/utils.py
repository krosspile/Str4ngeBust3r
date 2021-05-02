import logging
import threading
from os import listdir
from os.path import isfile, join, isdir
import time
import json
import re


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

    for file in listdir(folder):
        path = join(folder, file)

        if isfile(path):
            files.append((file, 0))

        elif isdir(path):
            for subfile in listdir(path):
                files.append((subfile, 1))

    files.sort(key= lambda file: file[0])
    
    return files
