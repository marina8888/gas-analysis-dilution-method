Attribute VB_Name = "Module2"

' ------------------------------------------------------KEY-----------------------------------------------------------------------------------------------------------------
' --------Variables required for calculating mole fractions and uncertainties in an analysed gas containing a dilution gas (with a tracer species, marked as tr):--------

' TracerGasNum classifies tracer gas concentration where 0- no dilution gas; 1 - 1st concentration of dilution gas; 2 - 2ns concentration of dilution gas
' H$cell contains IF formula user should modify to match tracer gas concentrations used in experiment
' Gas 1 and gas 2 values should be assigned correctly based on whether the tracer gas is marked as 0,1 or 2
' H$column must be ordered so that top line contains gas 1 and afterwards it is alternating 1,2,1,2,  etc. This does not apply for when no or only one dilution gas is used (i.e all rows are marked as dilution gas number 2Åj

' --------X_Xi is the corresponding partial derivative term for tracer gas uncertainty using uncertainty equations from appendix:---------
' smallx - moles of target species as measured; Epsilontr - moles of dilution gas as measured
' XLarge - mole fraction of tagret species as measured; XLargetr - mole fraction of dilution gas present in product gas (as combustion product only);
' Xitr - (as above) dilution gas mole fraction introduced to the system;
' Qd - dilution gas flowrate at p0, t0 (as SLM value on flowmeter); Qtr - Qs - sampling gas flowrate (goes through hot MFM but use calculated values);
' Hence Qtotal = Qd + Qs; Qtr = Qd*Xitr;
' Z - dilution ratio (calculated, but 1 if there is no dilution gas, and for TracerGasNum1!=TracerGasNum2, need to use 2 line switching equations to obtain similar results)

'--------------------------------------regarding the terms in the overall uncertainty equation----------------------------------------------------------------------------
' Uncertainty - set constant per flowmeter, taken from manufacturer data; Xitr - dilution gas mole fraction
' Mutliply these terms to find the uncertainty of the tracer gas in the dilution gas 1 or 2 is found e.g Delta_Xi_tr = Xitr1 (or Xitr2) * Uncertainty

' Uncertainty of measuring the tracer gas species by the gas analyser Delta_Epsilon_tr = Rangetr * Uncertainty
'---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Public Function Zfunc() As Double
' This function calculates Z (dilution ratio) and returns it

' 0 = no dilution gas;
If TracerGasNum1 = 0 Then
    Zfunc() = 1
    
' same gas = dilution gas, simple dilution calculation only;
ElseIf TracerGasNum1 = TracerGasNum2 Then
    Zfunc() = Xitr1 / (Xitr1 - Epsilontr1)
    
    ' full dilution method return gas 1 value
ElseIf GasCurrentSelector = 1 Then
    Zfunc() = 1 + (Qd1 * (Epsilontr1 - Epsilontr2) / ((Qd1 * (Xitr1 - Epsilontr1)) - (Qd2 * (Xitr2 - Epsilontr2))))
    
    ' full dilution method return gas 2 value
ElseIf GasBelowSelector = 1 Then
    Zfunc() = 1 + (Qd2 * (Epsilontr1 - Epsilontr2) / ((Qd1 * (Xitr1 - Epsilontr1)) - (Qd2 * (Xitr2 - Epsilontr2))))
    
Else: MsgBox "Error - stuck on z value calcs"

End If

End Function


Public Function Qsfunc() As Double
' This function calculates Qs (sample line flowrate) and returns it

' 0 = no dilution gas;
If TracerGasNum1 = 0 Then
    Qsfunc() = 0
    
' same gas = dilution gas, simple dilution calculation only;
ElseIf TracerGasNum1 = TracerGasNum2 Then
    Qsfunc() = Qd * Xitr1 / (Epsilontr1 - 1)
    
' full dilution method return gas 1 or 2 value (should be same for both)
ElseIf GasCurrentSelector = 1 Or GasBelowSelector = 1 Then
    Qsfunc() = Qd * (((Xitr1 - Xitr2) / (Epsilontr1 - Epsilontr2)) - 1)
    
' full dilution method return gas 2 value
Else: MsgBox "Error - stuck on z value calcs"

End If

End Function


Public Function Xtrfunc() As Double
' This function calculates Xtr (object mole fraction of tracer gas species) and returns it

'if no dilution gas or only 1 dilution gas, tracer gas mole fraction in product gas would not need to be measured
'in this case, treat this cell as if calculating another product gas, i.e Epsilontr1 = smallx1 = largex1 / Z1
If TracerGasNum1 = 0 Or TracerGasNum1 = TracerGasNum2 Then
    Xtrfunc() = Z * Smallx1

' full dilution method return gas 1 or 2 value (should be same for both)
ElseIf GasCurrentSelector = 1 Or GasBelowSelector = 1 Then
    Xtrfunc() = ((Xitr1 * Epsilontr2) - (Xitr2 * Epsilontr1)) / ((Xitr1 - Epsilontr1) - (Xitr2 - Epsilontr2))

End If

End Function

Public Function Largexfunc() As Double
' This function calculates XLarge (object mole fraction of gas species) and returns it

If TracerGasNum1 = 0 Or TracerGasNum1 = TracerGasNum2 Then
    Largexfunc() = Z * Smallx1
    
ElseIf GasCurrentSelector = 1 Then
    Largexfunc() = Z * Smallx1
    
ElseIf GasBelowSelector = 1 Then
    Largexfunc() = Z * Smallx2
    
End If
End Function

Public Function X_Xi_Delta_Xi_tr() As Double
' This function calculates first two terms of XLarge overall uncertainty. Result must be squared before using in the combined uncertainty equation.


' --------------Calculating X_Xi value based on tracer gas type----------

' 0 = no dilution gas;
If TracerGasNum1 = 0 Then
    MsgBox "used case no dilution which is " & X_Xi
    X_Xi_Delta_Xi_tr = 0
    
' same gas = dilution gas, simple dilution calculation only;
ElseIf TracerGasNum1 = TracerGasNum2 Then
    X_Xi = (Abs(-Smallx1 * Epsilontr1 / (Xitr1 - Epsilontr1) ^ 2))
    MsgBox "used case only one dilution which is " & X_Xi & "values are " & Smallx1 & ", " & -Epsilontr1 & ", " & Xitr1 & ". "
    X_Xi_Delta_Xi_tr = Xitr1 * Uncertainty * X_Xi
    
' full dilution method return gas 1 value
ElseIf GasCurrentSelector = 1 Then
    X_Xi = Abs(-(((Qd2 ^ 2) * Smallx1 * (Epsilontr1 - Epsilontr2)) / (((Xitr1 - Epsilontr1) * Qd1) - (Xitr2 - Epsilontr2) * Qd2) ^ 2))
    MsgBox "used gas 1 type which is " & X_X & "values are " & Smallx1 & ", " & -Epsilontr1 & ", " & Xitr1 & ". "
    X_Xi_Delta_Xi_tr = Xitr1 * Uncertainty * X_Xi

' full dilution method return gas 2 value
ElseIf GasBelowSelector = 1 Then
    X_Xi = Abs((Qd1 * Qd2 * Smallx1 * (Epsilontr1 - Epsilontr2)) / (((Xitr1 - Epsilontr1) * Qd1) - (Xitr2 - Epsilontr2) * Qd2) ^ 2)
    MsgBox "used gas 2 type which is " & X_Xi & "values are " & Smallx1 & ", " & -Epsilontr1 & ", " & Xitr1 & ". "
    X_Xi_Delta_Xi_tr = Xitr2 * Uncertainty * X_Xi
    
End If
 
Else
    MsgBox "Error - stuck on uncertainty tracer gas term 1 or 2"

End If
' Multiply uncertainty of tracer gas by partial derivative term:



End Function

Public Function X_Epsilon_Delta_Epsilon_tr() As Double
' This function calculates second two terms of XLarge overall uncertainty. Result must be squared before using in the combined uncertainty equation.


' --------------Calculating X_Epsilon value based on tracer gas type----------
' Check for valid numbers

' 0 = no dilution gas;
If TracerGasNum1 = 0 Then
    MsgBox "used case no dilution which is " & X_Epsilon
    X_Epsilon_Delta_Epsilon_tr() = 0
    
' same gas = dilution gas, simple dilution calculation only;
ElseIf TracerGasNum1 = TracerGasNum2 Then
    X_Epsilon = (Abs(Smallx1 * Xitr1 / (Xitr1 - Epsilontr1) ^ 2))
    MsgBox "used case only one dilution which is " & X_Epsilon & "values are " & Smallx1 & ", " & -Epsilontr1 & ", " & Xitr1 & ". "
    X_Epsilon_Delta_Epsilon_tr() = Xitr1 * Uncertainty * X_Epsilon
    
' full dilution method return gas 1 value
ElseIf GasCurrentSelector = 1 Then
    X_Xi = Smallx1 * (Abs(-(Qd2 ^ 2) * ((Epsilontr1 - Epsilontr2) / (((Xitr1 - Epsilontr1) * Qd1) - (Xitr2 - Epsilontr2) * Qd2) ^ 2)))
    MsgBox "used gas 1 type which is " & X_Epsilon & "values are " & Smallx1 & ", " & -Epsilontr1 & ", " & Xitr1 & ". "
    X_Epsilon_Delta_Epsilon_tr() = Xitr1 * Uncertainty * X_Xi

' full dilution method return gas 2 value
ElseIf GasBelowSelector = 1 Then
    X_Xi = Smallx1 * (Abs(-(Qd2 ^ 2) * ((Epsilontr1 - Epsilontr2) / (((Xitr1 - Epsilontr1) * Qd1) - (Xitr2 - Epsilontr2) * Qd2) ^ 2)))
    MsgBox "used gas 2 type which is " & X_Epsilon & "values are " & Smallx1 & ", " & -Epsilontr1 & ", " & Xitr1 & ". "
    X_Epsilon_Delta_Epsilon_tr() = Xitr2 * Uncertainty * X_Xi
    
End If
 
Else
    MsgBox "Error - stuck on uncertainty tracer gas term 1 or 2"

End If
' Multiply uncertainty of tracer gas by partial derivative term:



End Function

Public Function X_Q_Delta_Qd() As Double
' This function calculates second two terms of XLarge overall uncertainty. Result must be squared before using in the combined uncertainty equation.


' --------------Calculating X_Xi1 value based on tracer gas type----------
' Check for valid numbers
MsgBox "My tracergas values are " & TracerGasNum2 & ", " & TracerGasNum1
If IsNumeric(TracerGasNum1) And IsNumeric(TracerGasNum2) And Not IsEmpty(TracerGasNum1) And Not IsEmpty(TracerGasNum2) Then

' 0 = no dilution gas;
If TracerGasNum1 = 0 Then
    MsgBox "used case no dilution which is " & X_Xi
    X_Epsilon_Delta_Epsilon_tr() = 0
    
' same gas = dilution gas, simple dilution calculation only;
ElseIf TracerGasNum1 = TracerGasNum2 Then
    MsgBox "values are " & Smallx1 & ", " & -Epsilontr1 & ", " & Xitr1 & ". "
    X_Xi = Smallx1 * (Abs(-Epsilontr1 / (Xitr1 - Epsilontr1) ^ 2))
    MsgBox "used case only one dilution which is " & X_Xi
    X_Epsilon_Delta_Epsilon_tr() = Xitr1 * Uncertainty * X_Xi
    
' full dilution method return gas 1 value
ElseIf GasCurrentSelector = 1 Then
    MsgBox "values are " & Smallx1 & ", " & -Epsilontr1 & ", " & Xitr1 & ". "
    X_Xi = Smallx1 * (Abs(-(Qd2 ^ 2) * ((Epsilontr1 - Epsilontr2) / (((Xitr1 - Epsilontr1) * Qd1) - (Xitr2 - Epsilontr2) * Qd2) ^ 2)))
    MsgBox "used gas 1 type which is " & X_Xi
    X_Epsilon_Delta_Epsilon_tr() = Xitr1 * Uncertainty * X_Xi

' full dilution method return gas 2 value
ElseIf GasBelowSelector = 1 Then
    MsgBox "values are " & Smallx1 & ", " & -Epsilontr1 & ", " & Xitr1 & ". "
    X_Xi = Smallx1 * (Abs(-(Qd2 ^ 2) * ((Epsilontr1 - Epsilontr2) / (((Xitr1 - Epsilontr1) * Qd1) - (Xitr2 - Epsilontr2) * Qd2) ^ 2)))
    MsgBox "used gas 2 type which is " & X_Xi
    X_Epsilon_Delta_Epsilon_tr() = Xitr2 * Uncertainty * X_Xi
    
End If
 
Else
    MsgBox "Error - stuck on uncertainty tracer gas term 1 or 2"

End If
' Multiply uncertainty of tracer gas by partial derivative term:



End Function

