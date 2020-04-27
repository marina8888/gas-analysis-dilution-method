import pandas as pd
import copy


# class workbook imports variables as arrays from excel file given an excel starting row number from which data collection begins
# intialises a list of lists (from a pandas dataframe) and into np arrays that represent each variable
class Workbook():
    def __init__(self, workbook_name, start_row_number: int, gas_list: list):
        self.df = pd.read_excel(workbook_name, sheet_name='Main')
        self.workbook_name = workbook_name
        self.start_row_number = start_row_number
        self.gas_list = gas_list

        # add new cols and prepare dataframe with correct headers:
        self.prepare_df()
        self.init_cols()

        self.df_0 = self.split_df_mode0()
        self.df_1 = self.split_df_mode1()
        self.df_2 = self.split_df_mode2()

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
        # for mode0 and mode1 calculations, use 1 as default, e.g Qd1=Qd and X_Epsilon1=X_Epilson
        self.df['Qd1_upper'] = None
        self.df['Qd1_lower'] = None
        self.df['Qd2_upper'] = None
        self.df['Qd2_lower'] = None
        self.df['Epsilontr1'] = None
        self.df['Epsilontr2'] = None
        self.df['Xitr1'] = None
        self.df['Xitr2'] = None
        self.df['Qs'] = None
        self.df['Z'] = None
        self.df['upper_eq'] = None
        self.df['lower_eq'] = None

        spike_cols = [col for col in self.df.columns if col.startswith('ppmv')]
        for gas, col in zip(self.gas_list, self.df[spike_cols]):
            self.df.rename(columns={'ppmv': 'x_' + gas},inplace=True)
            print(col)
        # for gas, col in zip(self.gas_list, self.df.iteritems()):
        #     # assign through cycling through all columns named 'ppmv' and 'range':
        #     self.df.rename(columns={'ppmv': 'x_' + gas},inplace=True)
                # self.df.rename(columns={'ppmv': 'x_' + gas}, inplace=True)
                # self.df.rename(columns={'range_' + gas}, inplace=True)
            # values per gas
            # self.df['x_'+ gas] = None
            # self.df['X_'+ gas] = None
            # # self.df['range_'+ gas]= None
            # self.df['X_Xi1_'+ gas] = None
            # self.df['X_Xi2_'+ gas] = None
            # self.df['X_Epsilon1_'+ gas] = None
            # self.df['X_Epsilon2_'+ gas] = None
            # self.df['X_Q1_'+ gas] = None
            # self.df['X_Q2_'+ gas] = None
            # self.df['X_x_'+ gas] = None

            #uncertainty term final
            # self.df['delta_X_'+ gas] = None

    # splitting df by tracer gas column into mode0 (no gas) mode 1 and 2
    def split_df_mode0(self):
        self.df_0 = self.df[self.df['Tracer gas type'] == '0']
        return self.df_0

    def split_df_mode1(self):
        # create a new empty dataframe with same columns and number of columns as previous dataframe
        df_1 = pd.DataFrame().reindex_like(self.df).apply(copy.deepcopy)
        df_1 = df_1.iloc[0:0].apply(copy.deepcopy)
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
                    df_1.loc[len(df_1)] = self.df.iloc[row_id - 1]
            last_tgt = this_tgt
        return df_1

    def split_df_mode2(self):
        # create a new empty dataframe with same columns and number of columns as previous dataframe
        df_2 = pd.DataFrame().reindex_like(self.df).apply(copy.deepcopy)
        df_2 = df_2.iloc[0:0].apply(copy.deepcopy)
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
                    df_2.loc[len(df_2)] = self.df.iloc[row_id - 1].apply(copy.deepcopy)
                    df_2.loc[len(df_2)] = self.df.iloc[row_id].apply(copy.deepcopy)
            last_tgt = this_tgt
        return df_2

    def lists_to_array(self, datatype, col_num: int):
        self.df = self.df.T
        self.df = self.df.values.tolist()
        list = (self.df[col_num])
        for i in range(0, len(list)):
            list[i] = datatype(list[i])
        return list

    def concat(self):
        self.df_0 = self.df_0.reset_index(drop=True)
        self.df_1 = self.df_1.reset_index(drop=True)
        self.df_2 = self.df_2.reset_index(drop=True)
        split_dataframes = [self.df_0, self.df_1, self.df_2]
        self.df = pd.concat(split_dataframes)
        self.df = self.df.reset_index(drop=True)

    # below are methods for calculating values in all three dataframes- basic variables for plotting or uncertainty calcs
    def upper_eq(self):
        if self.df_0 is not None:
            self.df_0['upper_eq'] = (4.76 / (self.df_0.iloc[:, 32])) * ((2 * self.df_0.iloc[:, 33])
                                                                        + (0.75 * self.df_0.iloc[:, 35]))
        if self.df_1 is not None:
            self.df_1['upper_eq'] = (4.76 / (self.df_1.iloc[:, 32])) * ((2 * self.df_1.iloc[:, 33])
                                                                        + (0.75 * self.df_1.iloc[:, 35]))
        if self.df_2 is not None:
            self.df_2['upper_eq'] = (4.76 / (self.df_2.iloc[:, 32])) * ((2 * self.df_2.iloc[:, 33])
                                                                        + (0.75 * self.df_2.iloc[:, 35]))

    def lower_eq(self):
        if self.df_0 is not None:
            self.df_0['lower_eq'] = (4.76 / (self.df_0.iloc[:, 31])) * ((2 * self.df_0.iloc[:, 34])
                                                                        + (0.75 * self.df_0.iloc[:, 36]))
        if self.df_1 is not None:
            self.df_1['lower_eq'] = (4.76 / (self.df_1.iloc[:, 31])) * ((2 * self.df_1.iloc[:, 34])
                                                                        + (0.75 * self.df_1.iloc[:, 36]))
        if self.df_2 is not None:
            self.df_2['lower_eq'] = (4.76 / (self.df_2.iloc[:, 31])) * ((2 * self.df_2.iloc[:, 34])
                                                                        + (0.75 * self.df_2.iloc[:, 36]))

    def Qd(self):

        if self.df_0 is not None:
            self.df_0['Qd1_upper'] = self.df_0['Qd Ar/CO2 upper']
            self.df_0['Qd1_lower'] = self.df_0['Qd Ar/CO2 lower']

        if self.df_1 is not None:
            self.df_1['Qd1_upper'] = self.df_1['Qd Ar/CO2 upper']
            self.df_1['Qd1_lower'] = self.df_1['Qd Ar/CO2 lower']

        if self.df_2 is not None:
            self.df_2.loc[self.df_2['Tracer gas type'] == '1', 'Qd1_upper'] = self.df_2['Qd Ar/CO2 upper']
            self.df_2.loc[self.df_2['Tracer gas type'] == '1', 'Qd1_lower'] = self.df_2['Qd Ar/CO2 lower']

        if self.df_2 is not None:
            self.df_2.loc[self.df_2['Tracer gas type'] == '2', 'Qd2_upper'] = self.df_2[
                'Qd Ar/CO2 upper']
            self.df_2.loc[self.df_2['Tracer gas type'] == '2', 'Qd2_lower'] = self.df_2[
                'Qd Ar/CO2 lower']
            self.df_2['Qd1_upper'] = self.df_2['Qd1_upper'].fillna(method='ffill')
            self.df_2['Qd1_lower'] = self.df_2['Qd1_lower'].fillna(method='ffill')
            self.df_2['Qd2_upper'] = self.df_2['Qd2_upper'].fillna(method='backfill')
            self.df_2['Qd2_lower'] = self.df_2['Qd2_lower'].fillna(method='backfill')

    def Epsilon(self):
        if self.df_0 is not None:
            self.df_0['Epsilontr1'] = self.df_0[' ξtr 1,2 ppmv']

        if self.df_1 is not None:
            self.df_1['Epsilontr1'] = self.df_1[' ξtr 1,2 ppmv']

        if self.df_2 is not None:
            self.df_2.loc[self.df_2['Tracer gas type'] == '1', 'Epsilontr1'] = self.df_2[' ξtr 1,2 ppmv']
            self.df_2.loc[self.df_2['Tracer gas type'] == '2', 'Epsilontr2'] = self.df_2[' ξtr 1,2 ppmv']
            self.df_2['Epsilontr1'] = self.df_2['Epsilontr1'].fillna(method='ffill')
            self.df_2['Epsilontr2'] = self.df_2['Epsilontr2'].fillna(method='backfill')

    def Xitr(self):
        if self.df_0 is not None:
            self.df_0['Xitr1'] = 10000 * self.df_0['Xtr %']

        if self.df_1 is not None:
            self.df_1['Xitr1'] = 10000 * self.df_1['Xtr %']

        if self.df_2 is not None:
            self.df_2.loc[self.df_2['Tracer gas type'] == '1', 'Xitr1'] = 10000 * self.df_2['Xtr %']
            self.df_2.loc[self.df_2['Tracer gas type'] == '2', 'Xitr2'] = 10000 * self.df_2['Xtr %']
            self.df_2['Xitr1'] = self.df_2['Xitr1'].fillna(method='ffill')
            self.df_2['Xitr2'] = self.df_2['Xitr2'].fillna(method='backfill')

    def Qs(self):
        if self.df_0 is not None:
            self.df_0['Qs'] = 0

        if self.df_1 is not None:
            self.df_1['Qs'] = self.df_1['Qd1_upper'] * (
                    (self.df_1['Xitr1'] / self.df_1['Epsilontr1']) - 1)

        if self.df_2 is not None:
            self.df_2.loc[self.df_2['Tracer gas type'] == '1', 'Qs'] = self.df_2['Qd1_upper'] * (
            ((self.df_2['Xitr1'] - self.df_2['Xitr2']) / (
            self.df_2['Epsilontr1'] - self.df_2['Epsilontr2'])) - 1)
            self.df_2.loc[self.df_2['Tracer gas type'] == '2', 'Qs'] = self.df_2['Qd2_upper'] * (
            ((self.df_2['Xitr1'] - self.df_2['Xitr2']) / (
            self.df_2['Epsilontr1'] - self.df_2['Epsilontr2'])) - 1)

    def Z(self):
        if self.df_0 is not None:
            self.df_0['Z'] = 1

        if self.df_1 is not None:
            self.df_1['Z'] = self.df_1['Xitr1'] / (self.df_1['Xitr1'] - self.df_1['Epsilontr1'])

        if self.df_2 is not None:
            self.df_2.loc[self.df_2['Tracer gas type'] == '1', 'Z'] = 1 + (((self.df_2['Epsilontr1'] - self.df_2['Epsilontr2'])
            * self.df_2['Qd1_upper'])/ (((self.df_2['Xitr1'] - self.df_2['Epsilontr1'])*self.df_2['Qd1_upper'])-((self.df_2['Xitr2'] -
            self.df_2['Epsilontr2'])*self.df_2['Qd2_upper'])))
            self.df_2.loc[self.df_2['Tracer gas type'] == '2', 'Z'] = 1 + (((self.df_2['Epsilontr1'] - self.df_2['Epsilontr2'])
            * self.df_2['Qd2_upper'])/ (((self.df_2['Xitr1'] - self.df_2['Epsilontr1'])*self.df_2['Qd1_upper'])-((self.df_2['Xitr2'] -
            self.df_2['Epsilontr2'])*self.df_2['Qd2_upper'])))

    def X_gas(self):
        if self.df_0 is not None:
            for gas in self.gas_list:
                self.df_0['X_'+gas] = self.df_0['Z']* self.df_0['x_'+ gas]

        if self.df_1 is not None:
            for gas in self.gas_list:
                self.df_1['X_'+gas] = self.df_1['Z']* self.df_1['x_'+ gas]

        if self.df_2 is not None:
            for gas in self.gas_list:
                self.df_2['X_'+gas] = self.df_2['Z']* self.df_2['x_'+ gas]

    def X_Xi1_gas(self):
        pass

    def X_Epsilon_gas(self):
        pass

    def X_Q_gas(self):
        pass

    def X_x_gas(self):
        pass

    def delta_X_gas(self):
        pass


