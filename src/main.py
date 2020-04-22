from . import functions
from . import classes

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import openpyxl as xl


# chosen_workbook=input("please input the filepath of workbook you will be working with today: ")
def main():
    wb = xl.load_workbook('/Users/marina/Developer/GitHub/gas-analysis-dilution-method/excel/test1.xlsx',
                          read_only=True, data_only=True)
    sheet = wb["Main"]
    # wb.save()


if __name__ == "__main__":
    main()
