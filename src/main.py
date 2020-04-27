import pandas as pd
from classes import Workbook
import basicvariables

# run file with -W in script parameters. Warnings related to dataslice copies can be ignored because original dataframe is never used after splitting
import warnings


def main():
    warnings.filterwarnings("ignore")

    # gases = input("please input the gases as a comma seperated list: ")
    # gas_list=gases.split()
    # workbook_name = input("please input the filepath of workbook you will be working with today: ")
    # test = Workbook(workbook_name, 15, gas_list)

    test = Workbook('/Users/marina/Developer/GitHub/gas-analysis-dilution-method/excel/test1.xlsx', 15,
                    ['O2', 'N2', 'Air', 'CH4'])
    # fill columns for basic/inital values
    print(test.df.columns.values)
    test.Qd()
    test.Epsilon()
    test.Xitr()
    test.Qs()
    test.Z()
    test.upper_eq()
    test.lower_eq()
    # test.X_gas()
    # test.X_Xi1_gas()
    # test.X_Epsilon_gas()
    # test.X_Q_gas():
    # test.X_x_gas():
    # test.delta_X_gas():
    # fill columns for gas specific values and uncertainties

    # complete and print
    test.concat()
    print(test.df_0['Z'])
    print(test.df_1['Z'])
    print(test.df_2['Z'])
    print(test.df['Z'])

    # graphs


if __name__ == "__main__":
    main()
