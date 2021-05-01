from subprocess import check_output
from utils import parse_flag, get_teams, get_config
from os.path import join
import threading


class Exploit:

    def __init__(self, exploit_name):
        self.name = exploit_name
        self._lock = threading.RLock()
        self.flags = []

    def store_flag(self, team_name, flag):
        with self._lock:
            entry = (team_name, flag)

            if entry not in self.flags:
                self.flags.append(entry)

    def attack_team(self, team_name, ip_address):
        script_path = join(get_config()["client"]["exploit_path"], self.name)
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

    def run(self):
        teams = get_teams()["teams"]
        threads = []

        for team_name in teams:
            thread = threading.Thread(
                target=self.attack_team, args=(team_name, teams[team_name]))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
