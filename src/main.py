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

    test1 = Workbook('/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/plotting_data/30RESULTSbook345final(23012020)new.xlsx', 15,
                    ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3'], ['H2', 'O2'])
    test2 = Workbook('/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/plotting_data/20ERESULTSbook21final(09042020).xlsx', 24,
                     ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3'], ['H2', 'O2'])
    test3 = Workbook('/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/plotting_data/20RESULTSbook9final(05022020).xlsx', 15,
                     ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3'], ['H2', 'O2'])
    workbookfuncs.create_workbook(test1)
    workbookfuncs.create_workbook(test2)
    workbookfuncs.create_workbook(test3)

    # test.df.to_csv('../excel/image_plots/out.csv')

    graphfuncs.create_plot_multiple(test1.full_gas_list, test1, '30%')

if __name__ == "__main__":
    main()
