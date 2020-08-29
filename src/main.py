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
    test1 = Workbook(
        '/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/repeat_experiments/60%E_14-08-2020_BOOK1.xlsx',
        27,
         ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3', 'HCN'], ['H2', 'O2'])
    test2 = Workbook(
          '/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/repeat_experiments/40%E_15-08-2020_BOOK2.xlsx',
        27,
          ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3', 'HCN'], ['H2', 'O2'])
    test3 = Workbook(
        '/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/repeat_experiments/30%E_16-08-2020_BOOK3.xlsx',
        27,
        ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3', 'HCN'], ['H2', 'O2'])
    test4 = Workbook(
        '/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/repeat_experiments/20%E_17-08-2020BOOK4.xlsx',
        27,
        ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3', 'HCN'], ['H2', 'O2'])
    test5 = Workbook(
        '/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/repeat_experiments/10%E_26-08-2020BOOK10.xlsx',
        27,
        ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3', 'HCN'], ['H2', 'O2'])
    test6 = Workbook(
        '/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/repeat_experiments/AllE_Confirmation_Experiment_27-08-2020BOOOK11.xlsx',
        27,
        ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3', 'HCN'], ['H2', 'O2'])


    # create all columns and calculate uncertainties for all workbooks:
    instance_list = [test1,test2,test3,test4,test5,test6]

    for instance in instance_list:
        create_workbook.create_workbook(instance)

    # save all data with complete uncertainty calcs to one large csv file:
    all_heat_workbook = BigWorkbook(instance_list)
    all_heat_workbook.df.to_csv('../excel_external/image_plots/repeatfinal4.csv')
    #
    # # create lists and labels for all objects that need plotting. These can be modified to suit the plots:
    # title = 'Gas Concentration vs Dilution Method 60% Heat Ratio'
    #
    # # # plot graph_creator for all gases and lists given above as input parameters to the graph_creator:
    # create_graphs.plot_by_workbook(test12.full_gas_list, instance_list, title, colour_list= ['r'])


if __name__ == "__main__":
    main()
