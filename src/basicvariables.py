import pandas as pd


def upper_eq(dataframe: pd.DataFrame):
    dataframe['upper_eq']= (4.76 / (dataframe['Air Lower'])) * (2 * dataframe['CH4upper']) + (0.75 * dataframe['NH3upper'])
    return dataframe


# def smallx(dataframe: pd.DataFrame, gas_num):
#     pass
#
# def smallx1(dataframe: pd.DataFrame, gas_num):
#     pass
#
#
# def smallx2(dataframe: pd.DataFrame, gas_num):
#     pass
#
#
# def rangex(dataframe: pd.DataFrame, gas_num):
#     pass
#
# def rangex1(dataframe: pd.DataFrame, gas_num):
#     pass
#
#
# def rangex2(dataframe: pd.DataFrame, gas_num):
#     pass


def Z(workbook_name):
    pass