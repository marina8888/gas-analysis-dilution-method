from excel_file.classes import Workbook, BigWorkbook



#all functions in this file create a new plot, assist with creating workbooks,and are general 'create' fucntions

def create_workbook(instance: Workbook):
    #fill columns with basic initial values
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

