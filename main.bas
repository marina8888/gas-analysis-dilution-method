Attribute VB_Name = "Module2"
Option Explicit

'Subroutine activated by "calculate uncertainty" button on the bottom left of the spreadsheet.
'Subroutine loops through all all rows for which column H has values and pastes the relevant uncertainties into the correct column
'User must select the leftmost, uppermost cell from where the uncertainties selection start (Column BY cell 51 ish, skin coloured section of document)

'------------initialising values for looping and moving cells---------------------
Dim celres As Range
Dim Mode As Integer
Dim increm As Integer 'multiplier to select smallxvalue for the correct gas
Dim r As Integer
Dim coliterator As Integer
Dim GasCurrentSelector() As Long 'Dilution gas type and condition selector
Dim TotalRows As Integer
Dim Counter As Long 'Your counting variable to step through your entire array
Dim Result As Boolean 'Your result variable, will be set to False if something is not equal to 0, otherwise it's default value is True
Dim InletGasNum As Integer 'Constant, number of inlet gases including dilution gas (still counted as +1 when 2 difference concentrations are used)
Dim TodaysDate As Integer 'Used to map datalogger vaues to correct spreadsheet- column 3 should match logger spreadshet
Dim SearchValue, MatchRange As Range
Dim wsnum As Integer 'Worksheet number for datalogger
Dim WorksheetName As Variant
Dim MyArr As Variant

'----------initialising parameters taken available in experiment for dilution gas 1--------
Dim Rangetr1() As Variant
Dim Xitr1() As Variant
Dim Smallx1() As Variant
Dim Rangex1() As Variant
Dim Epsilontr1() As Variant
Dim Qd1() As Variant

'----------initialising parameters taken available in experiment for dilution gas 2--------
Dim Rangetr2() As Variant
Dim Xitr2() As Variant
Dim Smallx2() As Variant
Dim Rangex2() As Variant
Dim Epsilontr2() As Variant
Dim Qd2() As Variant

'-----------------initialising partial derivative terms of the uncertainty-------------------
Dim X_Xi As Double
Dim X_Epsilon As Double
Dim X_Q As Double
Dim X_x As Double

'-------------------------initialising uncertainty product terms----------------------------
Dim X_Xi_Delta_Xi_tr1() As Variant
Dim X_Epsilon_Delta_Epsilon_tr1() As Variant
Dim X_Q_Delta_Qd1() As Variant
Dim X_x_Delta_Smallx1() As Variant
Dim Delta_Largex1() As Variant

Dim X_Xi_Delta_Xi_tr2() As Variant
Dim X_Epsilon_Delta_Epsilon_tr2() As Variant
Dim X_Q_Delta_Qd2() As Variant
Dim X_x_Delta_Smallx2() As Variant
Dim Delta_Largex2() As Variant
            
       
'-------------------------initialising uncertainty constants----------------------------
Dim MFMUncertainty As Single
Dim FTIRUncertainty As Single



Public Sub ArrayVer()

'------------user select starting cell-------------------------------
Dim x As Boolean
On Error Resume Next
Do While Not x
Set celres = Application.InputBox("Select first to start uncertainty calculation (leftmost, uppermost uncertainty cell)", Type:=8)
If celres Is Nothing Then
    MsgBox "Cell not selected!"
    End If
        
Select Case celres.Count
Case Is = 1
x = True

Case Else
MsgBox "Invalid selection - select one cell only"
End Select

Loop


'---------resizing dynamic arrays------------------------------------

TotalRows = FirstEmtpyRow() - 1

ReDim GasCurrentSelector(TotalRows)

ReDim Rangetr1(TotalRows)
ReDim Xitr1(TotalRows)
ReDim Smallx1(TotalRows)
ReDim Rangex1(TotalRows)
ReDim Epsilontr1(TotalRows)
ReDim Qd1(TotalRows)

ReDim Rangetr2(TotalRows)
ReDim Xitr2(TotalRows)
ReDim Smallx2(TotalRows)
ReDim Rangex2(TotalRows)
ReDim Epsilontr2(TotalRows)
ReDim Qd2(TotalRows)

ReDim X_Xi_Delta_Xi_tr1(TotalRows)
ReDim X_Epsilon_Delta_Epsilon_tr1(TotalRows)
ReDim X_Q_Delta_Qd1(TotalRows)
ReDim X_x_Delta_Smallx1(TotalRows)
ReDim Delta_Largex1(TotalRows)

ReDim X_Xi_Delta_Xi_tr2(TotalRows)
ReDim X_Epsilon_Delta_Epsilon_tr2(TotalRows)
ReDim X_Q_Delta_Qd2(TotalRows)
ReDim X_x_Delta_Smallx2(TotalRows)
ReDim Delta_Largex2(TotalRows)
ReDim WorksheetName(TotalRows)

InletGasNum = 5

increm = 0
r = 0
coliterator = 0

MFMUncertainty = 0.02
FTIRUncertainty = 0.02


'-------------------------------------------assigning row values using loop--------------------------------------------------
For r = 0 To TotalRows
    '----------assigning tracer gas 1 and 2 values to define how many dilution gases user is using and selectors to define which row calculations take place-------
    GasCurrentSelector(r) = Cells(celres.Row + r, 8).Value
    TodaysDate = Cells(celres.Row + r, 3).Value
    wsnum = Cells(celres.Row + r, 4).Value
    WorksheetName(r) = "logger_" + CStr(TodaysDate) + "(" + CStr(wsnum) + ")"
Next r

'Select mode
If Application.WorksheetFunction.Sum(GasCurrentSelector) = 0 Then
    Mode = 0

Else: For Counter = 0 To UBound(GasCurrentSelector) 'Loops through your array
    If GasCurrentSelector(Counter) <> 1 Then
        Mode = 2
        Exit For
    Else: Mode = 1
    End If
Next Counter 'Increment counting variable to proceed to the next index within your array
End If



'--------------------------------------------------assigning datalogger values------------------------------------------------
For coliterator = 1 To InletGasNum

    For r = 0 To TotalRows
    If Cells(celres.Row + r, 28).Value > Cells(celres.Row + r + 1, 28).Value + 250 Then
    wsnum = wsnum + 1 'Use next datalogger worksheet
    End If
    ReDim MyArr((Cells(celres.Row, 28).Value - Cells(celres.Row, 29).Value))
        Cells(celres.Row + r, 30 + (2 * coliterator)).Value = UpperLog()
        Cells(celres.Row + r, 31 + (2 * coliterator)).Value = LowerLog()
    Next r

Next coliterator
coliterator = 1

'------------------------------------------------assigning calcs from datalogger values---------------------------------------

For r = 0 To TotalRows
    Cells(celres.Row + r, 10).Value = UpperEq()
    Cells(celres.Row + r, 11).Value = LowerEq()
    Cells(celres.Row + r, 12).Value = UpperE()
    Cells(celres.Row + r, 13).Value = LowerE()
    Cells(celres.Row + r, 14).Value = RoundedE()
    
    
    
    
Next r




'-----------------------------------------------------------gas values--------------------------------------------------------
For r = 0 To TotalRows
    '----------assigning values gas 1------------------------------------
    Xitr1(r) = 10000 * Cells(celres.Row + r, 27).Value
    Rangetr1(r) = Cells(celres.Row + r, 58).Value
    Epsilontr1(r) = Cells(celres.Row + r, 57).Value
    Qd1(r) = Cells(celres.Row + r, 38).Value
    '----------assigning values gas 2 to cells in row below-------------------------------
    Xitr2(r) = 10000 * Cells(celres.Row + r + 1, 27).Value
    Rangetr2(r) = Cells(celres.Row + r + 1, 58).Value
    Epsilontr2(r) = Cells(celres.Row + r + 1, 57).Value
    Qd2(r) = Cells(celres.Row + r + 1, 38).Value
Next r

    

'-------print values to resopective rows (only once) for the rows that remain the same regardless of type of target gas------
'----------Hence print Z, Qs, Xtr (LargeX for the target gas that is also the tracer gas-------------------
For r = 0 To TotalRows
    increm = (coliterator - 1) / 6
    Smallx1(r) = Cells(celres.Row + r, (59 + 2 * increm)).Value 'small x - varies on gas
    Rangex1(r) = Cells(celres.Row + r, (60 + 2 * increm)).Value 'range x - varies on gas
    Smallx2(r) = Cells(celres.Row + r + 1, (59 + 2 * increm)).Value 'small x - varies on gas
    Rangex2(r) = Cells(celres.Row + r + 1, (60 + 2 * increm)).Value 'range x - varies on gas
    Cells(celres.Row + r, 76).Value = Z()
    Cells(celres.Row + r, 75).Value = Qs()
    Cells(celres.Row + r, celres.Column).Value = Xtr()
Next r




Do While (59 + (2 * (coliterator - 1) / 6)) < celres.Column

    '--------final uncertainty calculation which might require both gas 1 and 2 values---------------------------------------------------
    For r = 0 To TotalRows
        Cells(celres.Row + r, celres.Column + coliterator + 0).Value = Largex()
        Cells(celres.Row + r, celres.Column + coliterator + 1).Value = X_Xi_Delta_Xi_tr()
        Cells(celres.Row + r, celres.Column + coliterator + 2).Value = X_Epsilon_Delta_Epsilon_tr()
        Cells(celres.Row + r, celres.Column + coliterator + 3).Value = X_Q_Delta_Qd() 'No idea what Delta_Qd() is - check this
        Cells(celres.Row + r, celres.Column + coliterator + 4).Value = X_x_Delta_Smallx()
    Next r
    
    '--------Once the gas 2 column has also been populated, only then can both gas 1 and 2 uncertainty values can be set---------------------------------------
    For r = 0 To TotalRows
        X_Xi_Delta_Xi_tr1(r) = Cells(celres.Row + r, celres.Column + coliterator + 1).Value
        X_Epsilon_Delta_Epsilon_tr1(r) = Cells(celres.Row + r, celres.Column + coliterator + 2).Value
        X_Q_Delta_Qd1(r) = Cells(celres.Row + r, celres.Column + coliterator + 3).Value
        X_x_Delta_Smallx1(r) = Cells(celres.Row + r, celres.Column + coliterator + 4).Value
        
        X_Xi_Delta_Xi_tr2(r) = Cells(celres.Row + r + 1, celres.Column + coliterator + 1).Value
        X_Epsilon_Delta_Epsilon_tr2(r) = Cells(celres.Row + r + 1, celres.Column + coliterator + 2).Value
        X_Q_Delta_Qd2(r) = Cells(celres.Row + r + 1, celres.Column + coliterator + 3).Value
        X_x_Delta_Smallx2(r) = Cells(celres.Row + r + 1, celres.Column + coliterator + 4).Value
    Next r
    
    For r = 0 To TotalRows
        Cells(celres.Row + r, celres.Column + coliterator + 5).Value = Delta_Largex()
    Next r
    
    '-----------------------recalculate the above 6 parameters for every target gas (where gas parameters repeat every 6 rows)-------------------------------------
    coliterator = coliterator + 6

Loop

MsgBox "I`m finished here!"



End Sub

Public Function FirstEmtpyRow() As Long
r = 0

Do Until IsEmpty(Cells(celres.Row + r, 8))
   r = r + 1
Loop

   FirstEmtpyRow = r

   End Function




' ------------------------------------------------------KEY-----------------------------------------------------------------------------------------------------------------
' --------Variables required for calculating mole fractions and uncertainties in an analysed gas containing a dilution gas (with a tracer species, marked as tr):--------

' TracerGasNum classifies tracer gas concentration where 0- no dilution gas; 1 - 1st concentration of dilution gas; 2 - 2ns concentration of dilution gas
' H$cell contains IF formula user should modify to match tracer gas concentrations used in experiment
' Gas 1 and gas 2 values should be assigned correctly based on whether the tracer gas is marked as 0,1 or 2
' H$column must be ordered so that top line contains gas 1 and afterwards it is alternating 1,2,1,2,  etc. This does not apply for when no or only one dilution gas is used (i.e all rows are marked as dilution gas number 2j

' --------X_Xi is the corresponding partial derivative term for tracer gas uncertainty using uncertainty equations from appendix:---------
' smallx - moles of target species as measured; Epsilontr - moles of dilution gas as measured
' XLarge - mole fraction of tagret species as measured; XLargetr - mole fraction of dilution gas present in product gas (as combustion product only);
' Xitr - (as above) dilution gas mole fraction introduced to the system;
' Qd - dilution gas flowrate at p0, t0 (as SLM value on flowmeter); Qtr - Qs - sampling gas flowrate (goes through hot MFM but use calculated values);
' Hence Qtotal = Qd + Qs; Qtr = Qd*Xitr;
' Z - dilution ratio (calculated, but 1 if there is no dilution gas, and for GasCurrentSelector!=GasBelowSelector, need to use 2 line switching equations to obtain similar results)

'--------------------------------------regarding the terms in the overall uncertainty equation----------------------------------------------------------------------------
' Uncertainty - set constant per flowmeter, taken from manufacturer data. In the experiment this is a constant 2%. Also the FTIR measurement system error is 2%.

'The uncertainty of the tracer gas in the dilution gas                   Delta_Xi_tr = Xitr1 (or Xitr2) * FTIRUncertainty
'Uncertainty of measuring the tracer gas species by the gas analyser     Delta_Epsilon_tr = Rangetr * FTIRUncertainty
'Uncertainty in the volumetric flowrate of the dilution gas              Delta_Qd = Qd * MFMUncertainty
'Uncertainty of measurement of the target species by the gas analyser    Delta_Epsilon_tr = Rangex * FTIRUncertainty

'---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Private Function UpperLog() As Single
'drag values from log file - first find and multiply by mfm factor,  where 0.2 = 5V datalogger measurement

MyArr = Range(WorksheetFunction.Index(Sheets(WorksheetName).Column(8 + coliterator).Value, WorksheetFunction.Match(Cells(celres.Row, 29).Value, Sheets(WorksheetName).Column(1).Value, 0))): WorksheetFunction.Index(Sheets(WorksheetName).Column(8 + coliterator), WorksheetFunction.Match(Cells(celres.Row, 28).Value, Sheets(WorksheetName).Column(1).Value, 0)).Value

UpperLog = WorksheetFunction.Index(celres.Row + r, 30 + (2 * coliterator), WorksheetFunction.Match(ActiveSheet.Cells(celres.Row + r, 2).Value, Columns(1), 0)) * 0.2 * WorksheetFunction.Max(MyArr)

End Function

Private Function LowerLog() As Single
MyArr = Range(WorksheetFunction.Index(Sheets(WorksheetName).Column(8 + coliterator).Value, _
WorksheetFunction.Match(Cells(celres.Row, 29).Value, Sheets(WorksheetName).Column(1).Value, 0))): WorksheetFunction.Index(Sheets(WorksheetName).Column(8 + coliterator), WorksheetFunction.Match(Cells(celres.Row, 28).Value, Sheets(WorksheetName).Column(1).Value, 0)).Value

LowerLog = WorksheetFunction.Index(celres.Row + r, 30 + (2 * coliterator), WorksheetFunction.Match(ActiveSheet.Cells(celres.Row + r, 2).Value, Columns(1), 0)) * 0.2 * WorksheetFunction.Min(MyArr)

End Function

Private Function UpperEq() As Single

End Function

Private Function LowerEq() As Single

End Function

Private Function UpperE() As Single

End Function

Private Function LowerE() As Single

End Function


Private Function RoundedE() As Single

End Function

    
    
    
Private Function Z() As Single


' This tion calculates Z (dilution ratio) and returns it

' 0 = no dilution gas;
If Mode = 0 Then
   Z = 1
   
' same gas = dilution gas, simple dilution calculation only;
ElseIf Mode = 1 Then
   Z = Xitr1(r) / (Xitr1(r) - Epsilontr1(r))
   
   ' full dilution method return gas 1 value
ElseIf Mode = 2 And GasCurrentSelector(r) = 1 Then
   Z = 1 + (Qd1(r) * (Epsilontr1(r) - Epsilontr2(r)) / ((Qd1(r) * (Xitr1(r) - Epsilontr1(r))) - (Qd2(r) * (Xitr2(r) - Epsilontr2(r)))))
   
   ' full dilution method return gas 2 value
ElseIf Mode = 2 And GasCurrentSelector(r) = 2 Then
   Z = 1 + (Qd2(r) * (Epsilontr1(r) - Epsilontr2(r)) / ((Qd1(r) * (Xitr1(r) - Epsilontr1(r))) - (Qd2(r) * (Xitr2(r) - Epsilontr2(r)))))
   
Else: MsgBox "Error - stuck on z value calcs"

End If

End Function


Private Function Qs() As Double

' This tion calculates Qs (sample line flowrate) and returns it

' 0 = no dilution gas;
If Mode = 0 Then
   Qs = 0
   
' same gas = dilution gas, simple dilution calculation only;
ElseIf Mode = 1 Then
   Qs = Qd1(r) * Xitr1(r) / (Epsilontr1(r) - 1)
   
' full dilution method return gas 1 or 2 value (should be same for both)
ElseIf Mode = 2 Then
   Qs = Qd1(r) * (((Xitr1(r) - Xitr2(r)) / (Epsilontr1(r) - Epsilontr2(r))) - 1)
   
Else: MsgBox "Error - stuck on qs values"
   
' full dilution method return gas 2 value
End If

End Function


Private Function Xtr() As Double

' This tion calculates Xtr (object mole fraction of tracer gas species) and returns it

'if no dilution gas or only 1 dilution gas, tracer gas mole fraction in product gas would not need to be measured
'in this case, treat this cell as if calculating another product gas, i.e Epsilontr1 = smallx1 = largex1 / Z1
If Mode = 0 Or Mode = 1 Then
   Xtr = Z() * Smallx1(r)

' full dilution method return gas 1 or 2 value (should be same for both)
ElseIf Mode = 2 Then
   Xtr = ((Xitr1(r) * Epsilontr2(r)) - (Xitr2(r) * Epsilontr1(r))) / ((Xitr1(r) - Epsilontr1(r)) - (Xitr2(r) - Epsilontr2(r)))
   
Else
   MsgBox "Error - stuck on uncertainty xtr term"
   
End If

End Function

Private Function Largex() As Double

' This tion calculates XLarge (object mole fraction of gas species) and returns it

If Mode = 0 Or Mode = 1 Then
   Largex = Z() * Smallx1(r)
   
ElseIf Mode = 2 And GasCurrentSelector(r) = 1 Then
   Largex = Z() * Smallx1(r)
   
ElseIf Mode = 2 And GasCurrentSelector(r) = 2 Then
   Largex = Z() * Smallx2(r)

Else
   MsgBox "Error - stuck on uncertainty largex term"
   
End If
End Function

Private Function X_Xi_Delta_Xi_tr() As Double

' This tion calculates first two terms of XLarge overall uncertainty. Result must be squared before using in the combined uncertainty equation.


' --------------Calculating X_Xi value based on tracer gas type----------

' 0 = no dilution gas;
If Mode = 0 Then
   X_Xi_Delta_Xi_tr = 0
   
' same gas = dilution gas, simple dilution calculation only;
ElseIf Mode = 1 Then
   X_Xi = (Abs(-Smallx1(r) * Epsilontr1(r) / (Xitr1(r) - Epsilontr1(r)) ^ 2))
   X_Xi_Delta_Xi_tr = Xitr1(r) * FTIRUncertainty * X_Xi
   
' full dilution method return gas 1 value
ElseIf Mode = 2 And GasCurrentSelector(r) = 1 Then
   X_Xi_Delta_Xi_tr = Xitr1(r) * FTIRUncertainty * X_Xi

' full dilution method return gas 2 value
ElseIf Mode = 2 And GasCurrentSelector(r) = 2 Then
   X_Xi = Abs((Qd1(r) * Qd2(r) * Smallx1(r) * (Epsilontr1(r) - Epsilontr2(r))) / (((Xitr1(r) - Epsilontr1(r)) * Qd1(r)) - (Xitr2(r) - Epsilontr2(r)) * Qd2(r)) ^ 2)
   X_Xi_Delta_Xi_tr = Xitr2(r) * FTIRUncertainty * X_Xi

Else: MsgBox "Error - stuck on uncertainty Xi term"

End If



End Function

Private Function X_Epsilon_Delta_Epsilon_tr() As Double

' This tion calculates second two terms of XLarge overall uncertainty. Result must be squared before using in the combined uncertainty equation.


' --------------Calculating X_Epsilon value based on tracer gas type----------

' 0 = no dilution gas;
If Mode = 0 Then
   X_Epsilon = 0
   X_Epsilon_Delta_Epsilon_tr = 0
   
' same gas = dilution gas, simple dilution calculation only;
ElseIf Mode = 1 Then
   X_Epsilon = (Abs(Smallx1(r) * Xitr1(r) / (Xitr1(r) - Epsilontr1(r)) ^ 2))
   X_Epsilon_Delta_Epsilon_tr = Xitr1(r) * FTIRUncertainty * X_Epsilon
   
' full dilution method return gas 1 value
ElseIf Mode = 2 And GasCurrentSelector(r) = 1 Then
   X_Epsilon = Abs((Smallx1(r) * Qd1(r) * ((Xitr1(r) - Epsilontr2(r)) * Qd1(r)) - ((Xitr2(r) - Epsilontr2(r)) * Qd2(r))) / (((Xitr1(r) - Epsilontr1(r)) * Qd1(r)) - (Xitr2(r) - Epsilontr2(r)) * Qd2(r)) ^ 2)
   X_Epsilon_Delta_Epsilon_tr = Xitr1(r) * FTIRUncertainty * X_Epsilon

' full dilution method return gas 2 value
ElseIf Mode = 2 And GasCurrentSelector(r) = 2 Then
   X_Epsilon = Abs((Smallx1(r) * Qd1(r) * ((Xitr1(r) - Epsilontr2(r)) * -Qd1(r)) - ((Xitr2(r) - Epsilontr1(r)) * Qd2(r))) / (((Xitr1(r) - Epsilontr1(r)) * Qd1(r)) - (Xitr2(r) - Epsilontr2(r)) * Qd2(r)) ^ 2)
   X_Epsilon_Delta_Epsilon_tr = Xitr2(r) * FTIRUncertainty * X_Epsilon

Else
   MsgBox "Error - stuck on uncertainty epsilon term"

End If

End Function


Private Function X_Q_Delta_Qd() As Double

' This tion calculates second two terms of XLarge overall uncertainty. Result must be squared before using in the combined uncertainty equation.


' --------------Calculating X_Epsilon value based on tracer gas type----------

' 0 = no dilution gas;
If Mode = 0 Then
   X_Q = 0
   X_Q_Delta_Qd = 0
   
' same gas = dilution gas, simple dilution calculation only;
ElseIf Mode = 1 Then
   X_Q = 0
   X_Q_Delta_Qd = 0
   
' full dilution method return gas 1 value
ElseIf Mode = 2 And GasCurrentSelector(r) = 1 Then
   X_Q = Abs((-Smallx1(r) * Qd2(r) * (Epsilontr1(r) - Epsilontr2(r)) * (Xitr2(r) - Epsilontr2(r))) / (((Xitr1(r) - Epsilontr1(r)) * Qd1(r)) - (Xitr2(r) - Epsilontr2(r)) * Qd2(r)) ^ 2)
   X_Q_Delta_Qd = Qd1(r) * MFMUncertainty * X_Q

' full dilution method return gas 2 value
ElseIf Mode = 2 And GasCurrentSelector(r) = 2 Then
   X_Q = Abs((Smallx1(r) * Qd1(r) * (Epsilontr1(r) - Epsilontr2(r)) * (Xitr2(r) - Epsilontr2(r))) / (((Xitr1(r) - Epsilontr1(r)) * Qd1(r)) - (Xitr2(r) - Epsilontr2(r)) * Qd2(r)) ^ 2)
   X_Q_Delta_Qd = Qd2(r) * MFMUncertainty * X_Q

Else
   MsgBox "Error - stuck on uncertainty qd term"

End If

End Function


Private Function X_x_Delta_Smallx() As Double 'still incomplete

' This tion calculates second two terms of XLarge overall uncertainty. Result must be squared before using in the combined uncertainty equation.


' --------------Calculating X_Epsilon value based on tracer gas type----------

' 0 = no dilution gas;
If Mode = 0 Then
   X_x = 1
   X_x_Delta_Smallx = X_x * Rangex1(r) * FTIRUncertainty
   
' same gas = dilution gas, simple dilution calculation only;
ElseIf Mode = 1 Then
   X_x = Xitr1(r) / (Xitr1(r) - Epsilontr1(r))
   X_x_Delta_Smallx = X_x * Rangex1(r) * FTIRUncertainty
   
' full dilution method return gas 1 value
ElseIf Mode = 2 And GasCurrentSelector(r) = 1 Then
   X_x = Abs(1 + ((Qd1(r) * (Epsilontr1(r) - Epsilontr2(r))) / (((Xitr1(r) - Epsilontr1(r)) * Qd1(r)) - (Xitr2(r) - Epsilontr2(r)) * Qd2(r)) ^ 2))
   X_x_Delta_Smallx = X_x * Rangex1(r) * FTIRUncertainty

' full dilution method return gas 2 value
ElseIf Mode = 2 And GasCurrentSelector(r) = 2 Then
   X_x = Abs(1 + ((Qd1(r) * (Epsilontr1(r) - Epsilontr2(r))) / (((Xitr1(r) - Epsilontr1(r)) * Qd1(r)) - (Xitr2(r) - Epsilontr2(r)) * Qd2(r)) ^ 2))
   X_x_Delta_Smallx = X_x * Rangex2(r) * FTIRUncertainty

Else
   MsgBox "Error - stuck on uncertainty deltasmallx term"

End If

End Function

Private Function Delta_Largex() As Double 'still incomplete

' This tion calculates second two terms of XLarge overall uncertainty. Result must be squared before using in the combined uncertainty equation.


' --------------Calculating X_Epsilon value based on tracer gas type----------

' 0 = no dilution gas;
If Mode = 0 Then
    Delta_Largex = 0
    
' same gas = dilution gas, simple dilution calculation only;
ElseIf Mode = 1 Then
    Delta_Largex = Sqr(X_Xi_Delta_Xi_tr1(r) ^ 2 + X_Epsilon_Delta_Epsilon_tr1(r) ^ 2 + X_x_Delta_Smallx1(r) ^ 2)
    
' full dilution method return gas 1 value
ElseIf Mode = 2 And GasCurrentSelector(r) = 1 Then
    Delta_Largex = 0

' full dilution method return gas 2 value
ElseIf Mode = 2 And GasCurrentSelector(r) = 2 Then
    Delta_Largex = Sqr(X_Xi_Delta_Xi_tr1(r) ^ 2 + X_Xi_Delta_Xi_tr2(r) ^ 2 + X_Epsilon_Delta_Epsilon_tr1(r) ^ 2 + X_Epsilon_Delta_Epsilon_tr2(r) ^ 2 + X_Q_Delta_Qd1(r) ^ 2 + X_Q_Delta_Qd2(r) ^ 2 + X_x_Delta_Smallx1(r) ^ 2)
 
Else: MsgBox "Error - stuck on overall uncertainty term"

End If

End Function




