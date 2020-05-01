import pandas as pd
import copy
import matplotlib.pyplot as plt
from classes import Workbook
import numpy as np
plt.style.use('seaborn-notebook')


def plot_simple(gas, instance: Workbook, heat_ratio: str, fig=0, i=0, colour=0):
        if fig==0:
                fig = plt.figure(figsize=(6.5, 6))
        # assign x and y values
        x_val = Workbook.lists_to_array(instance.df, float,'mean_eq')
        y_val = Workbook.lists_to_array(instance.df, float,'X_'+gas)
        x_error = Workbook.lists_to_array(instance.df, float, 'error_eq')
        y_error = Workbook.lists_to_array(instance.df, float, 'delta_X_'+gas)

        plt.errorbar(x_val, y_val, yerr=y_error, fmt='none', zorder=9, color= 'darkgrey'if colour==0 else colour, figure=fig, elinewidth=1)
        # sort them so that polyfit gives correct result
        (x_val, y_val) = Workbook.sort_two_lists(x_val, y_val)

        # create line of best fit and error bars
        trend = np.polyfit(x_val, y_val, 12)
        trendpoly = np.poly1d(trend)
        # add axies names and details
        plt.title(heat_ratio + ' Heat Ratio', pad=15, figure=fig)
        plt.xlabel('equivalence ratio', figure=fig)
        plt.ylabel(gas+' concentration', figure=fig)
        plt.tight_layout()

        # Turn on the minor TICKS, which are required for the minor GRID
        plt.minorticks_on()
        # Customize the major and minor grids
        plt.grid(which='major', linestyle='-', linewidth='0.5', color='darkgrey', zorder=0, figure=fig)
        plt.grid(which='minor', linestyle=':', linewidth='0.5', color='silver', zorder=0, figure=fig)

        # plot scatter graph
        if colour == 0:
                plt.plot(x_val, trendpoly(x_val), linestyle=':', dashes=(6, 5), linewidth='1.3', color='gray' if colour==0 else colour, zorder=8, figure=fig)
        plt.scatter(x_val, y_val,color='darkblue', zorder=10, s=20, label='Marina experiment data' if i==0 else "", figure=fig)
        plt.legend()
        return fig

def plot_by_mode(gas, instance: Workbook, heat_ratio: str, fig=0, i=0, colour=0,legend=0):
        if fig==0:
                fig = plt.figure(figsize=(6.5, 6))

        # assign x and y values for individual modes
        x0_val = Workbook.lists_to_array(instance.df_0, float, 'mean_eq')
        y0_val = Workbook.lists_to_array(instance.df_0, float, 'X_' + gas)
        x0_error = Workbook.lists_to_array(instance.df_0, float, 'error_eq')
        y0_error = Workbook.lists_to_array(instance.df_0, float, 'delta_X_' + gas)
        plt.errorbar(x0_val, y0_val, yerr=y0_error, fmt='none', color='darkgrey' if colour==0 else colour, zorder=8, figure=fig, elinewidth=1)

        x1_val = Workbook.lists_to_array(instance.df_1, float, 'mean_eq')
        y1_val = Workbook.lists_to_array(instance.df_1, float, 'X_' + gas)
        x1_error = Workbook.lists_to_array(instance.df_1, float, 'error_eq')
        y1_error = Workbook.lists_to_array(instance.df_1, float, 'delta_X_' + gas)
        # plt.errorbar(x1_val, y1_val, yerr=y1_error, fmt='none', color='darkgrey' if colour==0 else colour, zorder=8, figure=fig,  elinewidth=1)

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

        # CONCAT
        n_x_val = x0_val + n_x2_val
        n_y_val = y0_val + n_y2_val

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
                plt.plot(n_x_val, trendpoly(n_x_val), linestyle=':', dashes=(6, 5), linewidth='1.3', color='gray' if colour==0 else colour, zorder=9, figure=fig)
        plt.scatter(x0_val, y0_val,color='blue'if colour==0 else colour, zorder=10, s=20, label='no dilution gas'if i==0 else legend, figure=fig)
        # plt.scatter(x1_val, y1_val,color='green' if colour==0 else colour, zorder=10, s=20, label='single dilution gas'if i==0 else "", figure=fig)
        plt.scatter(x2_val, y2_val,color='orange'if colour==0 else colour, zorder=10, s=20, label='two dilution gases' if i==0 else "", figure=fig)
        plt.legend()
        return fig

def create_plot(gas_list, instance: Workbook, heat_ratio: str):
    for gas in gas_list:
        new_fig = plot_by_mode(gas, instance, heat_ratio)
        new_fig.savefig('../excel/image_plots/'+heat_ratio + gas)

def create_plot_multiple(gas_list, instance: Workbook, heat_ratio: str, instance2: Workbook = 0, instance3: Workbook= 0):
    for gas in gas_list:
        new_fig = plot_by_mode(gas, instance, heat_ratio)
        if instance2 != 0:
            plot_by_mode(gas, instance2, heat_ratio, new_fig, 1, 'firebrick', "previous data" )
        if instance3 != 0:
            # plot_by_mode(gas, instance2, heat_ratio, new_fig, 1, 'pink', "high HCN and dilution gas flow")
            plot_by_mode(gas, instance3, heat_ratio, new_fig, 1, 'firebrick', "previous data")
        plt.savefig('../excel/image_plots/'+heat_ratio + gas)
