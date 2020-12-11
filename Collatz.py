import matplotlib.pyplot as plt
import numpy as np
import math


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


def _best_collatz_plot_refresh(n, x_max, cutoff=50):
    max_refresh = max(1, x_max // 100)
    if x_max < cutoff:
        return 1
    else:
        # todo: this is NOT smooth. Find a better function that increases slowly enough (but quickly enough)
        percent_done = max((n - cutoff) / (x_max - cutoff), 0)
        # r = math.log(max(x_max // 1000, 1))
        # return int(math.exp(percent_done * r))
        best_refresh = round(1 * ((1 - percent_done) ** (1 / 2)) + max_refresh * (percent_done ** (1 / 2)))
        # print(f"{percent_done:.02%} --> {best_refresh}")
        return best_refresh


def collatz_plot(maximum, live=True, refresh=0):
    # plt.ion()

    fig, ax = plt.subplots()

    if live:
        x_list, y_list = np.empty(0, dtype='int64'), np.empty(0, dtype='int64')
        sc = ax.scatter(x_list, y_list, s=2)
        plt.draw()
        for n in range(1, maximum + 1):
            x_list = np.append(x_list, n)
            y_list = np.append(y_list, collatz(n))
            best_refresh = _best_collatz_plot_refresh(n, maximum) if refresh <= 0 else refresh
            if n % best_refresh == 0 or n == maximum:
                last_refresh = n
                # set the new data with set_offsets. np.c_ puts it in the correct "data table" form
                # sc.set_offsets(np.c_[x_list, y_list])
                sc.set_offsets(np.transpose(np.vstack([x_list, y_list])))
                ax.set_xlim((0, n))
                ax.set_ylim((0, 1.05 * max(np.max(y_list), 1) if y_list.size > 0 else 10))
                fig.suptitle(f'Collatz Conjecture up to {n:,}')
                print(f'Collatz Conjecture up to {n:,}')
                ax.set_title(f'{n / maximum:.02%}, refresh={best_refresh:,}', loc='right')
                # fig.canvas.draw_idle()
                plt.pause(10 ** -100)
    else:
        x_list = np.array(range(1, maximum))
        # todo: can we make this efficient?
        y_list = np.array([collatz(xi) for xi in x_list])
        sc = ax.scatter(x_list, y_list, s=2)
        # sc.set_offsets(np.c_[x_list, y_list])
        sc.set_offsets(np.transpose(np.vstack([x_list, y_list])))
        ax.set_xlim((0, maximum))
        ax.set_ylim((0, 1.05 * np.max(y_list) if y_list.size > 0 else 10))
        fig.canvas.draw_idle()
        plt.pause(10 ** -9)

    input("Press Enter to quit")


collatz_plot(10 ** 6 - 1, live=True)
