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
def plot_error(d: dict, fig, colour):
    d_x = [d['x0_val'], d['x1_val'], d['x2_val']]
    d_y = [d['y0_val'], d['y1_val'], d['y2_val']]
    d_err = [d['x0_error'], d['x1_error'], d['x2_error']]
    for x, y, y_err in zip(d_x, d_y, d_err):
        plt.errorbar(x, y, yerr=y_err, fmt='none', color='darkgrey' if colour == None else colour, zorder=8, figure=fig,
                     elinewidth=1)

#input dictionary and use dictionary values to create a single polyfit line for 3 dataframes:
def polyfit_xy(d:dict):
    # prepare line of best fit by grouping dilution gas pairs in df2
    local_dataframe = pd.DataFrame({'n_x2_val': d['x2_val'], 'n_y2_val': d['y2_val']}).copy(deep=True)
    local_dataframe['n_x2_val'] = local_dataframe['n_x2_val'].round(2)
    local_dataframe = local_dataframe.groupby('n_x2_val').mean()
    n_x2_val = local_dataframe.index.to_list()
    n_y2_val = local_dataframe['n_y2_val'].to_list()

    # CONCAT
    n_x_val = d.get('x0_val', None) + d.get('x1_val', None) + n_x2_val
    n_y_val = d.get('y0_val', None) + d.get('y1_val', None) + n_y2_val

    # SORT IT 😜
    tuples = list(zip(n_x_val, n_y_val))
    tuples = sorted(tuples, key=lambda tup: tup[0])
    n_x_val = [tup[0] for tup in tuples]
    n_y_val = [tup[1] for tup in tuples]
    # Polyfit trend
    trend = np.polyfit(n_x_val, n_y_val, 32)
    trendpoly = np.poly1d(trend)

def plot_by_heat(gas: str, instance: Workbook, title: str, fig=None, legend=None, colour=None, ):
    if fig is None:
        fig = plt.figure(figsize=(6.5, 6))

    # assign a dictionary to access all x and y values for the plots.
    d = assign_xy('mean_eq', 'error_eq', 'X_' + gas, 'delta_X_' + gas, instance)

    # plot error bars based on dictionary values for all three dataframes
    plot_error(d, fig, colour)
    polyfit_xy(d)

    # add axies names and details
    plt.title(gas + ', ' + title, pad=15, figure=fig)
    plt.xlabel('equivalence ratio', figure=fig)
    plt.ylabel(gas + ' concentration', figure=fig)
    plt.tight_layout()

    # Turn on the minor TICKS, which are required for the minor GRID
    plt.minorticks_on()
    # Customize the major and minor grids
    plt.grid(which='major', linestyle='-', linewidth='0.5', color='darkgrey', zorder=0, figure=fig)
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='silver', zorder=0, figure=fig)

    # plot scatter graph
    if colour is not None:
        plt.plot(n_x_val, trendpoly(n_x_val), linestyle=':', dashes=(6, 5), linewidth='1.3',
                 color='gray' if colour is None else colour, zorder=9, figure=fig)
    plt.scatter(d['x0_val'], d['y0_val'], color='blue' if colour is None else colour, zorder=10, s=20,
                label='no dilution gas' if legend is None else legend, figure=fig)
    # plt.scatter(x1_val, y1_val, color='green' if colour is None else colour, zorder=10, s=20,
    #             label='single dilution gas' if legend is None else "", figure=fig)
    # plt.scatter(x2_val, y2_val, color='orange' if colour is None else colour, zorder=10, s=20,
    #             label='two dilution gases' if legend is None else "", figure=fig)
    plt.legend()
    return fig


def plot_by_eq(gas: str, instance_list: list, equivalence_ratio: str, fig=None, colour=None):
    if fig is None:
        fig = plt.figure(figsize=(6.5, 6))

    df_0, df_1, df_2 = Workbook.concat_all(instance_list)
    # assign x and y values for individual modes
    if df_0 is not None:
        x0_val = Workbook.lists_to_array(df_0, float, 'mean_heat')
        y0_val = Workbook.lists_to_array(df_0, float, 'X_' + gas)
        x0_error = Workbook.lists_to_array(df_0, float, 'error_heat')
        y0_error = Workbook.lists_to_array(df_0, float, 'delta_X_' + gas)
        # plt.errorbar(x0_val, y0_val, yerr=y0_error, fmt='none', color='darkgrey'if colour==None else colour, zorder=8,
        #              figure=fig, elinewidth=1)
    else:
        x0_val = None
        y0_val = None

    if df_1 is not None:
        x1_val = Workbook.lists_to_array(df_1, float, 'heat_eq')
        y1_val = Workbook.lists_to_array(df_1, float, 'X_' + gas)
        x1_error = Workbook.lists_to_array(df_1, float, 'error_heat')
        y1_error = Workbook.lists_to_array(df_1, float, 'delta_X_' + gas)
        # plt.errorbar(x1_val, y1_val, yerr=y1_error, fmt='none', color='darkgrey' if colour==None else colour, zorder=8,
        #              figure=fig, elinewidth=1)
    else:
        x1_val = None
        y1_val = None

    if df_2 is not None:
        x2_val = Workbook.lists_to_array(df_2, float, 'heat_eq')
        y2_val = Workbook.lists_to_array(df_2, float, 'X_' + gas)
        x2_error = Workbook.lists_to_array(df_2, float, 'error_eq')
        y2_error = Workbook.lists_to_array(df_2, float, 'delta_X_' + gas)
        # plt.errorbar(x2_val, y2_val, yerr=y2_error, fmt='none', color='darkgrey' if colour==None else colour, zorder=8,
        #              figure=fig, elinewidth=1)
        # prepare line of best fit by grouping dilution gas pairs in df2
        local_dataframe = pd.DataFrame({'n_x2_val': x2_val, 'n_y2_val': y2_val}).copy(deep=True)
        local_dataframe['n_x2_val'] = local_dataframe['n_x2_val'].round(2)
        local_dataframe = local_dataframe.groupby('n_x2_val').mean()
        n_x2_val = local_dataframe.index.to_list()
        n_y2_val = local_dataframe['n_y2_val'].to_list()
    else:
        n_x2_val = None
        n_y2_val = None
        # CONCAT
    n_x_val = x0_val + x1_val + n_x2_val
    n_y_val = y0_val + y1_val + n_y2_val

    # SORT IT 😜
    tuples = list(zip(n_x_val, n_y_val))
    tuples = sorted(tuples, key=lambda tup: tup[0])
    n_x_val = [tup[0] for tup in tuples]
    n_y_val = [tup[1] for tup in tuples]

    # Polyfit trend
    trend = np.polyfit(n_x_val, n_y_val, 16)
    trendpoly = np.poly1d(trend)

    # add axies names and details
    plt.title(gas + ', ' + equivalence_ratio, pad=15, figure=fig)
    plt.xlabel('NH3 heat ratio', figure=fig)
    plt.ylabel(gas + ' concentration', figure=fig)
    plt.tight_layout()

    # Turn on the minor TICKS, which are required for the minor GRID
    plt.minorticks_on()
    # Customize the major and minor grids
    plt.grid(which='major', linestyle='-', linewidth='0.5', color='darkgrey', zorder=0, figure=fig)
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='silver', zorder=0, figure=fig)

    # plot scatter graph
    plt.plot(n_x_val, trendpoly(n_x_val), linestyle=':', dashes=(6, 5), linewidth='1.3',
             color='gray' if colour is None else colour, zorder=9, figure=fig)
    plt.scatter(x0_val, y0_val, color='blue' if colour is None else colour, zorder=10, s=20, figure=fig)
    plt.scatter(x1_val, y1_val, color='green' if colour is None else colour, zorder=10, s=20, figure=fig)
    plt.scatter(x2_val, y2_val, color='orange' if colour is None else colour, zorder=10, s=20, figure=fig)
    plt.legend()
    return fig

