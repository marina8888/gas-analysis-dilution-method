# before running this code pip install pandas, matplotlib and numpy libraries to your environment:
from excel_file.classes import Workbook, BigWorkbook
from excel_file import create_workbook
from graph_creator import create_graphs
# run file with -W in script parameters. Warnings related to dataslice copies can be ignored because original dataframe is never used after splitting
import warnings


# ensure that all column headers match the excel template file in excel_file folder and there are no duplicates. 
# Ensure all gases measured by percentage are marked as 'range %' and that two gas lists are passed as Workbookclass arguments - first for ppmv and second for %

def main():
    warnings.filterwarnings("ignore")
    # import workbooks as dataframe objects
    test1 = Workbook('/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/plotting_data/60ERESULTSbook16final(0404020).xlsm', 15,
                     ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3'], ['H2', 'O2'])
    test2 = Workbook(
         '/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/plotting_data/100RESULTS(hayakawa).xlsx',
       15,
         ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3'], ['H2', 'O2'])
    test3 = Workbook(
        '/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/plotting_data/40RESULTSbook19final(07042020)new.xlsx',
        21,
        ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3'], ['H2', 'O2'])
    test4 = Workbook(
        '/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/plotting_data/30RESULTSbook20final(08042020).xlsx',
        24,
        ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3'], ['H2', 'O2'])
    test5 = Workbook(
        '/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/plotting_data/20ERESULTSbook21final(09042020).xlsx',
        24,
        ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3'], ['H2', 'O2'])
    test6 = Workbook(
        '/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/plotting_data/10RESULTSBook22final(11042020).xlsx',
        24,
        ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3'], ['H2', 'O2'])

    # create all columns and calculate uncertainties for all workbooks:
    instance_list = [test1, test2, test3, test4, test5, test6]
    for instance in instance_list:
        create_workbook.create_workbook(instance)
        # if required: save to csv file:
        # test.df.to_csv('../excel_external/image_plots/out.csv')

    # create lists and labels for all objects that need plotting. These can be modified to suit the plots:
    title = 'concentration by equivalence ratio'
    colour_list = ['firebrick', 'blue', 'green', 'orange', 'darkgrey']
    legend= 'mean_eq'
    heat_ratio_list = ['100%', '60%', '40%', '30%', '20%', '10%']
    legend_list=[0.85, 0.95, 1.05, 1.15, 1.25]
    #plot graph_creator for all gases and lists given above as input parameters to the graph_creator:
    create_graphs.plot_by_legend(test1.full_gas_list, instance_list, title, colour_list, legend, legend_list)


if __name__ == "__main__":
    main()
