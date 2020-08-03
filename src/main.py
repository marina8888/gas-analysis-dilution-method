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
    # test1 = Workbook(
    #     '/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/plotting_data/60All.xlsx',
    #     15,
    #      ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3', 'HCN'], ['H2', 'O2'])
    # test2 = Workbook(
    #       '/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/plotting_data/100RESULTS(hayakawa).xlsx',
    #     15,
    #       ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3', 'HCN'], ['H2', 'O2'])
    # test3 = Workbook(
    #     '/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/plotting_data/40All.xlsx',
    #     21,
    #     ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3', 'HCN'], ['H2', 'O2'])
    # test4 = Workbook(
    #     '/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/plotting_data/30All.xlsx',
    #     24,
    #     ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3', 'HCN'], ['H2', 'O2'])
    # test5 = Workbook(
    #     '/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/plotting_data/20All.xlsx',
    #     24,
    #     ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3', 'HCN'], ['H2', 'O2'])
    # test6 = Workbook(
    #     '/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/plotting_data/10All.xlsx',
    #     24,
    #      ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3', 'HCN'], ['H2', 'O2'])

    # test7 = Workbook(
    #     '/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/plotting_data/N2ARESULTSbook12final(20022020).xlsx',
    #     15,
    #     ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3'], ['H2', 'O2'])
    # test8 = Workbook(
    #     '/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/plotting_data/N2RESULTSbook15finaledit(04012020).xlsx',
    #     15,
    #     ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3'], ['H2', 'O2'])
    # test9 = Workbook('/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/Final Results/CO2RESULTSbook21(31052020).xlsx', 15, ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3'], ['H2', 'O2'])
    # test10 = Workbook('/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/plotting_data/CO2RESULTSbook13final(21022020).xlsx', 15, ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3'], ['H2', 'O2'])
    # test11 = Workbook(
    #      '/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/plotting_data/60ERESULTSbook7final(30012020).xlsx',
    #      8,
    #      ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3'], ['H2', 'O2'])
    # test12 = Workbook('/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/plotting_data/30RESULTSbook20(08042020).xlsx', 24,
    #       ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3'], ['H2', 'O2'])
    # create all columns and calculate uncertainties for all workbooks:
    test12 = Workbook('/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/plotting_data/CO2RESULTSbook13final(21022020).xlsx', 15,  ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3'], ['H2', 'O2'])
    instance_list = [test12]

    for instance in instance_list:
        create_workbook.create_workbook(instance)

    # save all data with complete uncertainty calcs to one large csv file:
    all_heat_workbook = BigWorkbook(instance_list)
    all_heat_workbook.df.to_csv('../excel_external/image_plots/co2.csv')
    #
    # # create lists and labels for all objects that need plotting. These can be modified to suit the plots:
    # title = 'Gas Concentration vs Dilution Method 60% Heat Ratio'
    #
    # # # plot graph_creator for all gases and lists given above as input parameters to the graph_creator:
    # create_graphs.plot_by_workbook(test12.full_gas_list, instance_list, title, colour_list= ['r'])


if __name__ == "__main__":
    main()
