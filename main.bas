Attribute VB_Name = "Module1"

'Subroutine activated by "calculate uncertainty" button on the bottom left of the spreadsheet.
'Subroutine loops through all all rows for which column H has values and pastes the relevant uncertainties into the correct column
'User must select the leftmost, uppermost cell from where the uncertainties selection start (Column BY cell 51 ish, skin coloured section of document)

'------------initialising values for looping and moving cells---------------------

Dim increm As Integer 'multiplier to select smallxvalue for the correct gas
Dim rowiterator As Integer
Dim coliterator As Integer
Dim GasCurrentSelector As Integer 'Condition select of current row - checks if return value should be for gas type 1 or 2
Dim GasBelowSelector As Integer  'Condition select of row below -chekcs if return value should be for gas type 1 or 2

'----------initialising parameters taken available in experiment for dilution gas 1--------
Dim TracerGasNum1 As Single
Dim Rangetr1 As Integer
Dim Xitr1 As Double
Dim Smallx1 As Double
Dim Epsilontr1 As Double
Dim Qd1 As Single

'----------initialising parameters taken available in experiment for dilution gas 2--------
Dim TracerGasNum2 As Single
Dim Rangetr2 As Integer
Dim Xitr2 As Double
Dim Smallx2 As Double
Dim Epsilontr2 As Double
Dim Qd2 As Single


'-----------------initialising gas parameters to be calculated------------------------------
Dim Z As Double
Dim Qs As Double
Dim Largex As Double

'-----------------initialising values for calculating uncertainty terms in XLarge-------------------
Dim X_Xi As Double
Dim X_Epsilon As Double

Dim Uncertainty As Single


Public Sub Main()

increm = 0
rowiterator = 0
coliterator = 0
GasCurrentSelector = 0
GasBelowSelector = 0

Uncertainty = 0.02

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


 

Do Until WorksheetFunction.CountA(Columns(celres.Column + coliterator)) = 0 _
And WorksheetFunction.CountA(Columns(celres.Column + coliterator + 1)) = 0 _
And WorksheetFunction.CountA(Columns(celres.Column + coliterator + 2)) = 0

MsgBox "My tracergas values are " & TracerGasNum2 & ", " & TracerGasNum1
'-------------------------------------------assigning row values using loop--------------------------------------------------
    Do Until IsEmpty(Cells(celres.Row + rowiterator, 8))
'----------assigning tracer gas 1 and 2 values to define how many dilution gases user is using and selectors to define which row calculations take place-------
TracerGasNum1 = GasCurrentSelector = Cells(celres.Row + rowiterator, 8).Value
TracerGasNum2 = GasBelowSelector = Cells(celres.Row + rowiterator + 1, 8).Value


    If TracerGasNum1 = 0 Or TracerGasNum1 = TracerGasNum2 Or TracerGasNum1 = 1 Then
        '----------assigning values gas 1-------------------------------
        Xitr1 = 10000 * Cells(celres.Row + rowiterator, 27).Value
                Rangetr1
        increm = WorksheetFunction.RoundDown(((celres.Column - 77) / 6), 0)
        Smallx1 = Cells(celres.Row + rowiterator, (59 + 2 * increm)).Value 'small x - varies on gas
        Rangetr2
        Epsilontr1 = Cells(celres.Row + rowiterator, 57).Value
        Qd1 = Cells(celres.Row + rowiterator, 38).Value
        '----------assigning values gas 2 to cells in row below-------------------------------
        Xitr2 = 10000 * Cells(celres.Row + rowiterator + 1, 27).Value
                Rangetr2
        Smallx2 = Cells(celres.Row + rowiterator + 1, (59 + 2 * increm)).Value 'small x - varies on gas
        Rangetr2
        Epsilontr2 = Cells(celres.Row + rowiterator + 1, 57).Value
        Qd2 = Cells(celres.Row + rowiterator + 1, 38).Value


    ElseIf TracerGasNum2 = Gas2Selector = 1 Then
        '----------assigning values gas 1 to cells in row above-------------------------------
        TracerGasNum1 = Cells(celres.Row + rowiterator - 1, 8).Value
                Rangetr1
        Xitr1 = 10000 * Cells(celres.Row + rowiterator - 1, 27).Value
        increm = WorksheetFunction.RoundDown(((celres.Column - 77) / 6), 0)
        Smallx1 = Cells(celres.Row + rowiterator - 1, (59 + 2 * increm)).Value 'small x - varies on gas
        Epsilontr1 = Cells(celres.Row + rowiterator - 1, 57).Value
        Qd1 = Cells(celres.Row + rowiterator - 1, 38).Value
        
        '----------assigning values gas 2-------------------------------
        TracerGasNum2 = Cells(celres.Row + rowiterator, 8).Value
            Rangetr2
        Xitr2 = 10000 * Cells(celres.Row + rowiterator, 27).Value
        Smallx2 = Cells(celres.Row + rowiterator, (59 + 2 * increm)).Value 'small x - varies on gas
        Epsilontr2 = Cells(celres.Row + rowiterator, 57).Value
        Qd2 = Cells(celres.Row + rowiterator, 38).Value

        'Tracer gas values also need reassigning under tracer gas 2 condition

    Else
        MsgBox "Error - cannot assign tracer gas values - check tracer gas type column format"

End If
'-------print values to resopective rows (only once) for the rows that remain the same regardless of type of target gas------
' ----------Hence print Z, Qs, Xtr (LargeX for the target gas that is also the tracer gas-------------------
    If coliterator = 0 Then
        Cells(celres.Row + rowiterator, 76).Value = Zfunc() = Z
        Cells(celres.Row + rowiterator, 75).Value = Qsfunc() = Qs
        Cells(celres.Row + rowiterator, celres.Column).Value = Xtrfunc() = Xtr
    End If
        
        Cells(celres.Row + rowiterator, celres.Column + coliterator + 1).Value = XLargefunc()
        Cells(celres.Row + rowiterator, celres.Column + coliterator + 2).Value = X_Xi_Delta_Xi_tr()
            
            rowiterator = rowiterator + 1
Loop

coliterator = coliterator + 6
rowiterator = 0

Loop


MsgBox "Exited subroutine"



End Sub






