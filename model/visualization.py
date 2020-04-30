import matplotlib.pyplot as plt


def plot_graphs(history, string):
    plt.plot(history.history[string])
    plt.plot(history.history[f'val_{string}'])
    plt.xlabel('Epochs')
    plt.ylabel(string)
    plt.legend([string, f'val_{string}'])
    plt.show()
