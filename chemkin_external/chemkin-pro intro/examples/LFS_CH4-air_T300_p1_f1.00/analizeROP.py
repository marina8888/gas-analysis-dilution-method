import sys, re, os
from os.path import expanduser
mypydir = expanduser("~") + "/python"
sys.path.append(mypydir)
import nksub



# main
eqlist = []
nksub.chemkin_GetEquationList(eqlist, './chem.out')

h2_values = [0.0]*len(eqlist)
nksub.premix_ExtractROP('H2')
nksub.premix_GetDataPerReactionFromCKCSV(h2_values, 5.0)

fpout = open('./analysisROP.csv', 'w')
fpout.write('Equation, ROP_H2\n')
for eq, h2 in zip(eqlist, h2_values):
    fpout.write(eq)
    fpout.write(', ')
    fpout.write('{0:e}'.format(h2))
    fpout.write('\n')
fpout.close()








