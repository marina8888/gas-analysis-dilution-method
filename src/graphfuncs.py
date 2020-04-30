import pandas as pd
import matplotlib.pyplot as plt
from classes import Workbook
import numpy as np
plt.style.use('seaborn-notebook')

def plot_all(gas_list:list, instance: Workbook, heat_ratio: str):
    for gas in gas_list:
        fig, ax = plt.subplots()
        # assign x and y values
        x_val = Workbook.lists_to_array(instance.df, float,'mean_eq')
        y_val = Workbook.lists_to_array(instance.df, float,'X_'+gas)
        x_error = Workbook.lists_to_array(instance.df, float, 'error_eq')
        y_error = Workbook.lists_to_array(instance.df, float, 'delta_X_'+gas)

        # sort them so that polyfit gives correct result
        (x_val, y_val) = Workbook.sort_two_lists(x_val, y_val)

        # create line of best fit and error bars
        trend = np.polyfit(x_val, y_val, 4)
        trendpoly = np.poly1d(trend)
        plt.errorbar(x_val,y_val,x_error, y_error)
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
        ax.plot(x_val, trendpoly(x_val), linestyle=':', dashes=(6, 5), linewidth='1.3', color='lightblue', zorder=9)
        ax.scatter(x_val, y_val, zorder=10, s=20, label='Marina experiment data')

        ax.legend()
        plt.show()
        # plt.savefig('../excel/image_plots/'+heat_ratio + gas)

#  def plot_by_mode(x_data, y_data):
# #     pass
#
# def plot_by_mode_uncert(x_data, y_data, uncert_data):
#     pass
#
# def plot_multiple(x_data1, y_data1, x_data2, y_data2, x_data3=0, y_data3=0, x_data4=0, y_data4=0):
#     pass