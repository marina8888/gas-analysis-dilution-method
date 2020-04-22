import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from classes import Workbook
from pandas import ExcelFile
from pandas import ExcelWriter


def main():
    workbook_name = input("please input the filepath of workbook you will be working with today: ")
    test = Workbook(workbook_name, 15)


if __name__ == "__main__":
    main()
