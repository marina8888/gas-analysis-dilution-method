#before running this code pip install pandas, matplotlib and numpy libraries to your environment:
import pandas as pd
from classes import Workbook
import graphfuncs

# run file with -W in script parameters. Warnings related to dataslice copies can be ignored because original dataframe is never used after splitting
import warnings

# ensure that all column headers match to code- that they are correct
# however, change the range columns for H2, O2 to 'range %' !

def main():
    warnings.filterwarnings("ignore")

    test = Workbook('/Users/marina/Developer/GitHub/gas-analysis-dilution-method/excel/test1.xlsx', 15,
                    ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3'], ['H2', 'O2'])

    #fill columns with basic initial values
    test.Qd()
    test.Epsilon()
    test.Xitr()
    test.Z()
    test.X_gas()


    test.Qs()
    test.eq()

    #fill uncertainty columns
    test.X_Xi_gas()
    test.X_Epsilon_gas()
    test.X_Q_gas()
    test.X_x_gas()
    test.delta_X_gas()

    # concat and print
    test.concat()
    # test.print_df_uncert()

    # graphs
    graphfuncs.plot_all(test.full_gas_list, test, 'blah%')


if __name__ == "__main__":
    main()
