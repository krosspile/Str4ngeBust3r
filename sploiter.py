from subprocess import check_output
from utils import get_flag, get_teams, get_config
from concurrent.futures import ThreadPoolExecutor
import threading


class Exploit:

    def __init__(self, exploit_name):
        self.name = exploit_name
        self._lock = threading.RLock()
        self.flags = []

        self.executor = ThreadPoolExecutor(
            max_workers=get_config()["client"]["max_thread"])

    def store_flag():
        with self._lock:
            entry = (team_name, flag)

            if entry not in self.flags:
                flags.append(entry)

    def attack_team(self, team_name, ip_address):

        script_path = f'{get_config()["client"]["exploit_path"]}/{self.name}'
        output = check_output(["python3", script_path, ip_address]).decode()

        flag = get_flag(output)

        if flag is not None:
            store_flag(flag)

    def run_exploit(self):  # run script for every team

        teams = get_teams()["teams"]

        for team_name in teams:
            self.executor.submit(self.attack_team, team_name, teams[team_name])
