import subprocess
import utils
from os.path import join
import threading

FLAG_ERROR = "No flag found"


class Exploit:

    def __init__(self, exploit_name):
        self.name = exploit_name
        self._lock = threading.Lock()
        self.flags = []

    def store_flag(self, team_name, flag):
        entry = (team_name, flag)

        with self._lock:
            if entry not in self.flags:
                self.flags.append(entry)

    def attack_team(self, team_name, ip_address):
        script_path = join(utils.get_config()[
                           "client"]["exploit_path"], self.name)

        stdout = subprocess.check_output(
            ["python3", script_path, ip_address])

        flag = utils.parse_flag(stdout.decode())

        if flag:
            self.store_flag(team_name, flag)
            utils.clear_logs(self.name.strip('.py'))
        else:
            utils.write_log(self.name, team_name, FLAG_ERROR)
            utils.store_result(self.name, "fail")

    def get_flags(self):
        with self._lock:
            data = [(team_name, self.name, flag)
                    for team_name, flag in self.flags]
            self.flags.clear()

        return data

    def run(self):
        teams = utils.get_teams()
        threads = []

        for team_name in teams:
            thread = threading.Thread(
                target=self.attack_team, args=(team_name, teams[team_name]))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
