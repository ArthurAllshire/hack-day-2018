import requests
from datetime import datetime
import time
import math

class GitHub:
    """
    Class to fetch from GitHub REST api and return list of commits from a
    specific repo.
    """
    API_URL = "https://api.github.com"

    def __init__(self):
        keyfile = open('token.txt', 'r')
        self.token = keyfile.read().strip('\n')
        keyfile.close()
        self.headers = {'Authorization': 'token %s' % self.token}
        print(self.headers)

    def request(self, url):
        r = requests.get(url, headers=self.headers)
        return r.json()

    def get_commits(self, repo_owner, repo_name):
        url = GitHub.API_URL + f"/repos/{repo_owner}/{repo_name}/commits"
        commits_list_raw = self.request(url)

        sec_list = []
        interval_length = 3600.0

        for i in commits_list_raw:
            date_i_string = i["commit"]["author"]["date"].strip("Z")
            date_i_time = datetime.strptime(date_i_string, "%Y-%m-%dT%H:%M:%S")
            sec_i = time.mktime(date_i_time.timetuple())
            sec_list.append(sec_i)

        total_time = max(sec_list) - min(sec_list)
        interval_number = math.ceil(total_time / interval_length)
        start = min(sec_list)
        end = min(sec_list) + interval_number * interval_length



        '''commits_list_date = self.request("date")'''
        # return a list of times denoting the center of the 'bins'
        # of commits / additions / deletions, along with a list of the
        # number in each bin
        # times are in seconds since unix epoch
        '''times = [10e9, 1e9+10]
        data = [150, 140]
        frame_rate = 24 # bins / day
        return times, data, frame_rate '''
