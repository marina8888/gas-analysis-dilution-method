import sys, re, os
from os.path import expanduser
mypydir = expanduser("~") + "/python"
sys.path.append(mypydir)
import nksub



# main
premixout = open('./premix.out', 'r')
nksub.premix_GoDataLine(premixout)
maxHDOT_x = nksub.premix_GetMaxHDOT_X(premixout)
premixout.close()

eqlist = []
nksub.chemkin_GetEquationList(eqlist, './chem.out')

sl_values = [0.0]*len(eqlist)
nksub.premix_ExtractSensitivity('flow_rate')
nksub.premix_GetDataPerReactionFromCKCSV(sl_values, 0.0)

Tm_values = [0.0]*len(eqlist)
Tn_values = [0.0]*len(eqlist)
nksub.premix_ExtractSensitivity('temperature')
nksub.premix_GetDataPerReactionFromCKCSV(Tm_values, maxHDOT_x[1])
nksub.premix_GetDataPerReactionFromCKCSV(Tn_values, 5.05)

h2_values = [0.0]*len(eqlist)
nksub.premix_ExtractSensitivity('H2')
nksub.premix_GetDataPerReactionFromCKCSV(h2_values, 5.0)

fpout = open('./analysisSen.csv', 'w')
fpout.write('Equation, SEN_SL, SEN_T(@maxHDOT), SEN_T(5.05), SEN_H2\n')
for eq, sl, Tm, Tn, h2 in zip(eqlist, sl_values, Tm_values, Tn_values, h2_values):
    fpout.write(eq)
    fpout.write(', ')
    fpout.write('{0:e}'.format(sl))
    fpout.write(', ')
    fpout.write('{0:e}'.format(Tm))
    fpout.write(', ')
    fpout.write('{0:e}'.format(Tn))
    fpout.write(', ')
    fpout.write('{0:e}'.format(h2))
    fpout.write('\n')
fpout.close()








