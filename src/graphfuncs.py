import pandas as pd
import copy
import matplotlib.pyplot as plt
from classes import Workbook
import numpy as np
plt.style.use('seaborn-notebook')


def plot_by_mode(gas, instance: Workbook, heat_ratio: str, fig=None, colour=None,legend=None):
        if fig is None:
                fig = plt.figure(figsize=(6.5, 6))

        # assign x and y values for individual modes
        if instance.df_0 is not None:
                x0_val = Workbook.lists_to_array(instance.df_0, float, 'mean_eq')
                y0_val = Workbook.lists_to_array(instance.df_0, float, 'X_' + gas)
                x0_error = Workbook.lists_to_array(instance.df_0, float, 'error_eq')
                y0_error = Workbook.lists_to_array(instance.df_0, float, 'delta_X_' + gas)
                plt.errorbar(x0_val, y0_val, yerr=y0_error, fmt='none', color='darkgrey' if colour==0 else colour, zorder=8, figure=fig, elinewidth=1)
        else:
                x0_val = None
                y0_val = None

        if instance.df_1 is not None:
                x1_val = Workbook.lists_to_array(instance.df_1, float, 'mean_eq')
                y1_val = Workbook.lists_to_array(instance.df_1, float, 'X_' + gas)
                x1_error = Workbook.lists_to_array(instance.df_1, float, 'error_eq')
                y1_error = Workbook.lists_to_array(instance.df_1, float, 'delta_X_' + gas)
                plt.errorbar(x1_val, y1_val, yerr=y1_error, fmt='none', color='darkgrey' if colour==0 else colour, zorder=8, figure=fig,  elinewidth=1)
        else:
                x1_val = None
                y1_val = None

        if instance.df_2 is not None:
                x2_val = Workbook.lists_to_array(instance.df_2, float, 'mean_eq')
                y2_val = Workbook.lists_to_array(instance.df_2, float, 'X_' + gas)
                x2_error = Workbook.lists_to_array(instance.df_2, float, 'error_eq')
                y2_error = Workbook.lists_to_array(instance.df_2, float, 'delta_X_' + gas)
                plt.errorbar(x2_val, y2_val, yerr=y2_error, fmt='none', color='darkgrey' if colour==0 else colour, zorder=8, figure=fig,  elinewidth=1)
                        #prepare line of best fit by grouping dilution gas pairs in df2
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
        plt.title(gas + ', '+ heat_ratio + ' Heat Ratio', pad=15, figure=fig)
        plt.xlabel('equivalence ratio', figure=fig)
        plt.ylabel(gas + ' concentration', figure=fig)
        plt.tight_layout()

        # Turn on the minor TICKS, which are required for the minor GRID
        plt.minorticks_on()
        # Customize the major and minor grids
        plt.grid(which='major', linestyle='-', linewidth='0.5', color='darkgrey', zorder=0, figure=fig)
        plt.grid(which='minor', linestyle=':', linewidth='0.5', color='silver', zorder=0, figure=fig)

        # plot scatter graph
        if colour==0:
                plt.plot(n_x_val, trendpoly(n_x_val), linestyle=':', dashes=(6, 5), linewidth='1.3', color='gray' if colour is None else colour, zorder=9, figure=fig)
        plt.scatter(x0_val, y0_val,color='blue'if colour is None else colour, zorder=10, s=20, label='no dilution gas'if legend is None else legend, figure=fig)
        plt.scatter(x1_val, y1_val,color='green' if colour is None else colour, zorder=10, s=20, label='single dilution gas'if legend is None else "", figure=fig)
        plt.scatter(x2_val, y2_val,color='orange'if colour is None else colour, zorder=10, s=20, label='two dilution gases' if legend is None else "", figure=fig)
        plt.legend()
        return fig

def create_plot(gas_list, instance: Workbook, heat_ratio: str):
    for gas in gas_list:
        new_fig = plot_by_mode(gas, instance, heat_ratio)
        new_fig.savefig('../excel/image_plots/'+heat_ratio + gas)

def create_plot_multiple(gas_list:list, heat_ratio_list:list, instance_list:list, legend_list:list, colour_list:list):
        new_fig = plt.figure(figsize=(6.5, 6))
        for gas in gas_list:
                if instance_list is not None:
                        for heat_ratio, instance, legend, colour in zip(heat_ratio_list, instance_list, legend_list, colour_list):
                                plot_by_mode(gas, heat_ratio, instance, new_fig, legend, colour )
                plt.savefig('../excel/image_plots/'+'all' + gas)
