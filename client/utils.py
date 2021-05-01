import logging
import threading
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
