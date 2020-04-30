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

    test = Workbook('/Users/marina/Developer/GitHub/gas-analysis-dilution-method/excel/test1.xlsx', 15,
                    ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3'], ['H2', 'O2'])
    test2 = Workbook('/Users/marina/Developer/GitHub/gas-analysis-dilution-method/excel/test2.xlsx', 18,
                    ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3'], ['H2', 'O2'])

    workbookfuncs.create_workbook(test)
    workbookfuncs.create_workbook(test2)
    # graphs
    # graphfuncs.plot_all(test.full_gas_list, test, 'blah%')
    # graphfuncs.plot_all('O2', test, 'blah%')
    # graphfuncs.plot_by_mode('O2', test, 'blah%')
    graphfuncs.create_plot_multiple(test.full_gas_list, test, 'blah%', test2)

if __name__ == "__main__":
    main()
