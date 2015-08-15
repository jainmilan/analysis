__author__ = 'milan'

import matplotlib
import matplotlib.pyplot as plt

matplotlib.style.use('fivethirtyeight')


def scatter_plot(sers, labels, axs, title):
    X = sers.index.values
    Y = sers.values
    axs.scatter(X, Y, c = labels, s=200, alpha=0.1)

    axs.set_ylabel("Power (KW)", color='blue')
    axs.set_title(title)


def yy_plot(S1, S2, ax1):
    ax2 = ax1.twinx()  # Create another axes that shares the same x-axis as ax.

    S1.plot(kind='line', color='red', ax=ax1, grid=False, legend=False, linewidth=3, marker='o', rot=30)
    S2.plot(kind='line', color='blue', ax=ax2, grid=False, legend=False, linewidth=3, marker='o', rot=30)

    ax1.set_xlabel("Activities")
    ax1.set_title("Activities Wise Distribution")
    ax1.set_ylabel("Avg. Peak \n Power (KW)", color='blue')
    ax2.set_ylabel("Avg. External \n Temperature \n (degC)", color='red')

    #x_lims = ax1.get_xlim()
    #ax1.set_xlim((x_lims[0]-0.5, x_lims[-1]+0.5))

    y1_lims = ax1.get_ylim()
    ax1.set_ylim((y1_lims[0]-50, y1_lims[-1]+50))

    y2_lims = ax2.get_ylim()
    ax2.set_ylim((y2_lims[0]-4, y2_lims[-1]+4))