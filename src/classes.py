import numpy as np
import pandas as pd


# class workbook imports variables as arrays from excel file given an excel starting row number from which data collection begins
# intialises a list of lists (from a pandas dataframe) and into np arrays that represent each variable
class Workbook():
    def __init__(self, workbook_name, start_row_number: int):
        self.df = pd.read_excel(workbook_name, sheet_name='Main')
        self.workbook_name = workbook_name
        self.start_row_number = start_row_number

        self.df = self.prepare_df
        self.df_mode0 = self.split_df_mode0()
        self.df_mode0 = self.upper_eq()
        # # defining all variables that are stored directly in spreadsheet
        # self.gas_type = self.lists_to_array(int, 7)
        # print("gases types are: " + str(self.gas_type))

    @property
    def prepare_df(self):
        # cut sheet for relevant data only
        self.df = self.df.iloc[self.start_row_number - 3:]
        self.df = self.df.reset_index(drop=True)

        # rename columns
        new_header = self.df.iloc[0]  # grab the first row for the header
        self.df = self.df[1:]  # take the data less the header row
        self.df.columns = new_header  # set the header row as the df header
        self.df['upper_eq']= None
        return self.df

    def split_df_mode0(self):
        # column 7 is called Tracer gas type - this works
        self.df_mode0 = self.df[self.df['Tracer gas type'] == '0']
        return self.df_mode0

    # def split_df_mode1(self):
    #     # I need something like this, where for this file the print statement would return 1,1,1,1...:
    #     for row_index in self.df[7]:
    #         self.df_mode1 = self.df[self.df['Tracer gas type', row_index] == ['Tracer gas type', row_index+1] ]
    #     print(self.df_mode2.iloc[:,7])
    #     return self.df_mode1

    # def split_df_mode2(self):
    #     #I need something like this, where this print statement returns 1,2,1,2,1,2,1,2...:
    #     for row_index in self.df[7]:
    #         self.df_mode2 = self.df[self.df['Tracer gas type', row_index] =='1' & ['Tracer gas type', row_index+1] =='2']]
    #     print(self.df_mode2.iloc[:,7])
    #     return self.df_mode2

    def lists_to_array(self, datatype, col_num: int):
        self.df = self.df.T
        self.df = self.df.values.tolist()
        list = (self.df[col_num])
        for i in range(0, len(list)):
            list[i] = datatype(list[i])
        return list

    def upper_eq(self):
        print((4.76 / (self.df_mode0.iloc[:, 32])) * (2 * self.df_mode0.iloc[:, 33]) + (
                    0.75 * self.df_mode0.iloc[:, 35]))

        self.df_mode0.loc[0:len(self.df.index),'upper_eq']= (4.76 / (self.df_mode0.iloc[:, 32])) * (2 * self.df_mode0.iloc[:, 33]) + (
                    0.75 * self.df_mode0.iloc[:, 35])
        print(self.df_mode0.iloc[:, -1])
        return self.df_mode0
