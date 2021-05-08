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
        '/Users/marina/Documents/Work/Tohoku-Uni/CH4-NH3/For_Paper/c_dependency_27-07-2020BOOK14_rangeedit.xlsx',
        27,
         ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3', 'HCN'], ['H2', 'O2'])
    test2 = Workbook(
          '/Users/marina/Documents/Work/Tohoku-Uni/CH4-NH3/For_Paper/N2ARESULTSbook12final(20022020)_rangeedit.xlsx',
        15,
          ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3', 'HCN'], ['H2', 'O2'])
    test3 = Workbook(
        '/Users/marina/Documents/Work/Tohoku-Uni/CH4-NH3/For_Paper/Sampling_rate_matrix_27-08-2020BOOK12.xlsx',
        27,
        ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3', 'HCN'], ['H2', 'O2'])
    test4 = Workbook(
        '/Users/marina/Documents/Work/Tohoku-Uni/CH4-NH3/For_Paper/Temperature_27-08-2020_BOOK13.xlsx',
        27,
        ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3', 'HCN'], ['H2', 'O2'])



    # create all columns and calculate uncertainties for all workbooks:
    instance_list = [test1,test2,test3,test4]

    for instance in instance_list:
        create_workbook.create_workbook(instance)

    # save all data with complete uncertainty calcs to one large csv file:
    all_heat_workbook = BigWorkbook(instance_list)
    all_heat_workbook.df.to_csv('../excel_external/image_plots/appendix.csv')
    #
    # # create lists and labels for all objects that need plotting. These can be modified to suit the plots:
    # title = 'Gas Concentration vs Dilution Method 60% Heat Ratio'
    #
    # # # plot graph_creator for all gases and lists given above as input parameters to the graph_creator:
    # create_graphs.plot_by_workbook(test12.full_gas_list, instance_list, title, colour_list= ['r'])


if __name__ == "__main__":
    main()
