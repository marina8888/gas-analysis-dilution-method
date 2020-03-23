Attribute VB_Name = "Module2"



Public Function X_Xi1_Delta_Xi_tr() As Double
' This function calculates tracer gas (0,1 and/or 2)full uncertainty term. Result must be squared before using in combined uncertainty equation.

' ---------------------------------------------KEY-------------------------------------
' --------Variables for just the uncertainty of tracer gas in the dilution gas:--------
' Uncertainty - from MFM; Multiplier - standard unit conversion from Xitr as %; Xitr - dilution gas mole fraction

' TracerGasNum classifies tracer gases where 0%- 0; 16% - 1; other - 2 in H$cell tracer gas formula so user can modify
' TracerGasNum1 should be current line, and TracerGasNum2 should be on line below.
' Convention is to order tracer gas so that top line is gas 1 and afterwards it is alternating 1,2,1,2,  etc.

' --------X_Xi is the corresponding partial derivative term for tracer gas uncertainty using uncertainty equations from appendix:---------
' smallx - moles of target species as measured; Epsilontr - moles of dilution gas as measured
' largex - mole fraction of tagret species as measured; largextr - mole fraction of dilution gas present in product gas (as combustion product only);
' Xitr - (as above) dilution gas mole fraction introduced to the system;
' Qd - dilution gas flowrate at p0, t0 (as SLM value on flowmeter); Qtr - Qs - sampling gas flowrate (goes through hot MFM but use calculated values);
' Hence Qtotal = Qd + Qs; Qtr = Qd*Xitr;
' Z - dilution ratio (calculated, but 1 if there is no dilution gas, and for TracerGasNum1!=TracerGasNum2, need to use 2 line switching equations to obtain similar results)
'---------------------------------------------------------------------------------------------------------------------------------------------------------------------------




' --------------Calculating X_Xi1 value based on tracer gas type----------
' Check for valid numbers
MsgBox "My tracergas values are " & TracerGasNum2 & ", " & TracerGasNum1
If IsNumeric(TracerGasNum1) And IsNumeric(TracerGasNum2) And Not IsEmpty(TracerGasNum1) And Not IsEmpty(TracerGasNum2) Then

' 0 = no dilution gas;
If TracerGasNum1 = 0 Then
    MsgBox "used case no dilution which is " & X_Xi
    X_Xi1_Delta_Xi_tr = 0
    
' same gas = dilution gas, simple dilution calculation only;
ElseIf TracerGasNum1 = TracerGasNum2 Then
    MsgBox "values are " & Smallx1 & ", " & -Epsilontr1 & ", " & Xitr1 & ". "
    X_Xi = Smallx1 * (Abs(-Epsilontr1 / ((Xitr1 * 10000) - Epsilontr1) ^ 2))
    MsgBox "used case only one dilution which is " & X_Xi
    X_Xi1_Delta_Xi_tr = Xitr1 * Uncertainty * Multip * X_Xi
    
' full dilution method return gas 1 value
ElseIf GasCurrentSelector = 1 Then
    MsgBox "values are " & Smallx1 & ", " & -Epsilontr1 & ", " & Xitr1 & ". "
    X_Xi = Smallx1 * (Abs(-(Qd2 ^ 2) * ((Epsilontr1 - Epsilontr2) / ((((Xitr1 * 10000) - Epsilontr1) * Qd1) - ((Xitr2 * 10000) - Epsilontr2) * Qd2) ^ 2)))
    MsgBox "used gas 1 type which is " & X_Xi
    X_Xi1_Delta_Xi_tr = Xitr1 * Uncertainty * Multip * X_Xi

' full dilution method return gas 2 value
ElseIf GasBelowSelector = 1 Then
    MsgBox "values are " & Smallx1 & ", " & -Epsilontr1 & ", " & Xitr1 & ". "
    X_Xi = Smallx1 * (Abs(-(Qd2 ^ 2) * ((Epsilontr1 - Epsilontr2) / ((((Xitr1 * 10000) - Epsilontr1) * Qd1) - ((Xitr2 * 10000) - Epsilontr2) * Qd2) ^ 2)))
    MsgBox "used gas 2 type which is " & X_Xi
    X_Xi1_Delta_Xi_tr = Xitr2 * Uncertainty * Multip * X_Xi
    
End If
 
Else
    MsgBox "Error - stuck on uncertainty tracer gas term 1 or 2"

End If
' Multiply uncertainty of tracer gas by partial derivative term:



End Function


Public Function Zfunc() As Double

' 0 = no dilution gas;
If TracerGasNum1 = 0 Then
    Zfunc() = 1
    
' same gas = dilution gas, simple dilution calculation only;
ElseIf TracerGasNum1 = TracerGasNum2 Then
    Zfunc() = (10000 * Xitr1) / ((Xitr1 * 10000) - Epsilontr1)
    
    ' full dilution method return gas 1 value
ElseIf GasCurrentSelector = 1 Then
    Zfunc() = 1 + (Qd1 * (Epsilontr1 - Epsilontr2) / ((Qd1 * ((Xitr1 * 1000) - Epsilontr1)) - (Qd2 * ((Xitr2 * 1000) - Epsilontr2))))
    
    ' full dilution method return gas 2 value
ElseIf GasBelowSelector = 1 Then
    Zfunc() = 1 + (Qd2 * (Epsilontr1 - Epsilontr2) / ((Qd1 * ((Xitr1 * 1000) - Epsilontr1)) - (Qd2 * ((Xitr2 * 1000) - Epsilontr2))))
    
Else: MsgBox "Error - stuck on z value calcs"

End Function


Public Function Qsfunc()


' 0 = no dilution gas;
If TracerGasNum1 = 0 Then
    Qsfunc() = 1
    
' same gas = dilution gas, simple dilution calculation only;
ElseIf TracerGasNum1 = TracerGasNum2 Then
    Qsfunc() = (10000 * Xitr1) / ((Xitr1 * 10000) - Epsilontr1)
    
    ' full dilution method return gas 1 value
ElseIf GasCurrentSelector = 1 Then
    Qsfunc() = 1 + (Qd1 * (Epsilontr1 - Epsilontr2) / ((Qd1 * ((Xitr1 * 1000) - Epsilontr1)) - (Qd2 * ((Xitr2 * 1000) - Epsilontr2))))
    
    ' full dilution method return gas 2 value
ElseIf GasBelowSelector = 1 Then
    Qsfunc() = 1 + (Qd2 * (Epsilontr1 - Epsilontr2) / ((Qd1 * ((Xitr1 * 1000) - Epsilontr1)) - (Qd2 * ((Xitr2 * 1000) - Epsilontr2))))
    
Else: MsgBox "Error - stuck on z value calcs"

End Function


Public Function Epsilontrvalue()

End Function


