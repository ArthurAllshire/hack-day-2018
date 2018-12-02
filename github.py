import requests
from datetime import datetime
import time
import math
import numpy as np
from urllib.parse import urlparse, parse_qs

class GitHub:
    """
    Class to fetch from GitHub REST api and return list of commits from a
    specific repo.
    """
    API_URL = "https://api.github.com"
    HOUR = 3600 # sec
    INTERVAL_LENGTH = HOUR * 6
    API_TIME_STR = "%Y-%m-%dT%H:%M:%S"
    MAX_PAGES = 1000

    def __init__(self):
        keyfile = open('token.txt', 'r')
        self.token = keyfile.read().strip('\n')
        keyfile.close()
        self.headers = {'Authorization': 'token %s' % self.token}
        # print(self.headers)

    def request(self, url):
        page = 1
        last = 1
        page_head = "?page="
        add_head = "&per_page=100"
        response = []
        while not page > last and page <= self.MAX_PAGES:
            r = requests.get(url+page_head+str(page)+add_head,
                             headers=self.headers)
            try:
                last_link = r.links['last']['url']
            except KeyError:
                response += r.json()
                break
            # print(last_link)
            # massive hack
            last = int(last_link.split('=')[1].split('&')[0])
            print(f'Last {last} Page {page}')
            page += 1
            response += r.json()
        return response

    def get_commits(self, repo_owner, repo_name):
        url = GitHub.API_URL + f"/repos/{repo_owner}/{repo_name}/commits"
        commits_list_raw = self.request(url)

        sec_list = []

        for i in commits_list_raw:
            date_i_string = i["commit"]["author"]["date"].strip("Z")
            date_i_time = datetime.strptime(date_i_string, self.API_TIME_STR)
            sec_i = time.mktime(date_i_time.timetuple())
            sec_list.append(sec_i)

        total_time = max(sec_list) - min(sec_list)
        interval_number = math.ceil(total_time / self.INTERVAL_LENGTH)
        start = min(sec_list)
        end = min(sec_list) + interval_number * self.INTERVAL_LENGTH
        # print(f"Time Delta {end-start}")

        bins = np.linspace(start, end, interval_number+1)
        bin_means = [(bins[i-1] + bins[i])/2
                     for i in range(len(bins[1:]))]
        digitised = np.digitize(sec_list, bins)

        commit_counts = np.zeros(shape=(len(bin_means)))

        for bn in digitised:
            commit_counts[bn-1] = commit_counts[bn-1] + 1
        # time, commit_count, rate
        # rate is returned in bins/hour, as the eventual frequency will be
        # per hour
        return bin_means, commit_counts, self.INTERVAL_LENGTH/self.HOUR
