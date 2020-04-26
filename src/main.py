import pandas as pd
from classes import Workbook

# run file with -W in script parameters. Warnings related to dataslice copies can be ignored because original dataframe is never used after splitting
import warnings


def main():
    warnings.filterwarnings("ignore")
    workbook_name = input("please input the filepath of workbook you will be working with today: ")
    test = Workbook(workbook_name, 15)
    test.Qd()
    test.Epsilon()
    test.Xitr()
    # test.Qs()
    # test.Z()
    test.upper_eq()
    test.lower_eq()
    test.concat()
    print(test.df_mode0['Xitr1'])
    print(test.df_mode0['Xitr2'])
    print(test.df_mode1['Xitr1'])
    print(test.df_mode1['Xitr2'])
    print(test.df_mode2['Xitr1'])
    print(test.df_mode2['Xitr2'])
    print(test.df['Xitr1'])
    print(test.df['Xitr2'])


if __name__ == "__main__":
    main()
