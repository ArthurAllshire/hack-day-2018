import requests

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

    def get_commits(self, owner, repo):
        url = GitHub.API_URL + f"/repos/{owner}/{repo}/commits"
        commits_list_raw = self.request(url)

        # return a list of times denoting the endpoins of the 'bins'
        # of commits / additions / deletions, along with a list of the
        # number in each bin
        times = [10e9, 10e9 + 150]
        data = [150]
        return times, data
