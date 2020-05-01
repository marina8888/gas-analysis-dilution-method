from classes import Workbook

def create_workbook(instance: Workbook):
    #fill columns with basic initial values
    print(instance.df_2)
    instance.Qd()
    instance.Epsilon()
    instance.Xitr()
    instance.Z()
    instance.X_gas()

    print(instance.df_2)
    instance.Qs()
    instance.eq()

    #fill uncertainty columns
    instance.X_Xi_gas()
    instance.X_Epsilon_gas()
    instance.X_Q_gas()
    instance.X_x_gas()
    instance.delta_X_gas()
    print(instance.df_2)

    # concat and print
    instance.concat()
