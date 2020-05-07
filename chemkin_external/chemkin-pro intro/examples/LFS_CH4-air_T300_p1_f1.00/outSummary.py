import sys, re
from os.path import expanduser
mypydir = expanduser("~") + "/python"
sys.path.append(mypydir)
import nksub

#main
summary = nksub.premix_GetSummary('./premix.out')

sys.stdout.write( 'SL = {0:7.4f} (cm/s) with dT {1:7.4f} (K)\n'.format(summary[0], summary[1]) )
sys.stdout.write( 'Tad = {0:7.4f} (K)\n'.format(summary[2]) )
sys.stdout.write( 'maxHDOT = {0:7.4f} (cal/s/cm^3) at {1:7.4f} (cm)\n'.format(summary[3],summary[4]) )
sys.stdout.write( 'maxDTDX = {0:7.4f} (K/cm) at {1:7.4f} (cm)\n'.format(summary[5],summary[6]) )
sys.stdout.write( 'delta(Tad/maxDTDX) = {0:7.4f} (mm)\n'.format(summary[7]*10.) )
