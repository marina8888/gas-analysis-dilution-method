from classes import Workbook
import graph_funcs
import matplotlib.pyplot as plt


#all functions in this file create a new plot, assist with creating workbooks,and are general 'create' fucntions

def create_workbook(instance: Workbook):
    #fill columns with basic initial values
    instance.Qd()
    instance.Epsilon()
    instance.Xitr()
    instance.Z()
    instance.X_gas()

    instance.Qs()
    instance.heat()
    instance.eq()


    #fill uncertainty columns
    instance.X_Xi_gas()
    instance.X_Epsilon_gas()
    instance.X_Q_gas()
    instance.X_x_gas()
    instance.delta_X_gas()
    # concat and print
    instance.concat_df()

#
def create_plot_by_eq(gas_list: list, instance_list: list, final_part_title: str, colour_list: list= None, legend_list:list=None):
    for gas in gas_list:
        fig = plt.figure(figsize=(6.5, 6))
        # title artguments - first part+final part can be from list or variable (e.g gas, eq_ratio)
        graph_funcs.format_graph(gas, final_part_title, fig, 'Heat ratio', gas + ' concentration')
        # iterate over all instances (heat fractions) on one gas plot:
        for instance, colour in zip(instance_list, colour_list):
            # concat all instances to three dataframes (df_0, df_1, df_2):
            df_list=Workbook.concat_all(instance_list)
            # assign these three dfs to a dictionary containing x and y values:
            d = graph_funcs.assign_xy_from_list('mean_heat', 'error_heat', 'X_' + gas, 'delta_X_' + gas, df_list)
            d=graph_funcs.add_legend_to_df(d, 'mean_eq', df_list)
            d=graph_funcs.round_col(d, 'x0_val')
            d=graph_funcs.round_col(d, 'x1_val')
            d=graph_funcs.round_col(d, 'x2_val')
            # plot error bars based on dictionary values for all three dataframes
            graph_funcs.plot_error(d, fig, colour)
            graph_funcs.polyfit_xy(d, fig, colour)
            # plot scatter graph with legends (default legends and colours available here)
            graph_funcs.plot_scatter(d, fig, legend_list)
        plt.savefig('../excel/image_plots/' + 'test' + gas)

def create_plot_by_heat(gas_list: list, instance_list: list, final_part_title: str, colour_list: list=None, legend_list:list=None):
    #Create and format new plot for each gas only:
    for gas in gas_list:
        fig = plt.figure(figsize=(6.5, 6))
        #title artguments - first part+final part can be from list or variable (e.g gas, eq_ratio)
        graph_funcs.format_graph(gas, final_part_title, fig, 'Equivalence ratio', gas + ' concentration')

        #iterate over all instances (heat fractions) on one gas plot:
        for instance, colour in zip(instance_list, colour_list):
            #assign x and y values to a dictionary to use as graph data:
            d = graph_funcs.assign_xy_from_inst('mean_eq', 'error_eq', 'X_' + gas, 'delta_X_' + gas, instance)

            # plot error bars based on dictionary values for all three dataframes
            graph_funcs.plot_error(d, fig, colour)
            graph_funcs.polyfit_xy(d, fig, colour)
            # plot scatter graph with legends (default legends and colours available here)
            graph_funcs.plot_scatter(d, fig, legend_list)
        plt.savefig('../excel/image_plots/' + 'test' + gas)
