Attribute VB_Name = "Module3"

Public Sub Clear_Click()
' This macro clears all cells for new worksheet. Travels to the right and down. Select the rightermost/. To break, create three new blank columns in a row.
' Also clears other parameters required as inputs during experiment.
' Uncertainties can be rewritten into the sheet using the uncertainty button. As so for any other formulas that were deleted in this sheet.
'DO NOT delete column H - tracer gas column. Code will only erase as many rows as there are populated in the tracer gas column.
'------------------Activate worksheet--------------------------------------
Worksheets("Main").Activate

Dim rowiterator As Integer
Dim coliterator As Integer
Dim staticrowiterator As Integer

rowiterator = 0
coliterator = 0

Dim x As Boolean


On Error Resume Next
Do While Not x
Set celres = Application.InputBox("Select cell (everything right of it and below it will be cleared at column H populated values depth)", Type:=8)
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


'---loop to populate uncertainty section rows along which column H (tracer gas) has a value-----------
Do Until WorksheetFunction.CountA(Columns(celres.Column + coliterator)) = 0 _
And WorksheetFunction.CountA(Columns(celres.Column + coliterator + 1)) = 0 _
And WorksheetFunction.CountA(Columns(celres.Column + coliterator + 2)) = 0

Do Until IsEmpty(Cells(celres.Row + rowiterator, 8))
    Cells(celres.Row + rowiterator, celres.Column + coliterator).Value = ""
    rowiterator = rowiterator + 1
Loop

coliterator = coliterator + 1
staticrowiterator = rowiterator
rowiterator = 0

Loop

'Clear initial information
Range(Cells(celres.Row, 1), Cells(celres.Row + staticrowiterator, 7)).ClearContents
    
     
'Clear actual values
Range(Cells(celres.Row, 15), Cells(celres.Row + staticrowiterator, 24)).ClearContents

'Clear datalogger times
 Range(Cells(celres.Row, 28), Cells(celres.Row + staticrowiterator, 29)).ClearContents


'Clear purple area - FTIR and concentration
Range(Cells(celres.Row, 25), Cells(celres.Row + staticrowiterator, 27)).ClearContents
    
'Clear temperatures
Range(Cells(celres.Row, 47), Cells(celres.Row + staticrowiterator, 51)).ClearContents

End Sub
