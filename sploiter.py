from subprocess import check_output
from utils import parse_flag, get_teams, get_config
from concurrent.futures import ThreadPoolExecutor
import threading


class Exploit:

    def __init__(self, exploit_name):
        self.name = exploit_name
        self._lock = threading.RLock()
        self.flags = []

        self.executor = ThreadPoolExecutor(
            max_workers=get_config()["client"]["max_thread"])

    def store_flag(self, team_name, flag):
        with self._lock:
            entry = (team_name, flag)

            if entry not in self.flags:
                self.flags.append(entry)

            

    def attack_team(self, team_name, ip_address):

        script_path = f'{get_config()["client"]["exploit_path"]}/{self.name}'
        output = check_output(["python3", script_path, ip_address]).decode()

        flag = parse_flag(output)

        if flag is not None:
            self.store_flag(team_name, flag)

    def get_flags(self):

        with self._lock:
            data = [(team_name, self.name, flag)
                    for team_name, flag in self.flags]

            self.flags.clear()

        return data

    def run_exploit(self):  # run script for every team

        teams = get_teams()["teams"]

        for team_name in teams:
            self.executor.submit(self.attack_team, team_name, teams[team_name])

