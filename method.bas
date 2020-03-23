Attribute VB_Name = "Module1"
'------------initialising variables---------------------
Dim Uncertainty As Single
Dim Multip As Integer

Dim increm As Integer 'multiplier to select smallxvalue for the correct gas
Dim rowiterator As Integer
Dim coliterator As Integer
Dim GasCurrentSelector As Integer 'Condition select of current row - checks if return value should be for gas type 1 or 2
Dim GasBelowSelector As Integer  'Condition select of row below -chekcs if return value should be for gas type 1 or 2
Dim X_Xi As Double

Dim TracerGasNum1 As Single
Dim Xitr1 As Double
Dim Smallx1 As Double
Dim Epsilontr1 As Double
Dim Qd1 As Single

Dim TracerGasNum2 As Single
Dim Xitr2 As Double
Dim Smallx2 As Double
Dim Epsilontr2 As Double
Dim Qd2 As Single

Dim Z As Double

'Subroutine activated by "calculate uncertainty" button on the bottom left of the spreadsheet.
'Subroutine loops through all all rows for which column H has values and pastes the relevant uncertainties into the correct column
'User must select the leftmost, uppermost cell from where the uncertainties selection start (Column BY cell 51 ish, skin coloured section of document)

Public Sub term1and2_Click()

Uncertainty = 0.02
Multip = 10000
rowiterator = 0
coliterator = 0
increm = 0

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


'----------assigning tracer gas 1 and 2 values to enable comparison-------------------------------
TracerGasNum1 = GasCurrentSelector = Cells(celres.Row + rowiterator, 8).Value
TracerGasNum2 = GasBelowSelector = Cells(celres.Row + rowiterator + 1, 8).Value


If TracerGasNum1 = 0 Or TracerGasNum1 = TracerGasNum2 Or TracerGasNum1 = 1 Then
'----------assigning values gas 1-------------------------------
Xitr1 = Cells(celres.Row + rowiterator, 27).Value
increm = WorksheetFunction.RoundDown(((celres.Column - 77) / 6), 0)
Smallx1 = Cells(celres.Row + rowiterator, (59 + 2 * increm)).Value 'small x - varies on gas
Epsilontr1 = Cells(celres.Row + rowiterator, 57).Value
Qd1 = Cells(celres.Row + rowiterator, 38).Value
'----------assigning values gas 2 to cells in row below-------------------------------
Xitr2 = Cells(celres.Row + rowiterator + 1, 27).Value
Smallx2 = Cells(celres.Row + rowiterator + 1, (59 + 2 * increm)).Value 'small x - varies on gas
Epsilontr2 = Cells(celres.Row + rowiterator + 1, 57).Value
Qd2 = Cells(celres.Row + rowiterator + 1, 38).Value


ElseIf TracerGasNum2 = Gas2Selector = 1 Then
'----------assigning values gas 1 to cells in row above-------------------------------
TracerGasNum1 = Cells(celres.Row + rowiterator - 1, 8).Value
Xitr1 = Cells(celres.Row + rowiterator - 1, 27).Value
increm = WorksheetFunction.RoundDown(((celres.Column - 77) / 6), 0)
Smallx1 = Cells(celres.Row + rowiterator - 1, (59 + 2 * increm)).Value 'small x - varies on gas
Epsilontr1 = Cells(celres.Row + rowiterator - 1, 57).Value
Qd1 = Cells(celres.Row + rowiterator - 1, 38).Value

'----------assigning values gas 2-------------------------------
TracerGasNum2 = Cells(celres.Row + rowiterator, 8).Value
Xitr2 = Cells(celres.Row + rowiterator, 27).Value
Smallx2 = Cells(celres.Row + rowiterator, (59 + 2 * increm)).Value 'small x - varies on gas
Epsilontr2 = Cells(celres.Row + rowiterator, 57).Value
Qd2 = Cells(celres.Row + rowiterator, 38).Value

'Tracer gas values also need reassigning under tracer gas 2 condition

Else
    MsgBox "Error - cannot assign tracer gas values - check tracer gas type column format"

End If


 
' ----------Call function to return Z values to cell-------------------
' This function calculates Z values and returns them to column BX (e.g col 76)
' ----------Call function to return Qs values to cell-------------------
' This function calculates Qs values and returns them to column BW (e.g col 75)

MsgBox "Starting Qs values calculation"
MsgBox "Starting Z values calculation"

Do Until IsEmpty(Cells(celres.Row + rowiterator, 8))
    Cells(celres.Row + rowiterator, 76).Value = Zfunc()
    Cells(celres.Row + rowiterator, 75).Value = Qsfunc()
    rowiterator = rowiterator + 1
Loop
 

 ' ----------Call function to reassign uncertainties 1 and 2 values of cell-------------------
 'loop to populate uncertainty section rows for as far down as column H (tracer gas) has a value, for all gas types,in order they are listed in the smallx values section
MsgBox "Starting X_Xi_delta_Xi_tr uncertainty calculation"

Do Until WorksheetFunction.CountA(Columns(celres.Column + coliterator)) = 0 _
And WorksheetFunction.CountA(Columns(celres.Column + coliterator + 1)) = 0 _
And WorksheetFunction.CountA(Columns(celres.Column + coliterator + 2)) = 0

Do Until IsEmpty(Cells(celres.Row + rowiterator, 8))
    Cells(celres.Row + rowiterator, celres.Column + coliterator + 2).Value = X_Xi1_Delta_Xi_tr()
    rowiterator = rowiterator + 1
Loop

coliterator = coliterator + 6
rowiterator = 0

Loop


MsgBox "Exited subroutine"



End Sub






