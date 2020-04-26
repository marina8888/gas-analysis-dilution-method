import numpy as np
import pandas as pd


# class workbook imports variables as arrays from excel file given an excel starting row number from which data collection begins
# intialises a list of lists (from a pandas dataframe) and into np arrays that represent each variable
class Workbook():
    def __init__(self, workbook_name, start_row_number: int):
        self.df = pd.read_excel(workbook_name, sheet_name='Main')
        self.workbook_name = workbook_name
        self.start_row_number = start_row_number

        self.prepare_df()
        self.init_cols()

        # called in this order because mode 1 is least selective
        self.df_mode0 = self.split_df_mode0()
        self.df_mode1 = self.split_df_mode1()
        self.df_mode2 = self.split_df_mode2()

    def prepare_df(self):
        # cut sheet for relevant data only
        self.df = self.df.iloc[self.start_row_number - 3:]
        self.df = self.df.reset_index(drop=True)

        # rename columns
        new_header = self.df.iloc[0]  # grab the first row for the header
        self.df = self.df[1:]  # take the data less the header row
        self.df.columns = new_header  # set the header row as the df header

    # initialising new columns for storing variables
    def init_cols(self):
        self.df['Qd1_upper'] = None
        self.df['Qd1_lower'] = None
        self.df['Qd2_upper'] = None
        self.df['Qd2_lower'] = None
        self.df['Epsilontr1'] = None
        self.df['Epsilontr2'] = None
        self.df['Qs'] = None
        self.df['Z'] = None
        self.df['upper_eq'] = None
        self.df['lower_eq'] = None

        #values per gas
        self.df['x1']= None
        self.df['x2']= None
        self.df['X1'] = None
        self.df['X2'] = None
        self.df['X_Xi1'] = None
        self.df['X_Xi2'] = None
        self.df['X_Epsilon1'] = None
        self.df['X_Epsilon2'] = None
        self.df['X_Q1'] = None
        self.df['X_Q2'] = None
        self.df['X_x']=None
        self.df['X_x'] = None


    # splitting df by tracer gas column into mode0 (no gas) mode 1 and 2
    def split_df_mode0(self):
        self.df_mode0 = self.df[self.df['Tracer gas type'] == '0']
        return self.df_mode0

    def split_df_mode1(self):
        # create a new empty dataframe with same columns and number of columns as previous dataframe
        df_mode1 = pd.DataFrame().reindex_like(self.df)
        df_mode1 = df_mode1.iloc[0:0]
        # initalising first and second col values to check
        last_tgt = ''
        this_tgt = ''

        # go over all rows in df.values
        for row_id in range(0, len(self.df.values)):
            this_tgt = self.df.iloc[row_id][7]
            # leave out the first row for comparison
            if (last_tgt != ''):
                # if dataframe rows are consecutively equal, write to new dataframe
                if ((this_tgt == '1' and last_tgt == '1') or (this_tgt == '2' and last_tgt == '2')):
                    df_mode1.loc[len(df_mode1)] = self.df.iloc[row_id - 1]
            last_tgt = this_tgt
        return df_mode1

    def split_df_mode2(self):
        # create a new empty dataframe with same columns and number of columns as previous dataframe
        df_mode2 = pd.DataFrame().reindex_like(self.df)
        df_mode2 = df_mode2.iloc[0:0]
        # initalising first and second col values to check
        last_tgt = ''
        this_tgt = ''

        # go over all rows in df.values
        for row_id in range(0, len(self.df.values)):
            this_tgt = self.df.iloc[row_id][7]
            # leave out the first row for comparison
            if (last_tgt != ''):
                # if the last tgt was 1 and this is 2 then write both rows to the new dataset
                if (this_tgt == '2' and last_tgt == '1'):
                    df_mode2.loc[len(df_mode2)] = self.df.iloc[row_id - 1]
                    df_mode2.loc[len(df_mode2)] = self.df.iloc[row_id]
            last_tgt = this_tgt
        return df_mode2

    def lists_to_array(self, datatype, col_num: int):
        self.df = self.df.T
        self.df = self.df.values.tolist()
        list = (self.df[col_num])
        for i in range(0, len(list)):
            list[i] = datatype(list[i])
        return list

    def concat(self):
        split_dataframes = [self.df_mode0, self.df_mode1, self.df_mode2]
        self.df = pd.concat(split_dataframes)
        self.df = self.df.reset_index(drop=True)


    # below are methods for calculating values in all three dataframes
    def upper_eq(self):
        if self.df_mode0 is not None:
            self.df_mode0['upper_eq'] = (4.76 / (self.df_mode0.iloc[:, 32])) * ((2 * self.df_mode0.iloc[:, 33])
                                                                                + (0.75 * self.df_mode0.iloc[:, 35]))
        if self.df_mode1 is not None:
            self.df_mode1['upper_eq'] = (4.76 / (self.df_mode1.iloc[:, 32])) * ((2 * self.df_mode1.iloc[:, 33])
                                                                                + (0.75 * self.df_mode1.iloc[:, 35]))
        if self.df_mode2 is not None:
            self.df_mode2['upper_eq'] = (4.76 / (self.df_mode2.iloc[:, 32])) * ((2 * self.df_mode2.iloc[:, 33])
                                                                                + (0.75 * self.df_mode2.iloc[:, 35]))

    def lower_eq(self):
        if self.df_mode0 is not None:
            self.df_mode0['lower_eq'] = (4.76 / (self.df_mode0.iloc[:, 31])) * ((2 * self.df_mode0.iloc[:, 34])
                                                                                + (0.75 * self.df_mode0.iloc[:, 36]))
        if self.df_mode1 is not None:
            self.df_mode1['lower_eq'] = (4.76 / (self.df_mode1.iloc[:, 31])) * ((2 * self.df_mode1.iloc[:, 34])
                                                                                + (0.75 * self.df_mode1.iloc[:, 36]))
        if self.df_mode2 is not None:
            self.df_mode2['lower_eq'] = (4.76 / (self.df_mode2.iloc[:, 31])) * ((2 * self.df_mode2.iloc[:, 34])
                                                                                + (0.75 * self.df_mode2.iloc[:, 36]))

    def Qd(self):
        self.df['Qd1_upper'] = None
        self.df['Qd1_lower'] = None
        self.df['Qd2_upper'] = None
        self.df['Qd2_lower'] = None

        self.df['Qd1_upper'] = None
        self.df['Qd1_lower'] = None
        self.df['Qd2_upper'] = None
        self.df['Qd2_lower'] = None

        self.df['Qd1_upper'] = None
        self.df['Qd1_lower'] = None
        self.df['Qd2_upper'] = None
        self.df['Qd2_lower'] = None
        pass


    def Epsilon(self):
    self.df['Epsilontr1'] = None
    self.df['Epsilontr2'] = None

    def Qs(self):
    self.df['Qs'] = None


    def Z(self):
        if self.df_mode0 is not None:
            self.df_mode0['Z'] = 1
        if self.df_mode1 is not None:
            self.df_mode1['Z'] = (10000 * self.df_mode1['Xtr %']) / (
                        (10000 * self.df_mode1['Xtr %']) - (self.df_mode1[' ξtr 1,2 ppmv']))
        if self.df_mode2 is not None:
            if self.df_mode2['Tracer gas type']=='1':
                self.df_mode2['Z'] = 1 + (self.df_mode2['Qd Ar/CO2 upper']*(self.df_mode2[' ξtr 1,2 ppmv'])
                                          pass
             elif self.df_mode2['Tracer gas type']=='2':
                                          pass


