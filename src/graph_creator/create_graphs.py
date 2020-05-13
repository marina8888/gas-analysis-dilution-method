from graph_creator import graph_funcs
import matplotlib.pyplot as plt
from excel_file.classes import Workbook, BigWorkbook

def plot_by_legend(gas_list: list, instance_list: [Workbook], final_part_title: str, colour_list: list= None, legend:str=None, legend_list: list = None):
    if len(colour_list) != len(legend_list):
        raise ValueError("pls input same number of colours in colour_list as legends in the legend_list")
    for gas in gas_list:
        fig = plt.figure(figsize=(6.5, 6))
        # title artguments - first part+final part can be from list or variable (e.g gas, eq_ratio)
        graph_funcs.format_graph(gas, final_part_title, fig, 'CO2 flowrate', gas + ' concentration')
        # create big_workbook from instances containing a df_list of three dataframes (0,1,2):
        eq_workbooks = BigWorkbook(instance_list)
        # round legend col before splitting by all cols with same legend:
        eq_workbooks.round_col(legend)
        df_para_split_list=eq_workbooks.split_df_list_by_para(legend, legend_list)

        # iterate over all legends (equivalence ratios) on one gas plot:
        for df_mini, l, colour in zip(df_para_split_list, legend_list, colour_list):
            # assign these three dfs to a dictionary containing x and y values:
            d_mini = graph_funcs.assign_xy_from_list('N2 upper', 'N2 lower', 'X_' + gas, 'delta_X_' + gas, df_mini, legend)

            # plot error bars based on dictionary values for all three dataframes:
            graph_funcs.plot_error(d_mini, fig, colour)
            graph_funcs.polyfit_xy(d_mini, fig, colour)
            # plot scatter graph with legends (default legends and colours available here):
            graph_funcs.plot_scatter(d_mini, fig, colour, l)

        plt.savefig('../excel_external/image_plots/' + 'CO2_conc' + gas)

#note there may be an error relating to legend_list not being a list:
def plot_by_workbook(gas_list: list, instance_list: [Workbook], final_part_title: str, colour_list: list=None, legend_list:list=None):
    #Create and format new plot for each gas only:
    for gas in gas_list:
        fig = plt.figure(figsize=(6.5, 6))
        #title artguments - first part+final part can be from list or variable (e.g gas, eq_ratio)
        graph_funcs.format_graph(gas, final_part_title, fig, 'CO2 Concentration', gas + ' concentration')

        #iterate over all instances (heat fractions) on one gas plot:
        for instance, colour in zip(instance_list, colour_list):
            #assign x and y values to a dictionary to use as graph data:
            d = graph_funcs.assign_xy_from_inst('Qd1_upper', 'Qd1_upper', 'X_' + gas, 'delta_X_' + gas, instance)

            # plot error bars based on dictionary values for all three dataframes
            graph_funcs.plot_error(d, fig)
            graph_funcs.polyfit_xy(d, fig)
            # plot scatter graph with legends (default legends and colours available here)
            graph_funcs.plot_scatter(d, fig, legend_list)
        plt.savefig('../excel_external/image_plots/' + 'CO2Conc' + gas)

def plot_all_gas_on_one(gas_list: list, instance_list: [Workbook], final_part_title: str, colour_list: list= None, legend:str=None, legend_list: list = None):
    if len(colour_list) != len(legend_list):
        raise ValueError("pls input same number of colours in colour_list as legends in the legend_list")
    for gas in gas_list:
        fig = plt.figure(figsize=(6.5, 6))
        # title artguments - first part+final part can be from list or variable (e.g gas, eq_ratio)
        graph_funcs.format_graph(gas, final_part_title, fig, 'N2 flowrate', gas + ' concentration')
        # create big_workbook from instances containing a df_list of three dataframes (0,1,2):
        eq_workbooks = BigWorkbook(instance_list)
        # round legend col before splitting by all cols with same legend:
        eq_workbooks.round_col(legend)
        df_para_split_list=eq_workbooks.split_df_list_by_para(legend, legend_list)

        # iterate over all legends (equivalence ratios) on one gas plot:
        for df_mini, l, colour in zip(df_para_split_list, legend_list, colour_list):
            # assign these three dfs to a dictionary containing x and y values:
            d_mini = graph_funcs.assign_xy_from_list('N2 upper', 'N2 lower', 'X_' + gas, 'delta_X_' + gas, df_mini, legend)

            # plot error bars based on dictionary values for all three dataframes:
            graph_funcs.plot_error(d_mini, fig, colour)
            graph_funcs.polyfit_xy(d_mini, fig, colour)
            # plot scatter graph with legends (default legends and colours available here):
            graph_funcs.plot_scatter(d_mini, fig, colour, l)

        plt.savefig('../excel_external/image_plots/' + 'N2_conc' + gas)
