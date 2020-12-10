import matplotlib.pyplot as plt
import numpy as np


def collatz(n, verbose=False):
    steps = 0
    while n > 1:
        print(f"{n} --> " if verbose else "", end='')
        if n % 2 == 0:
            n = int(n / 2)
        else:
            n = int(3 * n + 1)
        steps += 1
    print(n if verbose else "", end='\n' if verbose else '')
    return steps


def collatz_plot(maximum, live=True):
    plt.ion()

    fig, ax = plt.subplots()

    if live:
        x_list, y_list = np.empty(0, dtype='int64'), np.empty(0, dtype='int64')
        sc = ax.scatter(x_list, y_list, s=2)
        plt.xlim(0, 10)
        plt.ylim(0, 10)
        plt.draw()
        for MAX in range(2, maximum):
            # x_list.append(MAX)
            # y_list.append(collatz(MAX))
            x_list = np.append(x_list, MAX)
            y_list = np.append(y_list, collatz(MAX))
            if MAX < 200 or (MAX > 200 and MAX % 5000 == 0):
                sc.set_offsets(np.c_[x_list, y_list])
                ax.set_xlim((0, MAX))
                ax.set_ylim((0, 1.05 * np.max(y_list) if y_list.size > 0 else 10))
                fig.canvas.draw_idle()
                plt.pause(10 ** -9)
    else:
        x_list = np.array(range(2, maximum))
        # todo: can we make this efficient?
        y_list = np.array([collatz(xi) for xi in x_list])
        sc = ax.scatter(x_list, y_list, s=2)
        sc.set_offsets(np.c_[x_list, y_list])
        ax.set_xlim((0, maximum))
        ax.set_ylim((0, 1.05 * np.max(y_list) if y_list.size > 0 else 10))
        fig.canvas.draw_idle()
        plt.pause(10 ** -9)

    input("Press Enter to quit")


# input("Press enter to quit")
# MAX = 10 ** 6
# fig, ax = plt.subplots()
# sc = ax.scatter(range(2, MAX), [collatz(i) for i in range(2, MAX)], s=2)
# # sc = ax.scatter(np.array(range(2, MAX)), )
# plt.show()
# input("Press enter to quit")
collatz_plot(10000, live=False)
