from pathlib import Path

import matplotlib.pyplot as plt


def plot_graphs(history, string):
    plt.plot(history.history[string])
    plt.plot(history.history[f'val_{string}'])
    plt.xlabel('Epochs')
    plt.ylabel(string)
    plt.legend([string, f'val_{string}'])

    path = Path('model/data/{string}.png')
    if path.is_file():
        path.unlink()
    plt.savefig(str(path))


# from model.model import load_model; load_model(force_retrain=True)
