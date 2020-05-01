#before running this code pip install pandas, matplotlib and numpy libraries to your environment:
from classes import Workbook
import graphfuncs
import workbookfuncs

# run file with -W in script parameters. Warnings related to dataslice copies can be ignored because original dataframe is never used after splitting
import warnings

# ensure that all column headers match to code- that they are correct
# however, change the range columns for H2, O2 to 'range %' !

def main():
    warnings.filterwarnings("ignore")

    test2 = Workbook('/Users/marina/Developer/GitHub/gas-analysis-dilution-method/excel/test1.xlsx', 9,
                    ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3'], ['H2', 'O2'])
    test1 = Workbook('/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/plotting_data/100RESULTSbook18final(06042020).xlsx', 9,
                     ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3'], ['H2', 'O2'])
    # test3 = Workbook('/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/plotting_data/30RESULTSbook12final(04022020).xlsx', 15,
    #                  ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3'], ['H2', 'O2'])
    workbookfuncs.create_workbook(test1)
    # workbookfuncs.create_workbook(test3)
    # test.df.to_csv('../excel/image_plots/out.csv')

    graphfuncs.create_plot_multiple(test2.full_gas_list, test1, '100%')

if __name__ == "__main__":
    main()
