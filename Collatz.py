import matplotlib.pyplot as plt
import numpy as np
import math
import cmath
import copy


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


def complex_collatz(z, max_itter=10 ** 3, method='cosine'):
    steps = 0
    while abs(z) < 2 * 10 ** 8 and steps <= max_itter:
        if abs(z.imag) > 4 or z == 1:
            return steps

        if method.lower() in ['cosine', 'co-sine', 'cos']:
            z = (1 / 4) * (1 + 4 * z - (1 + 2 * z) * cmath.cos(math.pi * z))
        elif method.lower() in ['e', 'exp', 'exponential']:
            z = (1 / 4) * (1 + 4 * z - (1 + 2 * z) * cmath.exp(complex(0, 1) * math.pi * z))
        steps += 1
    return 0


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


def complex_collatz_plot(x_min=-3, x_max=3, y_min=-2, y_max=2,
                         steps=500, max_itter=10 ** 3, method='cosine'):
    my_cmap = copy.copy(plt.cm.get_cmap('hsv'))
    my_cmap.set_under('k')
    figure, axes = plt.subplots()
    x_step = (x_max - x_min) / steps
    y_step = (y_max - y_min) / steps
    heatmap = np.empty(shape=(steps + 1, steps + 1))
    fractal = axes.imshow(heatmap, cmap=my_cmap, vmin=0.5, vmax=50,
                          extent=[x_min, x_max, y_min, y_max], origin='lower')
    axes.set_xticks([x_min, (x_min + x_max) / 2, x_max])
    axes.set_yticks([y_min, (y_min + y_max) / 2, y_max])
    axes.set_xlim(x_min, x_max)
    axes.set_ylim(y_min, y_max)
    for y_counter in range(steps + 1):
        row_map = np.empty(steps + 1)
        for x_counter in range(steps + 1):
            result = complex_collatz(
                complex(x_min + x_step * x_counter,
                        y_min + y_step * y_counter),
                max_itter=max_itter, method=method
            )
            row_map[x_counter] = result
        heatmap[y_counter] = row_map
        if y_counter % 10 == 0 or y_counter == steps:
            fractal.set_data(heatmap)
            axes.set_title(
                f"Resolution: {steps + 1} Accuracy: {max_itter}\nPercent: {(steps + 1) * (y_counter + 1) / ((steps + 1) ** 2):.02%}")
            plt.pause(10 ** -10)


collatz_plot((10 ** 6 - 1) // 2, live=True)
# print(complex_collatz(0.547 + .611j))
# complex_collatz_plot(steps=500, x_min=-2, x_max=2, y_max=2, y_min=-2, method='exp')
