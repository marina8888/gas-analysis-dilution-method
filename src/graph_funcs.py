import pandas as pd
import matplotlib.pyplot as plt
from classes import Workbook
import numpy as np

# all functions in this file are a custom set of methods/options to use when creating a new graph plot
plt.style.use('seaborn-notebook')


# the dictionary can be used to access the graph's data (x, y etc. values):
def assign_xy(x_col: str, x_error: str, y_col: str, y_error: str, instance: Workbook):
    # create a dictionary, d of x, y, x error and y error values to assign to values for each of the three dataframes
    df_list = [instance.df_0, instance.df_1, instance.df_2]
    d = {}
    num_list = [0, 1, 2]
    for df_i, num in zip(df_list, num_list):
        d["x{0}".format(num) + '_val'] = Workbook.lists_to_array(df_i, float, x_col)
        d["y{0}".format(num) + '_val'] = Workbook.lists_to_array(df_i, float, y_col)
        d["x{0}".format(num) + '_error'] = Workbook.lists_to_array(df_i, float, x_error)
        d["y{0}".format(num) + '_error'] = Workbook.lists_to_array(df_i, float, y_error)
    return d


# input x, y and error values from dictionary and use them to plot a errorbars:
def plot_error(d: dict, figure, colour=None):
    d_x = [d['x0_val'], d['x1_val'], d['x2_val']]
    d_y = [d['y0_val'], d['y1_val'], d['y2_val']]
    d_err = [d['x0_error'], d['x1_error'], d['x2_error']]
    for x, y, y_err in zip(d_x, d_y, d_err):
        plt.errorbar(x, y, yerr=y_err, fmt='none', color='darkgrey' if colour == None else colour, zorder=8,
                     figure=figure,
                     elinewidth=1)


# input dictionary and use dictionary values to create a single polyfit line for 3 dataframes:
def polyfit_xy(d: dict, figure, colour=None):
    # convert dictionary to dataframe columns, round the values and group them then take the mean
    # round,mean used to smooth duplicate x values so that polyfit will take the mean y of every x value
    local_dataframe = pd.DataFrame({'n_x2_val': d['x2_val'], 'n_y2_val': d['y2_val']}).copy(deep=True)
    local_dataframe['n_x2_val'] = local_dataframe['n_x2_val'].round(2)
    local_dataframe = local_dataframe.groupby('n_x2_val').mean()
    n_x2_val = local_dataframe.index.to_list()
    n_y2_val = local_dataframe['n_y2_val'].to_list()

    # concat list
    n_x_val = d.get('x0_val', None) + d.get('x1_val', None) + n_x2_val
    n_y_val = d.get('y0_val', None) + d.get('y1_val', None) + n_y2_val

    # sort it in order of x for polyfit 😜
    tuples = list(zip(n_x_val, n_y_val))
    tuples = sorted(tuples, key=lambda tup: tup[0])
    n_x_val = [tup[0] for tup in tuples]
    n_y_val = [tup[1] for tup in tuples]

    # polyfit to assign coefficients from an x,y dataset
    # poly1d to create a polynomial line from coefficient inputs
    trend = np.polyfit(n_x_val, n_y_val, 32)
    trendpoly = np.poly1d(trend)

    # plot polyfit line:
    plt.plot(n_x_val, trendpoly(n_x_val), linestyle=':', dashes=(6, 5), linewidth='1.3',
             color='gray' if colour is None else colour, zorder=9, figure=figure)


def format_graph(first_part_title, final_part_title, figure, x_label: str, y_label: str):
    # add title, axies names and layout
    plt.title(first_part_title + ', ' + final_part_title, pad=15, figure=figure)
    plt.xlabel(x_label, figure=figure)
    plt.ylabel(y_label, figure=figure)
    plt.tight_layout()

    # Turn on the minor TICKS, which are required for the minor GRID
    plt.minorticks_on()
    # Customize the major and minor grids
    plt.grid(which='major', linestyle='-', linewidth='0.5', color='darkgrey', zorder=0, figure=figure)
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='silver', zorder=0, figure=figure)

def plot_scatter(d:dict, figure, colour_list: list = None,legend_list: list = None):
    if legend_list is None:
        legend_list=['no dilution gas', 'single dilution gas', 'two dilution gases']
    if colour_list is None:
        colour_list = ['blue', 'green', 'orange']
    d_x = [d['x0_val'], d['x1_val'], d['x2_val']]
    d_y = [d['y0_val'], d['y1_val'], d['y2_val']]

    for x, y, std_colour, l in zip(d_x, d_y, colour_list, legend_list):
        plt.scatter(x, y, color=std_colour, zorder=10, s=20, label=l, figure=figure)
        plt.legend()
