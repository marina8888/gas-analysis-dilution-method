import pandas as pd
import copy
import numpy as np
import math

# class workbook imports variables as arrays from excel_external file given an excel_external starting row number from which data collection begins
# intialises a list of lists (from a pandas dataframe) and into np arrays that represent each variable
class Workbook():
    def __init__(self, workbook_name, start_row_number: int, gas_list: list, gas_list_percent: list):
        self.df = pd.read_excel(workbook_name, sheet_name='Main')
        self.workbook_name = workbook_name
        self.start_row_number = start_row_number
        self.gas_list = gas_list
        self.co2_gas_list = copy.deepcopy(gas_list)
        self.gas_list_percent = gas_list_percent
        self.full_gas_list = self.gas_list + self.gas_list_percent

        self.tr_gas_uncert = 0.02
        self.ftir_uncert = 0.02
        self.mfm_uncert = 0.02

        new_var = 'CO2'
        self.co2_gas_list.insert(0, new_var)

        # add new cols and prepare dataframe with correct headers:
        self.prepare_df()
        self.init_cols()

        # check for duplicate columns before any concat function and print duplicates (as concat on duplicates causes issues):
        dup_cols:pd.Series = (self.df.columns[self.df.columns.duplicated(keep=False)])
        if dup_cols.empty==False:
            raise AssertionError(
                'in instance: ' + self.workbook_name + 'these duplicate columns need renaming: ' + str(
                    dup_cols))

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
        self.df['mean_eq'] = None
        self.df['error_eq'] = None
        self.df['upper_heat'] = None
        self.df['lower_heat'] = None
        self.df['mean_heat'] = None
        self.df['error_heat'] = None


        dups = self.df.columns.get_loc('ppmv')
        for gas, index in zip(self.gas_list, np.where(dups == True)[0].tolist()):
            self.df.columns.values[index] = 'x_' + gas

        dups2 = self.df.columns.get_loc('range')
        for gas, index in zip(self.co2_gas_list, np.where(dups2 == True)[0].tolist()):
            self.df.columns.values[index] = 'range_' + gas

        dups3 = self.df.columns.get_loc('%')
        for gas, index in zip(self.gas_list_percent, np.where(dups3 == True)[0].tolist()):
            self.df.columns.values[index] = 'x_' + gas

        dups4 = self.df.columns.get_loc('range %')
        for gas, index in zip(self.gas_list_percent, np.where(dups4 == True)[0].tolist()):
            self.df.columns.values[index] = 'range_' + gas

        for gas in self.full_gas_list:
            # values per gas
            self.df['X_' + gas] = None
            self.df['X_Xi1_' + gas] = None
            self.df['Delta_Xitr1_' + gas] = None
            self.df['X_Xi2_' + gas] = None
            self.df['Delta_Xitr2_' + gas] = None
            self.df['X_Epsilon1_' + gas] = None
            self.df['Delta_Epsilontr1_' + gas] = None
            self.df['X_Epsilon2_' + gas] = None
            self.df['Delta_Epsilontr2_' + gas] = None
            self.df['X_Q1_' + gas] = None
            self.df['Delta_Qd1_' + gas] = None
            self.df['X_Q2_' + gas] = None
            self.df['Delta_Qd2_' + gas] = None
            self.df['X_x_' + gas] = None
            self.df['delta_x_' + gas] = None

            # uncertainty term final
            self.df['delta_X_' + gas] = None

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
            this_tgt = self.df.iloc[row_id]['Tracer gas type']
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
            this_tgt = self.df.iloc[row_id]['Tracer gas type']
            # leave out the first row for comparison
            if (last_tgt != ''):
                # if the last tgt was 1 and this is 2 then write both rows to the new dataset
                if (this_tgt == '2' and last_tgt == '1'):
                    df_2.loc[len(df_2)] = self.df.iloc[row_id - 1].apply(copy.deepcopy)
                    df_2.loc[len(df_2)] = self.df.iloc[row_id].apply(copy.deepcopy)
            last_tgt = this_tgt
        return df_2

    @staticmethod
    def lists_to_array(dataframe: pd.DataFrame, datatype, col_name):
        col_location = dataframe.columns.get_loc(col_name)
        new_df = dataframe.T
        new_df = new_df.values.tolist()
        list = (new_df[col_location])
        for i in range(0, len(list)):
            list[i] = datatype(list[i])
        return list

    def print_df_uncert(self):
        for gas in self.full_gas_list:
            print(self.df['X_' + gas], self.df['X_Xi1_' + gas], self.df['Delta_Xitr1_' + gas], self.df['X_Xi2_' + gas])
            print(self.df['Delta_Xitr2_' + gas], self.df['X_Epsilon1_' + gas], self.df['Delta_Epsilontr1_' + gas], self.df['X_Epsilon2_' + gas])
            print(self.df['Delta_Epsilontr2_' + gas], self.df['X_Q1_' + gas], self.df['Delta_Qd1_' + gas])
            print(self.df['X_Q2_' + gas], self.df['Delta_Qd2_' + gas], self.df['X_x_' + gas])
            print(self.df['delta_X_' + gas])

    @staticmethod
    def sort_two_lists(x_list: list, y_list: list):
        x_list, y_list = [list(x) for x in zip(*sorted(zip(x_list, y_list), key=lambda pair: pair[0]))]
        return (x_list, y_list)

    def concat_df(self):
        self.df_0 = self.df_0.reset_index(drop=True)
        self.df_1 = self.df_1.reset_index(drop=True)
        self.df_2 = self.df_2.reset_index(drop=True)
        split_dataframes = [self.df_0, self.df_1, self.df_2]
        self.df = pd.concat(split_dataframes)
        self.df = self.df.reset_index(drop=True)

    # below are methods for calculating values in all three dataframes- basic variables for plotting or uncertainty calcs
    def eq(self):
        if self.df_0 is not None:
            self.df_0['upper_eq'] = (4.76 / (self.df_0.iloc[:, 32])) * ((2 * self.df_0.iloc[:, 33])
                                                                        + (0.75 * self.df_0.iloc[:, 35]))
            self.df_0['lower_eq'] = (4.76 / (self.df_0.iloc[:, 31])) * ((2 * self.df_0.iloc[:, 34])
                                                                        + (0.75 * self.df_0.iloc[:, 36]))
            self.df_0['mean_eq'] = (self.df_0['lower_eq'] + self.df_0['upper_eq'])/2
            self.df_0['error_eq'] = (self.df_0['upper_eq'] - self.df_0['lower_eq'])/2

        if self.df_1 is not None:
            self.df_1['upper_eq'] = (4.76 / (self.df_1.iloc[:, 32])) * ((2 * self.df_1.iloc[:, 33])
                                                                        + (0.75 * self.df_1.iloc[:, 35]))
            self.df_1['lower_eq'] = (4.76 / (self.df_1.iloc[:, 31])) * ((2 * self.df_1.iloc[:, 34])
                                                                        + (0.75 * self.df_1.iloc[:, 36]))
            self.df_1['mean_eq'] = (self.df_1['lower_eq'] + self.df_1['upper_eq']) / 2
            self.df_1['error_eq'] = (self.df_1['upper_eq'] - self.df_1['lower_eq'])/2

        if self.df_2 is not None:
            self.df_2['upper_eq'] = (4.76 / (self.df_2.iloc[:, 32])) * ((2 * self.df_2.iloc[:, 33])
                                                                        + (0.75 * self.df_2.iloc[:, 35]))
            self.df_2['lower_eq'] = (4.76 / (self.df_2.iloc[:, 31])) * ((2 * self.df_2.iloc[:, 34])
                                                                        + (0.75 * self.df_2.iloc[:, 36]))
            self.df_2['mean_eq'] = (self.df_2['lower_eq'] + self.df_2['upper_eq']) / 2
            self.df_2['error_eq'] = (self.df_2['upper_eq'] - self.df_2['lower_eq']) / 2

    def heat(self):

        if self.df_0 is not None:
            self.df_0['upper_heat'] = (316.84* self.df_0.iloc[:, 35])/((316.84* self.df_0.iloc[:, 35])+(802.3*self.df_0.iloc[:, 34]))
            self.df_0['lower_heat'] = (316.84* self.df_0.iloc[:, 36])/((316.84* self.df_0.iloc[:, 36])+(802.3*self.df_0.iloc[:, 33]))
            self.df_0['mean_heat'] = (self.df_0['lower_heat'] + self.df_0['upper_heat'])/2
            self.df_0['error_heat'] = (self.df_0['upper_heat'] - self.df_0['lower_heat'])/2

        if self.df_1 is not None:
            self.df_1['upper_heat'] =(316.84* self.df_1.iloc[:, 35])/((316.84* self.df_1.iloc[:, 35])+(802.3*self.df_1.iloc[:, 34]))
            self.df_1['lower_heat'] = (316.84* self.df_1.iloc[:, 36])/((316.84* self.df_1.iloc[:, 36])+(802.3*self.df_1.iloc[:, 33]))
            self.df_1['mean_heat'] = (self.df_1['lower_heat'] + self.df_1['upper_heat']) / 2
            self.df_1['error_heat'] = (self.df_1['upper_heat'] - self.df_1['lower_heat'])/2

        if self.df_2 is not None:
            self.df_2['upper_heat'] = (316.84* self.df_2.iloc[:, 35])/((316.84* self.df_2.iloc[:, 35])+(802.3*self.df_2.iloc[:, 34]))
            self.df_2['lower_heat'] = (316.84* self.df_2.iloc[:, 36])/((316.84* self.df_2.iloc[:, 36])+(802.3*self.df_2.iloc[:, 33]))
            self.df_2['mean_heat'] = (self.df_2['lower_heat'] + self.df_2['upper_heat']) / 2
            self.df_2['error_heat'] = (self.df_2['upper_heat'] - self.df_2['lower_heat']) / 2

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
            self.df_0['Epsilontr1'] = self.df_0['Eps']

        if self.df_1 is not None:
            self.df_1['Epsilontr1'] = self.df_1['Eps']

        if self.df_2 is not None:
            self.df_2.loc[self.df_2['Tracer gas type'] == '1', 'Epsilontr1'] = self.df_2['Eps']
            self.df_2.loc[self.df_2['Tracer gas type'] == '2', 'Epsilontr2'] = self.df_2['Eps']
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
            self.df_2.loc[self.df_2['Tracer gas type'] == '1', 'Z'] = 1 + (
                    ((self.df_2['Epsilontr1'] - self.df_2['Epsilontr2'])
                     * self.df_2['Qd1_upper']) / (
                            ((self.df_2['Xitr1'] - self.df_2['Epsilontr1']) * self.df_2['Qd1_upper']) - (
                            (self.df_2['Xitr2'] -
                             self.df_2['Epsilontr2']) * self.df_2['Qd2_upper'])))
            self.df_2.loc[self.df_2['Tracer gas type'] == '2', 'Z'] = 1 + (
                    ((self.df_2['Epsilontr1'] - self.df_2['Epsilontr2'])
                     * self.df_2['Qd2_upper']) / (
                            ((self.df_2['Xitr1'] - self.df_2['Epsilontr1']) * self.df_2['Qd1_upper']) - (
                            (self.df_2['Xitr2'] -
                             self.df_2['Epsilontr2']) * self.df_2['Qd2_upper'])))

    def X_gas(self):
        if self.df_0 is not None:
            for gas in self.full_gas_list:
                self.df_0['X_' + gas] = self.df_0['Z'] * self.df_0['x_' + gas]

        if self.df_1 is not None:
            for gas in self.full_gas_list:
                self.df_1['X_' + gas] = self.df_1['Z'] * self.df_1['x_' + gas]

        if self.df_2 is not None:
            for gas in self.full_gas_list:
                self.df_2['X_' + gas] = self.df_2['Z'] * self.df_2['x_' + gas]

    def X_Xi_gas(self):
        if self.df_0 is not None:
            for gas in self.full_gas_list:
                self.df_0['X_Xi1_' + gas] = 0
                self.df_0['Delta_Xitr1_' + gas] = self.df_0['Xitr1'] * self.ftir_uncert

        if self.df_1 is not None:
            for gas in self.full_gas_list:
                self.df_1['X_Xi1_' + gas] = abs(-self.df_1['Epsilontr1'] * self.df_1['x_' + gas] / (
                self.df_1['Xitr1'] - self.df_1['Epsilontr1'])**2 )
                self.df_1['Delta_Xitr1_' + gas] = self.df_1['Xitr1'] * self.ftir_uncert

        if self.df_2 is not None:
            for gas in self.full_gas_list:
                self.df_2['Delta_Xitr1_' + gas] = self.df_2['Xitr1'] * self.tr_gas_uncert
                self.df_2['Delta_Xitr2_' + gas] = self.df_2['Xitr2'] * self.tr_gas_uncert

                # setting values for tracer gas 1 values for X_Xi and Delta_Xitr
                self.df_2.loc[self.df_2['Tracer gas type'] == '1', 'X_Xi1_' + gas] = abs((- self.df_2['x_' + gas]
                * (self.df_2['Epsilontr1'] - self.df_2['Epsilontr2'])*(self.df_2['Qd1_upper'])**2)/(((self.df_2['Xitr1']
                -self.df_2['Epsilontr1'])*self.df_2['Qd1_upper'])-((self.df_2['Xitr2'] - self.df_2['Epsilontr2'])*
                self.df_2['Qd2_upper']))**2)

                self.df_2.loc[self.df_2['Tracer gas type'] == '1', 'X_Xi2_' + gas] = abs((self.df_2['x_' + gas]
                * (self.df_2['Epsilontr1'] - self.df_2['Epsilontr2'])*(self.df_2['Qd1_upper']*self.df_2['Qd2_upper']))/\
                (((self.df_2['Xitr1'] - self.df_2['Epsilontr1'])*self.df_2['Qd1_upper'])-((self.df_2['Xitr2']
                - self.df_2['Epsilontr2'])* self.df_2['Qd2_upper']))**2)

                # setting values for tracer gas 2 values for X_Xi and Delta_Xitr
                self.df_2.loc[self.df_2['Tracer gas type'] == '2', 'X_Xi1_' + gas] = abs((- self.df_2['x_' + gas]
                * (self.df_2['Epsilontr1'] - self.df_2['Epsilontr2'])*self.df_2['Qd1_upper']*self.df_2['Qd2_upper'])/
                (((self.df_2['Xitr1'] -self.df_2['Epsilontr1'])*self.df_2['Qd1_upper'])-((self.df_2['Xitr2'] -
                self.df_2['Epsilontr2'])*self.df_2['Qd2_upper']))**2)

                self.df_2.loc[self.df_2['Tracer gas type'] == '2', 'X_Xi2_' + gas] = abs((self.df_2['x_' + gas]
                * (self.df_2['Epsilontr1'] - self.df_2['Epsilontr2'])*(self.df_2['Qd1_upper'])**2)/\
                (((self.df_2['Xitr1'] - self.df_2['Epsilontr1'])*self.df_2['Qd1_upper'])-((self.df_2['Xitr2']
                - self.df_2['Epsilontr2'])* self.df_2['Qd2_upper']))**2)


    def X_Epsilon_gas(self):
        if self.df_0 is not None:
            for gas in self.full_gas_list:
                self.df_0['X_Epsilon1_' + gas] = 0
                self.df_0['Delta_Epsilontr1_' + gas] = self.df_0['range_CO2'] * self.ftir_uncert

        if self.df_1 is not None:
            for gas in self.full_gas_list:
                self.df_1['X_Epsilon1_' + gas] = abs(self.df_1['Xitr1'] * self.df_1['x_' + gas] / (
                self.df_1['Xitr1'] - self.df_1['Epsilontr1'])**2 )
                self.df_1['Delta_Epsilontr1_' + gas] = self.df_1['range_CO2'] * self.ftir_uncert

        if self.df_2 is not None:
            for gas in self.full_gas_list:
                self.df_2['Delta_Epsilontr1_' + gas] = self.df_2['range_CO2']* self.ftir_uncert
                self.df_2['Delta_Epsilontr2_' + gas] = self.df_2['range_CO2']* self.ftir_uncert

                # setting values for tracer gas 1 values for X_Epsilon and Delta_Epsilontr
                self.df_2.loc[self.df_2['Tracer gas type'] == '1', 'X_Epsilon1_' + gas] = \
                abs((self.df_2['x_' + gas] * self.df_2['Qd1_upper']*((self.df_2['Xitr1'] - self.df_2['Epsilontr2']) *
                self.df_2['Qd1_upper']) - ((self.df_2['Xitr2'] - self.df_2['Epsilontr2']) *
                self.df_2['Qd2_upper'])) / (((self.df_2['Xitr1'] - self.df_2['Epsilontr1']) *
                self.df_2['Qd1_upper']) - ((self.df_2['Xitr2'] - self.df_2['Epsilontr2']) *
                self.df_2['Qd2_upper'])) ** 2)

                self.df_2.loc[self.df_2['Tracer gas type'] == '1', 'X_Epsilon2_' + gas] = \
                abs((self.df_2['x_' + gas] * self.df_2['Qd1_upper']*(-(self.df_2['Xitr1'] - self.df_2['Epsilontr1']) *
                self.df_2['Qd1_upper']) - ((self.df_2['Xitr2'] - self.df_2['Epsilontr1']) *
                self.df_2['Qd2_upper'])) / (((self.df_2['Xitr1'] - self.df_2['Epsilontr1']) *
                self.df_2['Qd1_upper']) - ((self.df_2['Xitr2'] - self.df_2['Epsilontr2']) *
                self.df_2['Qd2_upper'])) ** 2)

                # setting values for tracer gas 2 values for X_Epsilon and Delta_Epsilontr

                self.df_2.loc[self.df_2['Tracer gas type'] == '2', 'X_Epsilon1_' + gas] = \
                abs((self.df_2['x_' + gas] * self.df_2['Qd2_upper']*((self.df_2['Xitr1'] - self.df_2['Epsilontr2']) *
                self.df_2['Qd1_upper']) - ((self.df_2['Xitr2'] - self.df_2['Epsilontr2']) *
                self.df_2['Qd2_upper'])) / (((self.df_2['Xitr1'] - self.df_2['Epsilontr1']) *
                self.df_2['Qd1_upper']) - ((self.df_2['Xitr2'] - self.df_2['Epsilontr2']) *
                self.df_2['Qd2_upper'])) ** 2)

                self.df_2.loc[self.df_2['Tracer gas type'] == '2', 'X_Epsilon2_' + gas] = \
                abs((self.df_2['x_' + gas] * self.df_2['Qd2_upper']*(-(self.df_2['Xitr1'] - self.df_2['Epsilontr1']) *
                self.df_2['Qd1_upper']) - ((self.df_2['Xitr2'] - self.df_2['Epsilontr1']) *
                self.df_2['Qd2_upper'])) / (((self.df_2['Xitr1'] - self.df_2['Epsilontr1']) *
                self.df_2['Qd1_upper']) - ((self.df_2['Xitr2'] - self.df_2['Epsilontr2']) *
                self.df_2['Qd2_upper'])) ** 2)



    def X_Q_gas(self):
        if self.df_0 is not None:
            for gas in self.full_gas_list:
                self.df_0['X_Q1_' + gas] = 0
                self.df_0['Delta_Qd1_' + gas] = 0

        if self.df_1 is not None:
            for gas in self.full_gas_list:
                self.df_1['X_Q1_' + gas] = 0
                self.df_1['Delta_Qd1_' + gas] = 0

        if self.df_2 is not None:
            for gas in self.full_gas_list:
                self.df_2['Delta_Qd1_' + gas] = self.df_2['Qd1_upper']* self.mfm_uncert
                self.df_2['Delta_Qd2_' + gas] = self.df_2['Qd2_upper']* self.mfm_uncert

                # setting values for tracer gas 1 values for X_Epsilon and Delta_Epsilontr
                self.df_2.loc[self.df_2['Tracer gas type'] == '1', 'X_Q1_' + gas] = \
                abs((-self.df_2['x_' + gas] * self.df_2['Qd2_upper']*(self.df_2['Epsilontr1'] - self.df_2['Epsilontr2']) *
                (self.df_2['Xitr2'] - self.df_2['Epsilontr2'])) / \
                (((self.df_2['Xitr1'] - self.df_2['Epsilontr1']) * self.df_2['Qd1_upper'])
                - ((self.df_2['Xitr2'] - self.df_2['Epsilontr2']) *
                self.df_2['Qd2_upper'])) ** 2)

                self.df_2.loc[self.df_2['Tracer gas type'] == '1', 'X_Q2_' + gas] = \
                abs((self.df_2['x_' + gas] * self.df_2['Qd1_upper']*(self.df_2['Epsilontr1'] - self.df_2['Epsilontr2']) *
                (self.df_2['Xitr2'] - self.df_2['Epsilontr2'])) / \
                (((self.df_2['Xitr1'] - self.df_2['Epsilontr1']) * self.df_2['Qd1_upper'])
                - ((self.df_2['Xitr2'] - self.df_2['Epsilontr2']) *
                self.df_2['Qd2_upper'])) ** 2)

                # setting values for tracer gas 2 values for X_Epsilon and Delta_Epsilontr
                self.df_2.loc[self.df_2['Tracer gas type'] == '2', 'X_Q1_' + gas] = \
                abs((-self.df_2['x_' + gas] * self.df_2['Qd2_upper']*(self.df_2['Xitr1'] - self.df_2['Epsilontr1']) *
                (self.df_2['Epsilontr1'] - self.df_2['Epsilontr2'])) / \
                (((self.df_2['Xitr1'] - self.df_2['Epsilontr1']) * self.df_2['Qd1_upper'])
                - ((self.df_2['Xitr2'] - self.df_2['Epsilontr2']) *
                self.df_2['Qd2_upper'])) ** 2)

                self.df_2.loc[self.df_2['Tracer gas type'] == '2', 'X_Q2_' + gas] = \
                abs((self.df_2['x_' + gas] * self.df_2['Qd1_upper']*(self.df_2['Epsilontr1'] - self.df_2['Epsilontr2']) *
                (self.df_2['Xitr1'] - self.df_2['Epsilontr1'])) / \
                (((self.df_2['Xitr1'] - self.df_2['Epsilontr1']) * self.df_2['Qd1_upper'])
                - ((self.df_2['Xitr2'] - self.df_2['Epsilontr2']) *
                self.df_2['Qd2_upper'])) ** 2)


    def X_x_gas(self):
        if self.df_0 is not None:
            for gas in self.full_gas_list:
                self.df_0['X_x_' + gas] = 1
                self.df_0['delta_x_' + gas] = self.mfm_uncert* self.df_0['range_' + gas]

        if self.df_1 is not None:
            for gas in self.full_gas_list:
                self.df_1['X_x_' + gas] = abs(self.df_1['Xitr1'] / (
                self.df_1['Xitr1'] - self.df_1['Epsilontr1']))
                self.df_1['delta_x_' + gas] = self.mfm_uncert* self.df_1['range_' + gas]

        if self.df_2 is not None:
            for gas in self.full_gas_list:
                self.df_2['delta_x_' + gas] = self.mfm_uncert* self.df_2['range_' + gas]

                self.df_2.loc[self.df_2['Tracer gas type'] == '1', 'X_x_' + gas] = \
                abs(1+((self.df_2['Qd1_upper']*(self.df_2['Epsilontr1'] - self.df_2['Epsilontr2']))
                /(((self.df_2['Xitr1'] - self.df_2['Epsilontr1']) * self.df_2['Qd1_upper'])
                - ((self.df_2['Xitr2'] - self.df_2['Epsilontr2']) *
                self.df_2['Qd2_upper']))))

                self.df_2.loc[self.df_2['Tracer gas type'] == '2', 'X_x_' + gas] = \
                abs(1+((self.df_2['Qd2_upper']*(self.df_2['Epsilontr1'] - self.df_2['Epsilontr2']))
                /(((self.df_2['Xitr1'] - self.df_2['Epsilontr1']) * self.df_2['Qd1_upper'])
                - ((self.df_2['Xitr2'] - self.df_2['Epsilontr2']) *
                self.df_2['Qd2_upper']))))


    def delta_X_gas(self):
        if self.df_0 is not None:
            for gas in self.full_gas_list:
                self.df_0['delta_X_' + gas] = (((self.df_0['X_Xi1_' + gas]*self.df_0['Delta_Xitr1_' + gas])**2)
                + ((self.df_0['X_Epsilon1_' + gas]*self.df_0['Delta_Epsilontr1_' + gas])**2) +
                ((self.df_0['delta_x_' + gas] * self.df_0['X_x_' + gas])**2))**0.5

        if self.df_1 is not None:
            for gas in self.full_gas_list:
                self.df_1['delta_X_' + gas] = (((self.df_1['X_Xi1_' + gas]*self.df_1['Delta_Xitr1_' + gas])**2)
                + ((self.df_1['X_Epsilon1_' + gas]*self.df_1['Delta_Epsilontr1_' + gas])**2) +
                ((self.df_1['delta_x_' + gas] * self.df_1['X_x_' + gas])**2))**0.5

        if self.df_2 is not None:
            for gas in self.full_gas_list:
                self.df_2['delta_X_' + gas] = ((((self.df_2['X_Xi1_' + gas]*self.df_2['Delta_Xitr1_' + gas])**2)
                + ((self.df_2['X_Xi2_' + gas] * self.df_2['Delta_Xitr2_' + gas])** 2)
                + ((self.df_2['X_Epsilon1_' + gas]*self.df_2['Delta_Epsilontr1_' + gas])**2)
                + ((self.df_2['X_Epsilon2_' + gas]*self.df_2['Delta_Epsilontr2_' + gas])**2)
                + ((self.df_2['X_Q1_' + gas]*self.df_2['Delta_Qd1_' + gas])**2)
                + ((self.df_2['X_Q2_' + gas]*self.df_2['Delta_Qd2_' + gas])**2)
                + ((self.df_2['delta_x_' + gas] * self.df_2['X_x_' + gas])**2))**0.5)

class BigWorkbook():
    def __init__(self, instance_list: [Workbook]):
        self.instance_list=instance_list
        #raise error for any duplicate cols before concat/append functions go crazy due to duplicate cols:

        for instance in self.instance_list:
            dup_cols: pd.Series = (instance.df.columns[instance.df.columns.duplicated(keep=False)])
            if dup_cols.empty==False:
                raise AssertionError(
                    'in : ' + instance.workbook_name + 'these duplicate columns need renaming: ' + str(
                        dup_cols))

        self.df_list = self.concat_instances()
        self.df = self.create_single_df()

    def concat_instances(self):

        #define split dataframes to store dfs from each instance:
        split0=[]
        split1=[]
        split2=[]
        for instance in self.instance_list:
            instance.df_0.reset_index(drop=True)
            split0.append(instance.df_0)
            self.df_0 = pd.concat(split0)
            self.df_0.reset_index(drop=True)

            instance.df_1.reset_index(drop=True)
            split1.append(instance.df_1)
            self.df_1 = pd.concat(split1)
            self.df_1.reset_index(drop=True)

            instance.df_2.reset_index(drop=True)
            split2.append(instance.df_2)
            self.df_2 = pd.concat(split2)
            self.df_2.reset_index(drop=True)
        df_list=[self.df_0, self.df_1, self.df_2]
        return df_list

#create one large df containing df_0, 1 and 2:
    def create_single_df(self):
        df = pd.concat(self.df_list)
        return df

    def round_col(self, value_to_round: str):
        for df in self.df_list:
            # ensure that column is in correct format before rounding:
            df[value_to_round] = df[value_to_round].astype(float)
            df[value_to_round]=df[value_to_round].round(2)

    #takes in a dataframe list (of three dataframes) and splits them into more dataframes by a col parameter
    def split_df_list_by_para(self, parameter_to_split_by: str, legend_list):
        split_list = []
        for l in legend_list:
            split = []
            for df in self.df_list:
                new_df = df[df[parameter_to_split_by] == l]
                split.append(new_df)
            split_list.append(split)
        return split_list
