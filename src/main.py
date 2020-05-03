#before running this code pip install pandas, matplotlib and numpy libraries to your environment:
from classes import Workbook
import graphfuncs
import workbookfuncs

# run file with -W in script parameters. Warnings related to dataslice copies can be ignored because original dataframe is never used after splitting
import warnings

# ensure that all column headers match to code- that they are correct
# however, change the range columns for H2, O2 to 'range %' !

def main():
    warnings.filterwarnings("ignore")

    test1 = Workbook('/Users/marina/Developer/GitHub/gas-analysis-dilution-method/excel/test1.xlsx', 9,
                     ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3'], ['H2', 'O2'])
    test2 = Workbook('/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/plotting_data/60ERESULTSbook16final(0404020).xlsm', 15,
                    ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3'], ['H2', 'O2'])
    test3 = Workbook('/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/plotting_data/40RESULTSbook19final(07042020)new.xlsx', 21,
                    ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3'], ['H2', 'O2'])
    test4 = Workbook('/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/plotting_data/30RESULTSbook20final(08042020).xlsx', 24,
                      ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3'], ['H2', 'O2'])
    test5 = Workbook('/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/plotting_data/20ERESULTSbook21final(09042020).xlsx', 24,
                      ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3'], ['H2', 'O2'])
    test6 = Workbook('/Users/marina/Documents/Work/Tohoku Uni/strain stabiolised product gas/plotting_data/10RESULTSBook22final(11042020).xlsx', 24,
                      ['CO', 'H2O', 'NO', 'NO2', 'N2O', 'NH3'], ['H2', 'O2'])
    workbookfuncs.create_workbook(test1)
    workbookfuncs.create_workbook(test2)
    workbookfuncs.create_workbook(test3)
    workbookfuncs.create_workbook(test4)
    workbookfuncs.create_workbook(test5)
    workbookfuncs.create_workbook(test6)
    # test.df.to_csv('../excel/image_plots/out.csv')
    # instance_list = [test1, test2, test3, test4, test5, test6]
    instance_list =[test1]
    # heat_ratio_list = ['All Heat Ratios', 'All Heat Ratios', 'All Heat Ratios','All Heat Ratios', 'All Heat Ratios', 'All Heat Ratios']
    heat_ratio_list=['All Heat Ratios']
    # colour_list= ['firebrick', 'pink', 'blue', 'green', 'orange', 'black']
    colour_list = ['firebrick']
    # legend_list=['100%', '60%', '40%', '30%', '20%', '10%']
    legend_list = ['100%']
    graphfuncs.create_plot_multiple(test1.full_gas_list, heat_ratio_list,instance_list, legend_list, colour_list)

if __name__ == "__main__":
    main()
