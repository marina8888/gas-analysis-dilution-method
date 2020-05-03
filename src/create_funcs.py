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


# def create_plot_eq(gas_list: list, instance_list: list, title_list: list, colour_list: list):
#     for gas in gas_list:
#         for t in title_list:
#             d = {}
#             d["new_fig{0}".format(gas)] = plt.figure(figsize=(6.5, 6))
#             for colour in zip(colour_list):
#                 plot_by_eq(gas, instance_list, equivalence_ratio=t, fig=d["new_fig" + gas], colour=colour)
#             plt.savefig('../excel/image_plots/' + 'all' + gas)
#
#
# def create_plot_heat(gas_list: list, heat_ratio_list: list, instance_list: list, legend_list: list,
#                      colour_list: list):
#     for gas in gas_list:
#         new_fig = plt.figure(figsize=(6.5, 6))
#         if instance_list is not None:
#             for heat_ratio, instance, legend, colour in zip(heat_ratio_list, instance_list, legend_list,
#                                                             colour_list):
#                 graph_funcs.plot_by_heat(gas, heat_ratio, instance, new_fig, legend, colour)
#         plt.savefig('../excel/image_plots/' + 'test' + gas)

def create_plot_by_heat(gas_list: list, instance_list: list, final_part_title: str, colour_list: list=None, legend_list:list=None):
    #Create and format new plot for each gas only:
    for gas in gas_list:
        fig = plt.figure(figsize=(6.5, 6))
        #title artguments - first part+final part can be from list or variable (e.g gas, eq_ratio)
        graph_funcs.format_graph(gas, final_part_title, fig, 'Equivalence ratio', gas + ' concentration')

        #iterate over all instances (heat fractions) on one gas plot:
        for instance, colour in zip(instance_list, colour_list):
            #assign x and y values to a dictionary to use as graph data:
            d = graph_funcs.assign_xy('mean_eq', 'error_eq', 'X_' + gas, 'delta_X_' + gas, instance)

            # plot error bars based on dictionary values for all three dataframes
            graph_funcs.plot_error(d, fig, colour)
            graph_funcs.polyfit_xy(d, fig, colour)
            # plot scatter graph with legends (default legends and colours available here)
            graph_funcs.plot_scatter(d, fig, legend_list)
        plt.savefig('../excel/image_plots/' + 'test' + gas)



# def plot_by_eq(gas: str, instance_list: list, equivalence_ratio: str, fig=None, colour=None):
#     if fig is None:
#         fig = plt.figure(figsize=(6.5, 6))
#
#     df_0, df_1, df_2 = Workbook.concat_all(instance_list)
#     # assign x and y values for individual modes
#     if df_0 is not None:
#         x0_val = Workbook.lists_to_array(df_0, float, 'mean_heat')
#         y0_val = Workbook.lists_to_array(df_0, float, 'X_' + gas)
#         x0_error = Workbook.lists_to_array(df_0, float, 'error_heat')
#         y0_error = Workbook.lists_to_array(df_0, float, 'delta_X_' + gas)
#         # plt.errorbar(x0_val, y0_val, yerr=y0_error, fmt='none', color='darkgrey'if colour==None else colour, zorder=8,
#         #              figure=fig, elinewidth=1)
#     else:
#         x0_val = None
#         y0_val = None
#
#     if df_1 is not None:
#         x1_val = Workbook.lists_to_array(df_1, float, 'heat_eq')
#         y1_val = Workbook.lists_to_array(df_1, float, 'X_' + gas)
#         x1_error = Workbook.lists_to_array(df_1, float, 'error_heat')
#         y1_error = Workbook.lists_to_array(df_1, float, 'delta_X_' + gas)
#         # plt.errorbar(x1_val, y1_val, yerr=y1_error, fmt='none', color='darkgrey' if colour==None else colour, zorder=8,
#         #              figure=fig, elinewidth=1)
#     else:
#         x1_val = None
#         y1_val = None
#
#     if df_2 is not None:
#         x2_val = Workbook.lists_to_array(df_2, float, 'heat_eq')
#         y2_val = Workbook.lists_to_array(df_2, float, 'X_' + gas)
#         x2_error = Workbook.lists_to_array(df_2, float, 'error_eq')
#         y2_error = Workbook.lists_to_array(df_2, float, 'delta_X_' + gas)
#         # plt.errorbar(x2_val, y2_val, yerr=y2_error, fmt='none', color='darkgrey' if colour==None else colour, zorder=8,
#         #              figure=fig, elinewidth=1)
#         # prepare line of best fit by grouping dilution gas pairs in df2
#         local_dataframe = pd.DataFrame({'n_x2_val': x2_val, 'n_y2_val': y2_val}).copy(deep=True)
#         local_dataframe['n_x2_val'] = local_dataframe['n_x2_val'].round(2)
#         local_dataframe = local_dataframe.groupby('n_x2_val').mean()
#         n_x2_val = local_dataframe.index.to_list()
#         n_y2_val = local_dataframe['n_y2_val'].to_list()
#     else:
#         n_x2_val = None
#         n_y2_val = None
#         # CONCAT
#     n_x_val = x0_val + x1_val + n_x2_val
#     n_y_val = y0_val + y1_val + n_y2_val
#
#     # SORT IT 😜
#     tuples = list(zip(n_x_val, n_y_val))
#     tuples = sorted(tuples, key=lambda tup: tup[0])
#     n_x_val = [tup[0] for tup in tuples]
#     n_y_val = [tup[1] for tup in tuples]
#
#     # Polyfit trend
#     trend = np.polyfit(n_x_val, n_y_val, 16)
#     trendpoly = np.poly1d(trend)
#
#     # add axies names and details
#     plt.title(gas + ', ' + equivalence_ratio, pad=15, figure=fig)
#     plt.xlabel('NH3 heat ratio', figure=fig)
#     plt.ylabel(gas + ' concentration', figure=fig)
#     plt.tight_layout()
#
#     # Turn on the minor TICKS, which are required for the minor GRID
#     plt.minorticks_on()
#     # Customize the major and minor grids
#     plt.grid(which='major', linestyle='-', linewidth='0.5', color='darkgrey', zorder=0, figure=fig)
#     plt.grid(which='minor', linestyle=':', linewidth='0.5', color='silver', zorder=0, figure=fig)
#
#     # plot scatter graph
#
#     return fig
