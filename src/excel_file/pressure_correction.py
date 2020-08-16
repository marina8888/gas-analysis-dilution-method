from excel_file.classes import Workbook
import pandas as pd


# dataframe object input is adjusted for pressure dependency of FTIR sensor

def pressure_correct(workbook: Workbook, pressure_correction_file: str):
    print("adding pressure correction")
    if pressure_correction_file.endswith('.csv'):
        p_df = pd.read_excel(pressure_correction_file, sheet_name='Main')
        workbook['name of temp mfm']
        workbook['name of FT mfm']
    elif pressure_correction_file.endswith('xlsx'):
        p_df = pd.read_csv(pressure_correction_file)
        workbook['name of temp mfm']
        workbook['name of FT mfm']
    else:
        raise TypeError('ensure pressure correction file format must be .xlsx or .csv')
