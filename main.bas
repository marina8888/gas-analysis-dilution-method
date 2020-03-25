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
Dim Rangex1 As Double
Dim Epsilontr1 As Double
Dim Qd1 As Single

'----------initialising parameters taken available in experiment for dilution gas 2--------
Dim TracerGasNum2 As Single
Dim Rangetr2 As Integer
Dim Xitr2 As Double
Dim Smallx2 As Double
Dim Rangex2 As Double
Dim Epsilontr2 As Double
Dim Qd2 As Single


'-----------------initialising gas parameters to be calculated------------------------------
Dim Z As Double
Dim Qs As Double
Dim Largex As Double

'-----------------initialising partial derivative terms of the uncertainty-------------------
Dim X_Xi As Double
Dim X_Epsilon As Double
Dim X_Q As Double
Dim X_x As Double

Dim MFMUncertainty As Single
Dim FTIRUncertainty As Single



Public Sub Main()

increm = 0
rowiterator = 0
coliterator = 2
GasCurrentSelector = 0
GasBelowSelector = 0

MFMUncertainty = 0.02
FTIRUncertainty = 0.02

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


 

Do Until (57 + (2 * coliterator)) > celres.Column

MsgBox "My tracergas values are " & TracerGasNum2 & ", " & TracerGasNum1
'-------------------------------------------assigning row values using loop--------------------------------------------------
    Do Until IsEmpty(Cells(celres.Row + rowiterator, 8))
        '----------assigning tracer gas 1 and 2 values to define how many dilution gases user is using and selectors to define which row calculations take place-------
        TracerGasNum1 = Cells(celres.Row + rowiterator, 8).Value
        GasCurrentSelector = Cells(celres.Row + rowiterator, 8).Value
        TracerGasNum2 = Cells(celres.Row + rowiterator + 1, 8).Value
        GasBelowSelector = Cells(celres.Row + rowiterator + 1, 8).Value

        If TracerGasNum1 = 0 Or TracerGasNum1 = TracerGasNum2 Or TracerGasNum1 = 1 Then
            '----------assigning values gas 1-------------------------------
            Xitr1 = 10000 * Cells(celres.Row + rowiterator, 27).Value
            Rangetr1 = Cells(celres.Row + rowiterator, 58).Value
            increm = (coliterator - 2) / 6
            Smallx1 = Cells(celres.Row + rowiterator, (59 + 2 * increm)).Value 'small x - varies on gas
            Rangex1 = Cells(celres.Row + rowiterator, (60 + 2 * increm)).Value 'range x - varies on gas
            Epsilontr1 = Cells(celres.Row + rowiterator, 57).Value
            Qd1 = Cells(celres.Row + rowiterator, 38).Value
            '----------assigning values gas 2 to cells in row below-------------------------------
            Xitr2 = 10000 * Cells(celres.Row + rowiterator + 1, 27).Value
            Rangetr2 = Cells(celres.Row + rowiterator + 1, 58).Value
            Smallx2 = Cells(celres.Row + rowiterator + 1, (59 + 2 * increm)).Value 'small x - varies on gas
            Rangex2 = Cells(celres.Row + rowiterator + 1, (60 + 2 * increm)).Value 'range x - varies on gas
            Epsilontr2 = Cells(celres.Row + rowiterator + 1, 57).Value
            Qd2 = Cells(celres.Row + rowiterator + 1, 38).Value


        ElseIf TracerGasNum2 = 1 Then
            '----------assigning values gas 1 to cells in row above-------------------------------
            TracerGasNum1 = Cells(celres.Row + rowiterator - 1, 8).Value
            Rangetr1 = Cells(celres.Row + rowiterator - 1, 58).Value
            Xitr1 = 10000 * Cells(celres.Row + rowiterator - 1, 27).Value
            increm = (coliterator - 2) / 6
            Smallx1 = Cells(celres.Row + rowiterator - 1, (59 + 2 * increm)).Value 'small x - varies on gas
            Rangex1 = Cells(celres.Row + rowiterator - 1, (60 + 2 * increm)).Value 'range x - varies on gas
            Epsilontr1 = Cells(celres.Row + rowiterator - 1, 57).Value
            Qd1 = Cells(celres.Row + rowiterator - 1, 38).Value
            
            '----------assigning values gas 2-------------------------------
            TracerGasNum2 = Cells(celres.Row + rowiterator, 8).Value
            Rangetr2 = Cells(celres.Row + rowiterator, 58).Value
            Xitr2 = 10000 * Cells(celres.Row + rowiterator, 27).Value
            Smallx2 = Cells(celres.Row + rowiterator, (59 + 2 * increm)).Value 'small x - varies on gas
            Rangex2 = Cells(celres.Row + rowiterator, (60 + 2 * increm)).Value 'range x - varies on gas
            Epsilontr2 = Cells(celres.Row + rowiterator, 57).Value
            Qd2 = Cells(celres.Row + rowiterator, 38).Value

        'Tracer gas values also need reassigning under tracer gas 2 condition

        Else
            MsgBox "Error - cannot assign tracer gas values - check tracer gas type column format"
            
        End If
    
    
        '-------print values to resopective rows (only once) for the rows that remain the same regardless of type of target gas------
        '----------Hence print Z, Qs, Xtr (LargeX for the target gas that is also the tracer gas-------------------
        If coliterator = 1 Then
            Cells(celres.Row + rowiterator, 76).Value = Zfunc()
            Z = Cells(celres.Row + rowiterator, 76).Value
            Cells(celres.Row + rowiterator, 75).Value = Qsfunc()
            Qs = Cells(celres.Row + rowiterator, 75).Value
            Cells(celres.Row + rowiterator, celres.Column).Value = Xtrfunc()
            Xtr = Cells(celres.Row + rowiterator, celres.Column).Value
            
        End If
            
            Cells(celres.Row + rowiterator, celres.Column + coliterator + 0).Value = Largexfunc()
            Cells(celres.Row + rowiterator, celres.Column + coliterator + 1).Value = X_Xi_Delta_Xi_tr()
            Cells(celres.Row + rowiterator, celres.Column + coliterator + 2).Value = X_Epsilon_Delta_Epsilon_tr()
            Cells(celres.Row + rowiterator, celres.Column + coliterator + 3).Value = X_Q_Delta_Qd() 'No idea what Delta_Qd() is - check this
            Cells(celres.Row + rowiterator, celres.Column + coliterator + 4).Value = X_x_Delta_Smallx()
            Cells(celres.Row + rowiterator, celres.Column + coliterator + 5).Value = Delta_Largex()
            
            '--------------------------reset to the start of the row------------------------------------------------------------------
            rowiterator = 0
    Loop
'-----------------------recalculate the above 6 parameters for every target gas-------------------------------------------------------
coliterator = coliterator + 6
rowiterator = 0

Loop

MsgBox "I`m finished here!"



End Sub






