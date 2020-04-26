import pandas as pd
from classes import Workbook

import warnings

def main():
    warnings.filterwarnings("ignore")
    workbook_name = input("please input the filepath of workbook you will be working with today: ")
    test = Workbook(workbook_name, 15)
    test.Qd()
    test.Epsilon()
    test.Qs()
    test.Z()
    test.upper_eq()
    test.lower_eq()
    test.concat()



if __name__ == "__main__":
    main()
