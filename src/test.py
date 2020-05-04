# before running this code pip install pandas, matplotlib and numpy libraries to your environment:
from classes import Workbook
import graph_funcs
import create_funcs

# run file with -W in script parameters. Warnings related to dataslice copies can be ignored because original dataframe is never used after splitting
import warnings


#this is a test file to check small parts of code:

def main():
    warnings.filterwarnings("ignore")

    test1 = Workbook('/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/plotting_data/60ERESULTSbook16final(0404020).xlsm', 15,
                     ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3'], ['H2', 'O2'])

    test3 = Workbook('/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/plotting_data/40RESULTSbook19final(07042020)new.xlsx',
        21,
        ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3'], ['H2', 'O2'])
    instance_list = [test1, test3]
    for instance in instance_list:
        create_funcs.create_workbook(instance)

    df_list=Workbook.concat_all(instance_list)
    # assign these three dfs to a dictionary containing x and y values:
    d = graph_funcs.assign_xy_from_list('mean_heat', 'error_heat', 'X_' + 'O2', 'delta_X_' + 'O2', df_list)
    print(df_list)
    d = graph_funcs.add_legend_to_df(d, 'mean_eq', df_list)
    d = graph_funcs.round_col(d, 'x0_val')

if __name__ == "__main__":
    main()
