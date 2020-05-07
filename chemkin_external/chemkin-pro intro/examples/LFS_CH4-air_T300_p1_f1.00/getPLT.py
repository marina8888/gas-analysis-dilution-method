import os.path,glob, sys, re
from os.path import expanduser
mypydir = expanduser("~") + "/python"
sys.path.append(mypydir)
import nksub


#main
splist = []
nksub.chemkin_GetSpeciesList(splist, './chem.out')

fp_out = open('./premix.out', 'r')
fp_plt = open('./profiles.plt', 'w')

#-- write header
fp_plt.write("VARIABLES=\"X(cm)\" \"T(K)\" \"AREA(cm^2)\" \"V(cm/s)\" \"RHO(g/cm^3)\" \"HDOT(cal/s/cm^3)\" \n")
for item in splist:
    fp_plt.write("\"%s\"\n" % item)
fp_plt.write("ZONE T=\"%s\", " % os.getcwd())

#-- get data number
pos = nksub.premix_GoDataLine(fp_out)
line = nksub.premix_GetExitDataLine(fp_out)
nums = re.split(" +", line)
ndata = int(nums[1])
fp_plt.write("I=%d, J=1, K=1, F=POINT\n" % ndata)

#-- write data
for idata in range(ndata):
    isection = 0
    fp_out.seek(pos)
    while 1:
        line = fp_out.readline()
        for i in range(idata):
            line = fp_out.readline()
        if isection==0:
            fp_plt.write(line[4:])
        else:
            fp_plt.write(line[13:])
        isection += 1
        next_pos = nksub.premix_GoDataLineNextSection(fp_out)
        if next_pos==0:
            break

fp_out.close()
fp_plt.close()


