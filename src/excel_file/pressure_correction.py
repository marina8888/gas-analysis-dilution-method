from excel_file.classes import Workbook


# dataframe object input is adjusted for pressure dependency of FTIR sensor

def pressure_correct(instance: Workbook, pressure_correction_file: str):
    print("adding pressure correction")
    if pressure_correction_file.endswith('.csv'):
        pass
    elif pressure_correction_file.endswith('xlsx'):
        pass
    else:
        raise TypeError('ensure pressure correction file format must be .xlsx or .csv')
