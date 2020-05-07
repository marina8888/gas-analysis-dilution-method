import sys
from os.path import expanduser
mypydir = expanduser("~") + "/python"
sys.path.append(mypydir)
import nksub

#main
summary = nksub.aurora_GetSummary()
sys.stdout.write( '{0:10.4E}'.format(summary[0]) )
