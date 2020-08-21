from excel_file.classes import Workbook
import pandas as pd


# dataframe object input is adjusted for pressure dependency of FTIR sensor

def pressure_correct(workbook: Workbook, pressure_correction_file: str):
    print("adding pressure correction")

