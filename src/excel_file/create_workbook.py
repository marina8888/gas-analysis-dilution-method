from excel_file.classes import Workbook



# call all functions to calculate dilution gas properties, with a workbook object input.
# this function modifies the workbook object so that it can then be saved in .csv format

def create_workbook(instance: Workbook):
    #fill columns with basic initial values
    print('created' + str(instance))
    print(instance.df.columns)
    instance.Qd()
    instance.Epsilon()
    instance.Xitr()
    instance.Z()
    instance.X_gas()

    instance.Qs()
    instance.heat()
    instance.eq()


    #fill uncertainty columns
    instance.X_Xi_gas()
    instance.X_Epsilon_gas()
    instance.X_Q_gas()
    instance.X_x_gas()
    instance.delta_X_gas()
    # concat and print
    instance.concat_df()

