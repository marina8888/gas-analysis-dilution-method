
import matplotlib.pyplot as plt
from classes import Workbook
plt.style.use('seaborn-notebook')

def plot_eq_gas(gas, dataframe: Workbook, heat_ratio: str):
    dataframe.df.plot(kind='scatter', x='upper_eq', y='X_' + gas)
    plt.title(heat_ratio + 'Heat Ratio')
    plt.xlabel('equivalence ratio')
    plt.ylabel(gas+' concentration')
    # Turn on the minor TICKS, which are required for the minor GRID
    plt.minorticks_on()
    # Customize the major and minor grids
    plt.grid(which='major', linestyle='-', linewidth='0.5', color='gray')
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

    plt.show()

# def plot_eq_gas_uncert(gas, dataframe: Workbook, heat_ratio: str):
#     dataframe.df.plot(kind='scatter', x='upper_eq', y='X_' + gas)
#     plt.title(heat_ratio + 'Heat Ratio')
#     plt.xlabel('equivalence ratio')
#     plt.ylabel(gas+' concentration')
#     # Turn on the minor TICKS, which are required for the minor GRID
#     plt.minorticks_on()
#     # Customize the major and minor grids
#     plt.grid(which='major', linestyle='-', linewidth='0.5', color='gray')
#     plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
#
#     plt.show()
#     pass
#
# def plot_by_mode(x_data, y_data):
#     pass
#
# def plot_by_mode_uncert(x_data, y_data, uncert_data):
#     pass
#
# def plot_multiple(x_data1, y_data1, x_data2, y_data2, x_data3=0, y_data3=0, x_data4=0, y_data4=0):
#     pass