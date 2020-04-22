import numpy as np
import pandas as pd


# class workbook imports variables as arrays from excel file given an excel starting row number from which data collection begins
# intialises a list of lists (from a pandas dataframe) and into np arrays that represent each variable
class Workbook():
    def __init__(self, workbook_name, start_row_number: int):
        self.df = pd.read_excel(workbook_name, sheet_name='Main')
        self.workbook_name = workbook_name
        self.start_row_number = start_row_number
        self.df = self.prepare_df()
        self.df=self.split_df()
        # self.df = self.df.values.tolist()
        #
        # # defining all variables that are stored directly in spreadsheet
        # self.gas_type = self.lists_to_array(int, 7)
        # print("gases types are: " + str(self.gas_type))

    def prepare_df(self):
        self.df = self.df.iloc[self.start_row_number - 2:]
        self.df = self.df.reset_index(drop=True)
        self.df = self.df.T
        return self.df

    def split_df(self):
        self.df= self.df[self.df['Unnamed: 7'] == '0']
        print(self.df)
        return self.df


    def lists_to_array(self, datatype, col_num: int):
        list = (self.df[col_num])
        for i in range(0, len(list)):
            list[i] = datatype(list[i])
        return list

    def mode(self):
        pass
        # while self.df[7])==0:
        #     list = (self.df[col_num])
        #     for i in range(0, len(list)):
        #         list[i] = datatype(list[i])
        #     return list
