from classes import Workbook
import graphfuncs


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


def create_plot_eq(gas_list: list, instance_list: list, title_list: list, colour_list: list):
    for gas in gas_list:
        for t in title_list:
            d = {}
            d["new_fig{0}".format(gas)] = plt.figure(figsize=(6.5, 6))
            for colour in zip(colour_list):
                plot_by_eq(gas, instance_list, equivalence_ratio=t, fig=d["new_fig" + gas], colour=colour)
            plt.savefig('../excel/image_plots/' + 'all' + gas)


def create_plot_heat(gas_list: list, heat_ratio_list: list, instance_list: list, legend_list: list,
                     colour_list: list):
    for gas in gas_list:
        new_fig = plt.figure(figsize=(6.5, 6))
        if instance_list is not None:
            for heat_ratio, instance, legend, colour in zip(heat_ratio_list, instance_list, legend_list,
                                                            colour_list):
                plot_by_heat(gas, heat_ratio, instance, new_fig, legend, colour)
        plt.savefig('../excel/image_plots/' + 'test' + gas)
