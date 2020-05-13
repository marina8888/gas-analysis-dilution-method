import pandas as pd
import matplotlib.pyplot as plt
from excel_file.classes import Workbook
import numpy as np

# all functions in this file are a custom set of methods/options to use when creating a new graph plot
plt.style.use('seaborn-notebook')


# the dictionary can be used to access the graph's data (x, y etc. values).
# Below are data sorting functions that mostly take in data in dictionary format and return the data back in dictionary format
# x y values can initally be accessed from passing in a list of three dataframes or an instance.
# correct assign fumction should be selected based on whether user passes in instance or dataframe list:
def assign_xy_from_inst(x_col: str, x_error: str, y_col: str, y_error: str, instance: Workbook, legend_parameter=None):
    # create a dictionary, d of x, y, x error and y error values to assign to values for each of the three dataframes
    df_list = [instance.df_0, instance.df_1, instance.df_2]
    d = {}
    num_list = [0, 1, 2]

    for df_i, num in zip(df_list, num_list):
        d["x{0}".format(num) + '_val'] = Workbook.lists_to_array(df_i, float, x_col)
        d["y{0}".format(num) + '_val'] = Workbook.lists_to_array(df_i, float, y_col)
        d["x{0}".format(num) + '_error'] = Workbook.lists_to_array(df_i, float, x_error)
        d["y{0}".format(num) + '_error'] = Workbook.lists_to_array(df_i, float, y_error)
        if legend_parameter is not None:
            d['legend{0}'.format(num)] = Workbook.lists_to_array(df_i, float, legend_parameter)
    return d


# overwrite for a list of three dataframes instnead of an instance - some dataframes may not  belong to one specific workbook hence have no instance
def assign_xy_from_list(x_col: str, x_error: str, y_col: str, y_error: str, df_list: list, legend_parameter=None):
    if len(df_list) != 3:
        raise ValueError("df_list with length 3 was expected")
    d = {}
    num_list = [0, 1, 2]
    for df_i, num in zip(df_list, num_list):
        d["x{0}".format(num) + '_val'] = Workbook.lists_to_array(df_i, float, x_col)
        d["y{0}".format(num) + '_val'] = Workbook.lists_to_array(df_i, float, y_col)
        d["x{0}".format(num) + '_error'] = Workbook.lists_to_array(df_i, float, x_error)
        d["y{0}".format(num) + '_error'] = Workbook.lists_to_array(df_i, float, y_error)
        if legend_parameter is not None:
            d['legend{0}'.format(num)] = Workbook.lists_to_array(df_i, float, legend_parameter)
    return d


# Below are plotting functions with no return values- they plot directly to a figure input
# input x, y and error values from dictionary and use them to plot a errorbars:
def plot_error(d: dict, figure, colour=None):
    d_x=[]
    d_y=[]
    y_err=[]
    num_list=[0,1,2]
    for num in num_list:
        d_x.extend(d["x" +str(num)+ '_val'])
        d_y.extend((d["y" +str(num)+ '_val']))
        y_err.extend((d["y" +str(num)+ '_error']))


    for x, y, y_err in zip(d_x, d_y, y_err):
        plt.errorbar(x=d_x, y=d_y, yerr=y_err, fmt='none', color='darkgrey' if colour == None else colour, zorder=8,
                     figure=figure, elinewidth=1)


# input dictionary and use dictionary values to create a single polyfit line for 3 dataframes:
def polyfit_xy(d: dict, figure, colour=None):
    # convert dictionary to dataframe columns, round the values and group them then take the mean
    # round,mean used to smooth duplicate x values so that polyfit will take the mean y of every x value
    local_dataframe = pd.DataFrame({'n_x2_val': d['x2_val'], 'n_y2_val': d['y2_val']}).copy(deep=True)
    local_dataframe['n_x2_val'] = local_dataframe['n_x2_val'].round(2)
    local_dataframe = local_dataframe.groupby('n_x2_val').mean()
    n_x2_val = local_dataframe.index.to_list()
    n_y2_val = local_dataframe['n_y2_val'].to_list()
    list_x_val = []
    list_y_val = []
    # concat list
    list_x_val = d.get('x0_val', None) + d.get('x1_val') + n_x2_val
    list_y_val = d.get('y0_val', None) + d.get('y1_val') + n_y2_val

    # sort it in order of x for polyfit 😜
    tuples = list(zip(list_x_val, list_y_val))
    tuples = sorted(tuples, key=lambda tup: tup[0])
    list_x_val = [tup[0] for tup in tuples]
    list_y_val = [tup[1] for tup in tuples]

    # polyfit to assign coefficients from an x,y dataset
    # poly1d to create a polynomial line from coefficient inputs
    if list_x_val and list_y_val is not None:
        trend = np.polyfit(list_x_val, list_y_val, 32)
        trendpoly = np.poly1d(trend)

    # plot polyfit line:
        plt.plot(list_x_val, trendpoly(list_x_val), linestyle=':', dashes=(6, 5), linewidth='1.3',
                 color='gray' if colour is None else colour, zorder=9, figure=figure)


def format_graph(first_part_title, final_part_title, figure, x_label: str, y_label: str):
    # add title, axies names and layout
    plt.title(first_part_title + ' ' + final_part_title, pad=15, figure=figure)
    plt.xlabel(x_label, figure=figure)
    plt.ylabel(y_label, figure=figure)
    plt.tight_layout()

    # Turn on the minor TICKS, which are required for the minor GRID
    plt.minorticks_on()
    # Customize the major and minor grids
    plt.grid(which='major', linestyle='-', linewidth='0.5', color='darkgrey', zorder=0, figure=figure)
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='silver', zorder=0, figure=figure)


def plot_scatter(d: dict, figure, colour_user_in: str = None, legend_user_in = None):
    legend_list=[]
    colour_list=[]
    if legend_user_in is None:
        legend_list = ['no dilution gas', 'single dilution gas', 'two dilution gases']
    else: legend_list = [legend_user_in, "", ""]
    if colour_user_in is None:
        colour_list = ['blue', 'green', 'orange']
    else: colour_list = [colour_user_in, colour_user_in, colour_user_in]
    d_x = [d['x0_val'], d['x1_val'], d['x2_val']]
    d_y = [d['y0_val'], d['y1_val'], d['y2_val']]

    for x, y, std_colour, l in zip(d_x, d_y, colour_list, legend_list):
        plt.scatter(x, y, color=std_colour, zorder=10, s=20, label=l, figure=figure)
        plt.legend()
