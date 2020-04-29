#before running this code pip install pandas, matplotlib and numpy libraries to your environment:
import pandas as pd
from classes import Workbook
import basicvariables

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
    test.X_gas()

    test.Qs()
    test.Z()
    test.upper_eq()
    test.lower_eq()

    test.X_Xi_gas()
    test.X_Epsilon_gas()
    test.X_Q_gas()
    test.X_x_gas()
    test.delta_X_gas()
    # fill columns for gas specific values and uncertainties

    # concat and print
    test.concat()
    this_gas_list = ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3'], ['H2', 'O2']
    for gas in this_gas_list:
        print(test.df['X_' + gas], test.df['X_Xi1_' + gas], test.df['Delta_Xitr1_' + gas],test.df['delta_x_' + gas])

    # graphs


if __name__ == "__main__":
    main()
