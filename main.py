import git
from git import Repo
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import os
import numpy as np
import datetime

def read_file(path):
    with open(path, 'r') as file:
        return file.read()
    return ''

dir = '../Rapport-TN09'
file = 'main.tex'
due_date = datetime.datetime.strptime('2019-02-11 00:00:00+01:00', '%Y-%m-%d %H:%M:%S%z')


if __name__ == '__main__':
    repo = Repo(dir)
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

    repo.git.checkout('master')

    def get_fit_fn(dates, lengths, dim):
        min_date = min(dates)
        deltas = [ (date - min_date).total_seconds() for date in dates]
        fit = np.polyfit(deltas, lengths, dim)
        print(fit)
        def fit_fn(date):
            x = (date - min_date).total_seconds()
            return  sum([ n * np.power(x, p) for p, n in enumerate(reversed(fit))])
        return fit_fn
    fig, ax = plt.subplots()

    n_last_commit = 10
    dates_for_regression = dates[:n_last_commit]
    lengths_for_regression = lengths[:n_last_commit]
    fit_fn = get_fit_fn(dates_for_regression, lengths_for_regression, 1)
    base = min(dates_for_regression)
    delta_days =  int((due_date - min(dates_for_regression)).total_seconds() / (3600*24))
    date_list = [base + datetime.timedelta(days=x) for x in range(0, delta_days + 3)]
    prediction = [fit_fn(date) for date in date_list]

    ax.plot(
        dates, lengths, '-b',
        date_list, prediction, '--r'
    )

    ax.axhline(y=75000, linestyle='--')
    ax.axhline(y=95000, linestyle='--')
    ax.axvline(x=due_date, color='orange')

    plt.savefig('plot.png')
