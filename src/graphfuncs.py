
import matplotlib.pyplot as plt
from classes import Workbook
import numpy as np
plt.style.use('seaborn-notebook')

def plot_all(gas, instance: Workbook, heat_ratio: str):
    # for gas in gas_list:
        fig, ax = plt.subplots()
        # assign x and y values
        x_val = Workbook.lists_to_array(instance.df, float,'mean_eq')
        y_val = Workbook.lists_to_array(instance.df, float,'X_'+gas)
        x_error = Workbook.lists_to_array(instance.df, float, 'error_eq')
        y_error = Workbook.lists_to_array(instance.df, float, 'delta_X_'+gas)
        plt.errorbar(x_val, y_val, yerr=y_error, fmt='none', zorder=9)
        print(x_error)
        print(y_error)
        # sort them so that polyfit gives correct result
        (x_val, y_val) = Workbook.sort_two_lists(x_val, y_val)

        # create line of best fit and error bars
        trend = np.polyfit(x_val, y_val, 9)
        trendpoly = np.poly1d(trend)
        # add axies names and details
        ax.set_title(heat_ratio + ' Heat Ratio', pad=15)
        ax.set_xlabel('equivalence ratio')
        ax.set_ylabel(gas+' concentration')
        plt.tight_layout()

        # Turn on the minor TICKS, which are required for the minor GRID
        ax.minorticks_on()
        # Customize the major and minor grids
        ax.grid(which='major', linestyle='-', linewidth='0.5', color='darkgrey', zorder=0)
        ax.grid(which='minor', linestyle=':', linewidth='0.5', color='silver', zorder=0)

        # plot scatter graph
        ax.plot(x_val, trendpoly(x_val), linestyle=':', dashes=(6, 5), linewidth='1.3', color='lightblue', zorder=8)
        ax.scatter(x_val, y_val,color='darkblue', zorder=10, s=20, label='Marina experiment data')

        ax.legend()
        plt.show()
        # plt.savefig('../excel/image_plots/'+heat_ratio + gas)

def plot_by_mode(gas, instance: Workbook, heat_ratio: str):
    # for gas in gas_list:
    fig, ax = plt.subplots()
    # assign x and y values for individual modes
    x0_val = Workbook.lists_to_array(instance.df_0, float, 'mean_eq')
    y0_val = Workbook.lists_to_array(instance.df_0, float, 'X_' + gas)
    x0_error = Workbook.lists_to_array(instance.df_0, float, 'error_eq')
    y0_error = Workbook.lists_to_array(instance.df_0, float, 'delta_X_' + gas)
    plt.errorbar(x0_val, y0_val, yerr=y0_error, fmt='none', color='blue', zorder=8)

    x1_val = Workbook.lists_to_array(instance.df_1, float, 'mean_eq')
    y1_val = Workbook.lists_to_array(instance.df_1, float, 'X_' + gas)
    x1_error = Workbook.lists_to_array(instance.df_1, float, 'error_eq')
    y1_error = Workbook.lists_to_array(instance.df_1, float, 'delta_X_' + gas)
    plt.errorbar(x1_val, y1_val, yerr=y1_error, fmt='none', color='green', zorder=8)

    x2_val = Workbook.lists_to_array(instance.df_2, float, 'mean_eq')
    y2_val = Workbook.lists_to_array(instance.df_2, float, 'X_' + gas)
    x2_error = Workbook.lists_to_array(instance.df_2, float, 'error_eq')
    y2_error = Workbook.lists_to_array(instance.df_2, float, 'delta_X_' + gas)
    plt.errorbar(x2_val, y2_val, yerr=y2_error, fmt='none', color='orange', zorder=8)

    x_val=x0_val+x1_val+x2_val
    y_val=y0_val+y1_val+y2_val

    # sort them so that polyfit gives correct result
    (x_val, y_val) = Workbook.sort_two_lists(x_val, y_val)

    # create line of best fit and error bars
    trend = np.polyfit(x_val, y_val, 9)
    trendpoly = np.poly1d(trend)
    # add axies names and details
    ax.set_title(heat_ratio + ' Heat Ratio', pad=15)
    ax.set_xlabel('equivalence ratio')
    ax.set_ylabel(gas + ' concentration')
    plt.tight_layout()

    # Turn on the minor TICKS, which are required for the minor GRID
    ax.minorticks_on()
    # Customize the major and minor grids
    ax.grid(which='major', linestyle='-', linewidth='0.5', color='darkgrey', zorder=0)
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='silver', zorder=0)

    # plot scatter graph
    ax.plot(x_val, trendpoly(x_val), linestyle=':', dashes=(6, 5), linewidth='1.3', color='lightblue', zorder=9)
    ax.scatter(x0_val, y0_val,color='blue', zorder=10, s=20, label='no dilution gas')
    ax.scatter(x1_val, y1_val,color='green', zorder=10, s=20, label='single dilution gas')
    ax.scatter(x2_val, y2_val,color='orange', zorder=10, s=20, label='two dilution gases')

    ax.legend()
    plt.show()
    # plt.savefig('../excel/image_plots/'+heat_ratio + gas)

def plot_multiple(gas, instance: Workbook, heat_ratio: str):
    pass