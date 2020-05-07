import os


#main
cklist = open('./CKSolnList.txt', 'w')
cklist.write('VARIABLE VAR NONE\n')
cklist.write('VARIABLE SEN NONE\n')
cklist.write('VARIABLE ROP NONE\n')
cklist.write('VARIABLE temperature 1 0 0\n')
cklist.write('VARIABLE pressure 1 0 0\n')
cklist.write('VARIABLE net_heat_production_from_gas-phase_reactions 1 0 0\n')
cklist.write('VARIABLE H2 1 0 0\n')
cklist.write('UNIT Pressure (bar)\n')
cklist.write('UNIT HeatProductionRate (kJ/cm3-sec)\n')
cklist.close()
os.system('GetSolution')
os.system('CKSolnTranspose')



