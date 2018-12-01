import numpy as np

from github import GitHub

class Data:

    DEFAULT_REPO = {'owner':'tensorflow', 'repo': 'tensorflow'}

    def __init__(self):
        self.gh = GitHub()

    def get_frequency(self, repo_owner, repo_name):
        times, commits, frame_rate = self.gh.get_commits(repo_owner)

        freq = np.fft.fftfreq(len(commits)) * frame_rate

        power_f_domain = np.fft.fft(commits)
        power = f_domain.real

        abs_data = {}
        # make all amplitutudes and frequencies positive
        for i in range(len(freq_raw)):
            abs_freq = abs(freq_raw[i])
            if not abs_freq in abs_data:
                abs_data[abs_freq] = abs(power[i])
            else:
                abs_data[abs_freq] += abs(power[i])
        # construct final frequency amplitude lists
        frequencies, amplitudes = [], []
        for freq in abs_data.keys():
            frequencies.append(freq)
            amplitudes.append(abs_data[freq])

        return frequencies, amplitudes
