import git
from git import Repo
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import os
import datetime

def read_file(path):
    with open(path, 'r') as file:
        return file.read()
    return ''

dir = './Rapport-TN09'
file = 'main.tex'

if __name__ == '__main__':
    repo = Repo('./Rapport-TN09')
    repo.git.checkout('master')
    commits = list(repo.iter_commits())
    file_path = os.path.join(dir, file)
    dates = []
    lengths = []
    for commit in commits:
        date = commit.committed_datetime
        if date < datetime.datetime.strptime('2018-11-13 09:42:17+01:00', '%Y-%m-%d %H:%M:%S%z'):
            continue
        dates.append(date)
        print(f'Checkout commit {commit}')
        repo.git.checkout(f'{commit}')
        length = len(read_file(file_path))
        lengths.append(length)

    fig, ax = plt.subplots()
    ax.plot(dates, lengths)
    plt.savefig('plot.png')
