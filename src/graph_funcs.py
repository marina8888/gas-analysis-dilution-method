import pandas as pd
import matplotlib.pyplot as plt
from classes import Workbook
import numpy as np
from itertools import groupby
import operator

# all functions in this file are a custom set of methods/options to use when creating a new graph plot
plt.style.use('seaborn-notebook')


# the dictionary can be used to access the graph's data (x, y etc. values).
# Below are data sorting functions that mostly take in data in dictionary format and return the data back in dictionary format
# x y values can initally be accessed from passing in a list of three dataframes or an instance.
# correct assign fumction should be selected based on whether user passes in instance or dataframe list:
def assign_xy_from_inst(x_col: str, x_error: str, y_col: str, y_error: str, instance: Workbook):
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


# overwrite for a list of three dataframes instnead of an instance - some dataframes may not  belong to one specific workbook hence have no instance
def assign_xy_from_list(x_col: str, x_error: str, y_col: str, y_error: str, df_list: list):
    if len(df_list) != 3:
        raise ValueError("df_list with length 3 was expected")
    d = {}
    num_list = [0, 1, 2]

    for df_i, num in zip(df_list, num_list):
        d["x{0}".format(num) + '_val'] = Workbook.lists_to_array(df_i, float, x_col)
        d["y{0}".format(num) + '_val'] = Workbook.lists_to_array(df_i, float, y_col)
        d["x{0}".format(num) + '_error'] = Workbook.lists_to_array(df_i, float, x_error)
        d["y{0}".format(num) + '_error'] = Workbook.lists_to_array(df_i, float, y_error)
    return d


def round_col(d: dict, value_to_round: str):
    for value in d[value_to_round]:
        value=round(value,2)
        d[value_to_round].append(value)
    return d

# append a list of potential rounded legend values as the 'legend' col in dictionary:
def add_legend_to_df(d: dict, legend_parameter: str, df_list: list):
    if len(df_list) != 3:
        raise ValueError("df_list with length 3 was expected")
    num_list = [0, 1, 2]
    for df_i, num in df_list, num_list:
        d['legend{0}'.format(num)] = Workbook.lists_to_array(df_i, float, legend_parameter)

    for num in num_list:
        d=round_col(d, 'legend'+num)
    return d

# sort large dataframe by legend values and split it into individual dictionaries:
# def sort_split(d: dict, legend: str):
#     #create a list to store each set of dictionaries
#     dict_list=[]
#
#     d_sorted = sorted(d, key=legend)
#     print(d['legend'])
#     print(d['x0_val'])
#     split_d={}
#     for key, value in groupby(d_sorted):
#         split_d[key]=value
#     dict_list.append(split_d)
#     return dict_list


# Below are plotting functions with no return values- they plot directly to a figure input
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


def plot_scatter(d: dict, figure, colour_list: list = None, legend_list: list = None):
    if legend_list is None:
        legend_list = ['no dilution gas', 'single dilution gas', 'two dilution gases']
    if colour_list is None:
        colour_list = ['blue', 'green', 'orange']
    d_x = [d['x0_val'], d['x1_val'], d['x2_val']]
    d_y = [d['y0_val'], d['y1_val'], d['y2_val']]

    for x, y, std_colour, l in zip(d_x, d_y, colour_list, legend_list):
        plt.scatter(x, y, color=std_colour, zorder=10, s=20, label=l, figure=figure)
        plt.legend()
