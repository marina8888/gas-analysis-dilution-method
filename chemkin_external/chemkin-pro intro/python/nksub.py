import sys, re, os



def error(arg):
    print(arg)
    sys.exit(1)


# get text list of chemical equation from chem.out
# output:
#   eqlist: text list of chemical equation
# input:
#   filename: filename of chem.out
def chemkin_GetEquationList(eqlist, filename):
    chemout = open(filename, 'r')
    while 1:
        line = chemout.readline()
        if line[0:27] == "      REACTIONS CONSIDERED ":
            break
    line = chemout.readline() # blank line

    while 1:
        line = chemout.readline()
        if not line:
            break
        if line[4:5] == ".":
            data = re.split(" +", line)
            eqlist.append(data[2])
    chemout.close()
    return
""" test code 
eqlist = []
nksub.chemkin_GetEquationList(eqlist, './chem.out')
for item in eqlist:
    print( item )
"""

# get text list of species name from chem.out
# output:
#   splist: text line of species name
# input:
#   filename: filename of chem.out
def chemkin_GetSpeciesList(splist, filename):
    chemout = open(filename, 'r')
    while 1:
        line = chemout.readline()
        if line[0:53] == " CONSIDERED              E  E  WEIGHT     LOW    HIGH":
            break
    line = chemout.readline() # blank line

    while 1:
        line = chemout.readline()
        if not line:
            break
        if line[6:7] == ".":
            data = re.split(" +", line)
            splist.append(data[2])
    chemout.close()
    return
""" test code 
splist = []
nksub.chemkin_GetSpeciesList(splist, './chem.out')
for item in splist:
    print( item )
"""

# go to the first data line of solution in premix.out
# fpout.readline() reads the first data line of solution after this subroutine
# input/output:
#   fpout: file object for premix.out
# return:
#   file position in byte
def premix_GoDataLine(fpout):
    fpout.seek(0)
    r = -1
    while 1:
        line = fpout.readline()
        if not line:
            break
        if line[0:95] == "       X(cm)   T(K)            AREA(cm^2)      V(cm/s)         RHO(g/cm^3)     HDOT(cal/s/cm^3)":
            r = fpout.tell()
    fpout.seek(r)
    return r


# go to the data line at the exit position (largest x) in the current data section and get its data line
# this subroutine assumes that fpout is in somewhere of data section
# input/output:
#   fpout: file object for premix.out
# return:
#   data line at the exit position in the current data section
def premix_GetExitDataLine(fpout):
    ret = fpout.readline()
    nums = re.split(" +", ret)
    if len(nums) == 1:
        return ret
    while 1:
        line = fpout.readline()
        nums = re.split(" +", line)
        if len(nums) == 1:
            break
        ret = line
    return ret


# go to the first data line in the next data section from the current data section
# this subroutine assumes that fpout is in somewhere of data section
# input/output:
#   fpout: file object for premix.out
# return:
#   file position in byte
#   0 indicates no next data section
def premix_GoDataLineNextSection(fpout):
    ret = 0
    premix_GetExitDataLine(fpout)
    line = fpout.readline()
    if line[0:30] == "       X(cm)   MOLE FRACTIONS:":
        fpout.readline() # species name
        ret = fpout.tell()
    return ret



# check if there is error in premix.out
# input/output:
#   fpout: file object for premix.out
# return:
#   False if there is error, True if there is not error
def premix_IsFailure(fpout):
    fpout.seek(0)
    r = False
    while 1:
        line = fpout.readline()
        if not line:
            break
        if line[0:36] == "ERROR condition returned from PREMIX":
            r = True
            break
    return r



# get maximum HDOT (cal/s/cm^3) and its x (cm)
# this subroutine is expected to run after premix_GoDataLine or fpout.seek using return value of premix_GoDataLine
# input/output:
#   fpout: file object for premix.out
# return:
#   maximum HDOT (cal/s/cm^3) and its x (cm)
def premix_GetMaxHDOT_X(fpout):
    maxHDOT = 0.0
    x = 1e10
    while 1:
        line = fpout.readline()
        nums = re.split(" +", line)
        if len(nums) == 1:
            break
        hdot = float(nums[7])
        if hdot >= maxHDOT:
            maxHDOT = hdot
            x = float(nums[2])
    return maxHDOT, x
""" test code 
premixout = open('./premix.out', 'r')
nksub.premix_GoDataLine(premixout)
maxHDOT_x = nksub.premix_GetMaxHDOT_X(premixout)
premixout.close()
print(maxHDOT_x)
"""


# get maximum dT/dx (K/cm) and its x (cm)
# this subroutine is expected to run after premix_GoDataLine or fpout.seek using return value of premix_GoDataLine
# input/output:
#   fpout: file object for premix.out
# return:
#   maximum dT/dx (K/cm) and its x (cm)
def premix_GetMaxDTDX_X(fpout):
    maxDTDX = 0.0
    itsX = 1e10
    line = fpout.readline()
    nums = re.split(" +", line)
    prevT = float(nums[3])
    prevX = float(nums[2])
    while 1:
        line = fpout.readline()
        nums = re.split(" +", line)
        if len(nums) == 1:
            break
        T = float(nums[3])
        X = float(nums[2])
        try:
            dtdx = (T-prevT)/(X-prevX)
        except ZeroDivisionError:
            dtdx = 0.
        if dtdx >= maxDTDX:
            maxDTDX = dtdx
            itsX = X
        prevT = T
        prevX = X
    return maxDTDX, itsX
""" test code 
premixout = open('./premix.out', 'r')
nksub.premix_GoDataLine(premixout)
maxDTDX_x = nksub.premix_GetMaxDTDX_X(premixout)
premixout.close()
print(maxDTDX_x)
"""


# extract ROP data for a species and CKSoln.ckcsv is generated by getSolution.bat
# input:
#   name: species name
def premix_ExtractROP(name):
    cklist = open('./CKSolnList.txt', 'w')
    cklist.write('VARIABLE VAR NONE\n')
    cklist.write('VARIABLE SEN NONE\n')
    cklist.write('VARIABLE ROP NONE\n')
    cklist.write('VARIABLE {} 0 0 1\n'.format(name))
    cklist.close()
    os.system('GetSolution')
""" test code 
nksub.premix_ExtractROP('H2')
"""

# extract sensitivity data for a variable and CKSoln.ckcsv is generated by getSolution.bat
# solution data (XMLdata.zip) is expected to contain sensitivity data
# in other word, computation is expected to be successfully done with "ASEN xxx" inputs
# input:
#   name: variable name, which should be species name, "flow_rate" or "temperature"
def premix_ExtractSensitivity(name):
    cklist = open('./CKSolnList.txt', 'w')
    cklist.write('VARIABLE VAR NONE\n')
    cklist.write('VARIABLE SEN NONE\n')
    cklist.write('VARIABLE ROP NONE\n')
    cklist.write('VARIABLE {} 0 1 0\n'.format(name))
    cklist.close()
    os.system('GetSolution')
""" test code 
nksub.premix_ExtractSensitivity('flow_rate')
"""


# get data per a reaction at x (cm) for a variable from CKSoln.ckcsv
# this subroutine is expected to run after premix_ExtractSensitivity or premix_ExtractROP
# output:
#   values: data per a reaction at x (cm), float list for reaction index
# input:
#   x: position x (cm)
def premix_GetDataPerReactionFromCKCSV(values, x):
    ckcsv = open('./CKSoln.ckcsv', 'r')
    line = ckcsv.readline() # 1
    line = ckcsv.readline() # 2
    line = ckcsv.readline() # 3
    line = ckcsv.readline() # 4
    line = ckcsv.readline() # 5
    line = ckcsv.readline() # 6
    line = ckcsv.readline() # 7
    data = re.split(",", line)
    del data[0:2]
    dx_min = 1e10
    xi = 0
    for p in data:
        dx = abs(float(p)-x)
        if dx_min >= dx:
            dx_min = dx
            xi = data.index(p) + 2
    while 1:
        line = ckcsv.readline()
        if not line:
            break
        data = re.split(",", line)
        index = re.split("#", data[0])
        if len(index) == 1:
            continue
        label = int(index[1])-1
        values[label] = float(data[xi])
    ckcsv.close()
    return
"""
eqlist = []
nksub.chemkin_GetEquationList(eqlist, './chem.out')
sl_values = [0.0]*len(eqlist)
nksub.premix_ExtractSensitivity('flow_rate')
nksub.premix_GetDataPerReactionFromCKCSV(sl_values, 0.0)
print(sl_values)
"""



# get summary from premix.out of premix computation
# input:
#   filename: file name of premix.out
# return:
#   [0]: SL in cm/s
#   [1]: dT at inlet boundary in K
#   [2]: T at outlet boundary (Tad) in K
#   [3]: maximum HDOT in cal/s/cm^3
#   [4]: x at maximum HDOT in cm
#   [5]: maximum dT/dx in K/cm
#   [6]: x at maximum dT/dx in cm
#   [7]: delta = Tad/dTdx|max in cm
def premix_GetSummary(filename):
    fpout = open(filename, 'r')
    if ( not premix_IsFailure(fpout) ):
        pos = premix_GoDataLine(fpout)
        line = fpout.readline()
        nums = re.split(" +", line)
        sl = float(nums[5])
        dT = float(nums[3])

        line = fpout.readline()
        nums = re.split(" +", line)
        dT = float(nums[3])-dT

        line = premix_GetExitDataLine(fpout)
        nums = re.split(" +", line)
        Tad = float(nums[3])

        fpout.seek(pos)
        maxHDOT_x = premix_GetMaxHDOT_X(fpout)

        fpout.seek(pos)
        maxDTDX_x = premix_GetMaxDTDX_X(fpout)
        try:
            delta = Tad/maxDTDX_x[0]
        except ZeroDivisionError:
            delta = 0.
    fpout.close()
    return sl, dT, Tad, maxHDOT_x[0], maxHDOT_x[1], maxDTDX_x[0], maxDTDX_x[1], delta
"""
summary = nksub.premix_GetSummary('./premix.out')
print(summary)
"""



# go to the head of the data section of the next time in aurora.out
# aurora_GetVariables() must be called after this subroutine
# input/output:
#   fpout: file object for aurora.out
# return:
#   file position in byte
def aurora_GoNextDataSection(fpout):
    r = -1
    while 1:
        line = fpout.readline()
        if not line:
            break
        if line.find("PSPRNT: Printing of current solution from DDASPK:") != -1:
            r = fpout.tell()
            break
    return r

# get variables from the current data section in aurora.out
# input/output:
#   fpout: file object for aurora.out
# return:
#   dict-type (variable name, variable)
def aurora_GetVariables(fpout):
    while 1:
        line = fpout.readline()
        if not line:
            print 'unexpected end of file'
            exit(1)
        if line.find("DDASPK Transient Solution at Time =") != -1:
            break
    # get time
    vals = {'TIME':float(line[39:51])}
    nBlankLine = 0
    while 1:
        line = fpout.readline()
        if line=='\n':
            nBlankLine += 1
            if nBlankLine==2:
                break
        else:
            nBlankLine = 0
            vals[line[:44].strip()] = float(line[45:57])
    return vals



# get summary from aurora.out of aurora computation
# input:
#   filename: file name of aurora.out
# return:
#   [0] Ignition Delay Time (IDT) in sec based on dp/dt|max
#   [1] dp/dt|max in atm/sec
#   [2] T at endtime in K
def aurora_GetSummary(filename):
    fpout = open(filename, 'r')
    dpdt_max = 0.
    idt = 0.
    aurora_GoNextDataSection(fpout)
    vals = aurora_GetVariables(fpout)
    t_prev = vals['TIME']
    p_prev = vals['PRESSURE']
    while 1:
        r = aurora_GoNextDataSection(fpout)
        if r==-1:
            break
        vals = aurora_GetVariables(fpout)
        t = vals['TIME']
        p = vals['PRESSURE']
        try:
            dpdt = (p-p_prev)/(t-t_prev)
        except ZeroDivisionError:
            dpdt = 0.
        if dpdt > dpdt_max:
            dpdt_max = dpdt
            idt = (t+t_prev)/2.
        t_prev = t
        p_prev = p
    fpout.close()
    return idt, dpdt_max, vals['TEMPERATURE']
"""
summary = nksub.aurora_GetSummary('./aurora.out')
print(summary)
"""




