# ________________________________________________________________________________________________________________
#
# DEFINITION OF FUNCTIONS USED IN THE SCRIPT
# ________________________________________________________________________________________________________________


# Function to create a chemkin_external input file
def createInFile(p, t, curv, grad, nadp, npts, ntot, xend, tin, up, ch4, nh3, o2, n2, filestr):
    conditions = open("input.inp", "w")
    conditions.write("!")
    conditions.write("\n! problem type definition")
    conditions.write("\n!")
    conditions.write("\nAXIS   ! Cylindrical Coordinates")
    conditions.write("\nENRG   ! Solve Gas Energy Equation")
    conditions.write("\nMIX   ! Use Mixture-averaged Transport")
    conditions.write("\nPLAT   ! Plateau Profile for Initial Guess")
    conditions.write(
        "\nRSTR /home/RFa/RFa050/chemkin_external/extPrem/Mendiara/" + filestr + "   ! Restart from Previous Solution")
    conditions.write("\nTDIF   ! Use Thermal Diffusion (Soret Effect)")

    conditions.write("\n!")
    conditions.write("\n! physical property")
    conditions.write("\n!")
    conditions.write("\nPRES " + p + "   ! Pressure (atm)")
    conditions.write("\nTINF " + t + "   ! Ambient Temperature (K)")
    conditions.write("\nTMAX 2200.0   ! Maximum Temperature for Initial Profile (K)")
    conditions.write("\n!")
    conditions.write("\n! reactor dimension definition")
    conditions.write("\n!")
    conditions.write("\nCURV " + curv + "   ! Adaptive Grid Control Based On Solution Curvature")
    conditions.write("\nGRAD " + grad + "   ! Adaptive Grid Control Based On Solution Gradient")
    conditions.write("\nNADP " + nadp + "   ! Number of Adaptive Grid Points")
    conditions.write("\nNPTS " + npts + "   ! Number of Uniform Grid Points")
    conditions.write("\nNTOT " + ntot + "   ! Maximum Number of Grid Points Allowed")
    conditions.write("\nXEND " + xend + "   ! Ending Axial Position (cm)")
    conditions.write("\n!")
    conditions.write("\n! output control and other misc. property")
    conditions.write("\n!")
    conditions.write("\nGFAC 1.0   ! Gas Reaction Rate Multiplier")
    conditions.write("\n!")
    conditions.write("\n! physical property")
    conditions.write("\n!")
    conditions.write("\nAINL Fuel_C1_Inlet1 0.0   ! Radial Gradient in Inlet Velocity (1/sec)")
    conditions.write("\nTINL Fuel_C1_Inlet1 " + tin + "   ! Inlet Temperature (K)")
    conditions.write("\nUINL Fuel_C1_Inlet1 " + up + "   ! Inlet Velocity (cm/sec)")
    conditions.write("\n!")
    conditions.write("\n! species property")
    conditions.write("\n!")
    conditions.write("\nREAC Fuel_C1_Inlet1 N2 " + n2 + "   ! Reactant Fraction (mole fraction)")
    conditions.write("\nREAC Fuel_C1_Inlet1 NH3 " + nh3 + "   ! Reactant Fraction (mole fraction)")
    conditions.write("\nREAC Fuel_C1_Inlet1 CH4 " + ch4 + "   ! Reactant Fraction (mole fraction)")
    conditions.write("\nREAC Fuel_C1_Inlet1 O2 " + o2 + "   ! Reactant Fraction (mole fraction)")
    conditions.write("\nINLET Fuel_C1_Inlet1 1   ! Inlet Stream")
    conditions.write("\n!")
    conditions.write("\n! physical property")
    conditions.write("\n!")
    conditions.write("\nAINL Fuel_C1_Inlet2 0.0   ! Radial Gradient in Inlet Velocity (1/sec)")
    conditions.write("\nTINL Fuel_C1_Inlet2 " + tin + "   ! Inlet Temperature (K)")
    conditions.write("\nUINL Fuel_C1_Inlet2 " + up + "   ! Inlet Velocity (cm/sec)")
    conditions.write("\n!")
    conditions.write("\n! species property")
    conditions.write("\n!")
    conditions.write("\nREAC Fuel_C1_Inlet2 N2 " + n2 + "   ! Reactant Fraction (mole fraction)")
    conditions.write("\nREAC Fuel_C1_Inlet2 NH3 " + nh3 + "   ! Reactant Fraction (mole fraction)")
    conditions.write("\nREAC Fuel_C1_Inlet2 CH4 " + ch4 + "   ! Reactant Fraction (mole fraction)")
    conditions.write("\nREAC Fuel_C1_Inlet2 O2 " + o2 + "   ! Reactant Fraction (mole fraction)")
    conditions.write("\nINLET Fuel_C1_Inlet2 1   ! Inlet Stream")
    conditions.write("\nEND")
    conditions.close()
    pass


# ________________________________________________________________________________________________________________

## extract function transfert the data from excel_workbook (solution.out) to dst (solution.txt) and remove useless
## information for calculation process
## Caution open the files before using the function and close them after

def extract(src, dst):
    ## Suppress head, from solution, keep only the final solution first lines (velocity,HRR...)
    ## And put the line in temporary file
    # Open the source file to read its data

    # Preparation for calculation
    text = src.readlines()  # import the lines in a list
    lentxt = len(text)  # number of lines
    print(lentxt)
    i = 0  # initiate line counter
    debut = 0
    fin = 0
    debuthead = 0

    # Start of loople to detect the begining line of extraction
    while i < lentxt - 1:
        i = i + 1
        if text[i].rstrip('\n\r') == ' TWOPNT:  FINAL SOLUTION:':
            debut = i
        if text[i].rstrip('\n\r') == ' TWOPNT:  SUCCESS.  PROBLEM SOLVED.':
            fin = i

    print("begining extraction found")
    print(debut)
    debuthead = debut + 2  # addition of two to arrive just to the header
    l = 0  # initiation of test for the end
    i = debuthead

    # Start of loople to find the end line of extraction
    while l < 1 and i < lentxt - 1:

        dst.write(text[i])  # write line i in destination file
        i = i + 1
        if text[i].rstrip('\n\r') == '':
            l = l + 1
            print("end extraction found")
            print(i)

    if l == 0:
        print("end extraction not found")

    pass


# ___________________________________________________________________________________________________________________________
#
# CALCULATION SCRIPT
# ___________________________________________________________________________________________________________________________


# ___________________________________________________________________________________________________________________________

# Step 2 : Asking the user the initial conditions
## They will be stored in FinalSolution.txt, and will be used to create the input file

print("Please type the calculation conditions")
print("Physical property")
print("Pressure, P [atm] =")
P = input()
print("Temperature unburnt mixture, T [K]=")
T = input()

print("Reactor dimension definition")
print("Grid control on solution curvature, curv =")
CURV = input()
print("Grid control on solution gradient, grad =")
GRAD = input()
print("Number of adaptative grid point, nadp =")
NADP = input()
print("Number of uniform grid point, npts =")
NPTS = input()
print("Maxgrid point, ntot =")
NTOT = input()
print("endposition, xend [cm] =")
XEND = input()

print("Physical property of outlet")
print("Temperature, Tin [K] =")
TIN = input()
print("Minimum velocity for parameter study, Ui_min [cm/s] =")
Ui_min = float(input())
print("Maximum velocity for parameter study, Ui_max [cm/s] =")
Ui_max = float(input())

print("Mixture property of outlet")
print("Mole fraction NH3, nh3 =")
NH3 = input()
print("Mole fraction CH4, ch4 =")
CH4 = input()
print("Mole fraction O2, o2 =")
O2 = input()
print("Mole fraction N2, n2 =")
N2 = input()

finalsol = open("FinalSolution.txt", "a")
finalsol.write("\n! User defined conditions")
finalsol.write("\nPRES " + P + "   ! Pressure (atm)")
finalsol.write("\nTINF " + T + "   ! Ambient Temperature (K)")
finalsol.write("\nCURV " + CURV + "   ! Adaptive Grid Control Based On Solution Curvature")
finalsol.write("\nGRAD " + GRAD + "   ! Adaptive Grid Control Based On Solution Gradient")
finalsol.write("\nNADP " + NADP + "   ! Number of Adaptive Grid Points")
finalsol.write("\nNPTS " + NPTS + "   ! Number of Uniform Grid Points")
finalsol.write("\nNTOT " + NTOT + "   ! Maximum Number of Grid Points Allowed")
finalsol.write("\nXEND " + XEND + "   ! Ending Axial Position (cm)")
finalsol.write("\nTINL Fuel_C1_Inlet1and2 " + TIN + "   ! Inlet Temperature (K)")
finalsol.write("\nUmin " + str(Ui_min) + "   ! Inlet Velocity (cm/sec)")
finalsol.write("\nUmax " + str(Ui_max) + "   ! Inlet Velocity (cm/sec)")
finalsol.write("\nREAC Fuel_C1_Inlet1and2 N2 " + N2 + "   ! Reactant Fraction (mole fraction)")
finalsol.write("\nREAC Fuel_C1_Inlet1and2 CH4 " + CH4 + "   ! Reactant Fraction (mole fraction)")
finalsol.write("\nREAC Fuel_C1_Inlet1and2 NH3 " + NH3 + "   ! Reactant Fraction (mole fraction)")
finalsol.write("\nREAC Fuel_C1_Inlet1and2 O2 " + O2 + "   ! Reactant Fraction (mole fraction)")
finalsol.write("\n_________________________________________________________________________")
finalsol.close()

# ___________________________________________________________________________________________________________________________

# Step 3 : Modify mechanism, create the input data and launch calculation __________________________________________________


strEr = ""
strTp = ""
strU = ""

## "mech.inp" is ready for the calculation

## Preparation to launch extinction computation for arp

import time

temps1 = time.time()

## 3.0 : Initialize the problem
Umin = Ui_min
Umax = Ui_max

## 3.1 : Launch of extinction point research

last = 0  # last is a parameter to detect the end of the computation (extinction found in the desired range)
fail_nb = 0  # fail_nb is used to count the number of caculation which are failing in the U parametric study
flame_nb = 0  # flame_nb is used to count the number of flame - detection of case where Umax is too small and no extinction

from subprocess import Popen

while last < 2:  # While no go to end of calcultion condition is observed (loople until eps_ext is obtained)

    pas = (Umax - Umin) / 5  # increment of velocity on one iteration of U parametric study
    u = Umin  # initialization of u which will vary from Umin to Umax with increment pas
    ite = 1  # initialization of iteration number between Umin and Umax

    if pas <= 0.1:  # Test on the size of U increment
        pas = 0.1
        last = 1  # condition for the last calculation : last=1, calculation is done, then last is set to 2 (see in the following code)

    finalsol = open("FinalSolution.txt", "a")
    finalsol.write("\n! Parametric study calculation")
    finalsol.write("\n! Step is : " + str(pas))
    finalsol.close()

    fail_nb = 0
    flame_nb = 0
    eps_ext = 0

    from shutil import copyfile

    copyfile("data-ext.zip", "input.zip")

    while u <= Umax and last < 2:  # While u of iteration iter is smaller than Umax and that there is no error finishing calculation
        # (loople for parametric study, with a condition out if some error is detected last=2)

        ### 3.1.0 For iteration ite, create input file and launch chemkin_external

        createInFile(P, T, CURV, GRAD, NADP, NPTS, NTOT, XEND, TIN, str(u), CH4, NH3, O2, N2, "input.zip")
        finalsol = open("FinalSolution.txt", "a")
        finalsol.write("\n! U" + str(ite) + " : " + str(u))
        finalsol.close()

        ## the input file "input.inp" is created for u of iteration ite

        time.sleep(2)
        calcul = Popen("job.sh")
        Popen.wait(calcul, timeout=None)

        ## calculation is done, solution.out is produced by chemkin_external

        ### 3.1.1 For iteration ite, check fail/success

        import os.path

        test = os.path.isfile("CKRUN_SUCCESS.txt")
        if test == True:
            fail = 0
        else:
            fail = 1
            fail_nb = fail_nb + 1
            finalsol = open("FinalSolution.txt", "a")
            finalsol.write("\nRun " + str(ite) + " failed.")
            finalsol.close()

        if fail == 0:

            ### 3.1.2 For iteration ite, extract the output data from chemkin_external

            source = open("solution.out", "r")
            destination = open("solution.txt", "w")
            extract(source, destination)
            source.close()
            destination.close()

            data2 = []
            with open("solution.txt") as f:
                for line in f:
                    data2.append([word for word in line.split(" ") if word])
            l2 = len(data2)

            ### 3.1.3 For iteration ite, check flame/no flame (Up_min, Up_max, eps_ext)

            flame = 0
            for i in range(1, l2):
                if int(float(data2[i][7])) > 1300:  # 7 is the column for temperature
                    flame = 1

            if flame == 1:  # IF THERE IS A FLAME :
                flame_nb = flame_nb + 1
                if Umin < u:  # if there is a flame, the value of Umin for the next calculation is set as this iteration u
                    Umin = u

                # store the solution of the calculation
                source = open("solution.out", "r")
                destination = open("solution-flame.txt", "w")
                copyfile("XMLdata.zip", "data-ext.zip")
                extract(source, destination)
                source.close()
                destination.close()

                ### 3.1.4 For iteration ite, calculation of stretch rate

                l_mid = int(l2 / 2) + 2  # Middle line corresponding to stagnation plane

                z_maxHRR = 0  # Flame position as max HRR peak
                HRR = 0
                l_maxHRR = 0

                for j in range(1, l_mid):
                    if HRR < float(data2[j][9]):
                        HRR = float(data2[j][9])
                        z_maxHRR = float(data2[j][1])
                        l_maxHRR = j

                ## Temperature calculation
                temp = 0

                for j in range(1, l2):
                    if temp < float(data2[j][7]):
                        temp = float(data2[j][7])

                ## Gradient velocity calculation

                u1 = 0
                u2 = 0
                z1 = 0
                z2 = 0
                grad = 0
                gradmax = 0
                eps = 0
                k = 1

                while k <= l_maxHRR and grad <= 0:
                    u1 = float(data2[k][3])
                    u2 = float(data2[k + 1][3])
                    z1 = float(data2[k][1])
                    z2 = float(data2[k + 1][1])
                    if z2 - z1 == 0:
                        grad = grad
                    else:
                        grad = (u2 - u1) / (z2 - z1)
                    k = k + 1
                    if grad < gradmax:
                        gradmax = grad

                eps = -gradmax
                if eps_ext < eps:
                    eps_ext = eps

                Tkext = open("T-kext.txt", "a")
                Tkext.write("\n" + str(temp) + "   " + str(eps))
                Tkext.close()



            else:  # IF THERE IS NO FLAME :
                Umax = u

                if Umin == Umax:
                    print("Ui_min is too high, flame didn't occured")
                    last = 2
                    strEr = strEr + "   Fail"
                    strU = strU + "   Fail"
                    strTp = strTp + "   Fail"

                else:
                    if last == 0:
                        # launch new parametric study
                        print("launch iteration again")
                        print("Ui_min is now :" + str(Umin))
                        print("Ui_max is now :" + str(Umax))
                        finalsol = open("FinalSolution.txt", "a")
                        finalsol.write(
                            "\nLaunch new parametric study with Umin : " + str(Umin) + " and Umax : " + str(Umax))
                        finalsol.close()
                    else:

                        # if last = 1 calculation finished go to end
                        last = 2
                        print("finished calculation")
                        print("Uext = " + str(Umin))
                        print("eps_ext = " + str(eps_ext))
                        finalsol = open("FinalSolution.txt", "a")
                        finalsol.write("\nUext = " + str(Umin))
                        finalsol.write("\neps_ext = " + str(eps_ext))
                        finalsol.close()
                        strEr = strEr + "   " + str(eps_ext)
                        strU = strU + "   " + str(Umin)

        u = u + pas
        u = round(u, 1)
        ite = ite + 1

    if fail_nb == ite - 1:
        print("All calculations failed, please change the initial conditions")
        finalsol = open("FinalSolution.txt", "a")
        finalsol.write("\nAll calculations failed, please change the initial conditions")
        finalsol.close()
        last = 2
        strEr = strEr + "   Fail"
        strU = strU + "   Fail"
        # end of calculation
    else:
        if flame_nb == ite - 1:
            print("Ui_max is to small => extinction didn't occured")
            finalsol = open("FinalSolution.txt", "a")
            finalsol.write("\nUi_max is to small => extinction didn't occured")
            finalsol.close()
            last = 2
            strEr = strEr + "   Fail"
            strU = strU + "   Fail"

    finalsol = open("FinalSolution.txt", "a")
    finalsol.write("\n_________________________________________________________________________")
    finalsol.close()

temps2 = time.time()
dtemps = temps2 - temps1
finalsol = open("FinalSolution.txt", "a")
finalsol.write("\n Calculation time : " + str(dtemps))
finalsol.close()
strTp = strTp + "   " + str(dtemps)

# stocker la valeur epsij

biblieps = open("epsij.txt", "a")
biblieps.write("\n" + strEr)
biblieps.close()
caltime = open("CalcTime.txt", "a")
caltime.write("\n" + strTp)
caltime.close()
bibliu = open("uextij.txt", "a")
bibliu.write("\n" + strU)
bibliu.close()
