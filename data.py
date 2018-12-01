import numpy as np

from github import GitHub

class Data:

    DEFAULT_REPO = {'owner':'tensorflow',}

    def __init__(self):
        self.gh = GitHub()

    def get_frequency(self, repo_owner, repo_name):
        times, commits, frame_rate = self.gh.get_commits(repo_owner)

        frequencies, amplitudes = [], []
        return frequencies, amplitudes
