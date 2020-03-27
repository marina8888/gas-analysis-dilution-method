Attribute VB_Name = "Module4"
Sub RecordData()

Dim StartRow As Integer
Dim EndRow As Integer
Dim RowCount As Integer


'Provide row numbers for spreadsheet
StartRow = InputBox("What row number does data collection start on?")
RowCount = InputBox("How many rows would you like to populate?")
EndRow = StartRow + RowCount


InputBasicsForm.Show

'Setting up intial parameters in sheet

'Extending tracer gas column and formula
    Cells(StartRow, 8).Select
    Selection.AutoFill Destination:=Range(Cells(StartRow, 8), Cells(EndRow, 8)), Type:=xlFillCopy
    

'Extending sheet numbers
    Cells(StartRow, 9).Select
    Selection.AutoFill Destination:=Range(Cells(StartRow, 9), Cells(EndRow, 9)), Type:=xlFillSeries
    
'Extending book number - needs input
    Cells(StartRow, 1).Select
    Selection.AutoFill Destination:=Range(Cells(StartRow, 1), Cells(EndRow, 1)), Type:=xlFillCopy
    

'Extending date
    Cells(StartRow, 3).Select
    ActiveCell.Value = "4/1/2020"
    Selection.AutoFill Destination:=Range(Cells(StartRow, 3), Cells(EndRow, 3)), Type:=xlFillCopy
    Range("C15:C40").Select
    
   
'Extending room pressure
    Cells(StartRow, 5).Select
    ActiveCell.Value = 760
    Selection.AutoFill Destination:=Range(Cells(StartRow, 5), Cells(EndRow, 5)), Type:=xlFillCopy

'Extending laminar flame speed
    Cells(StartRow, 7).Select
    ActiveCell.Value = 2.2
    Selection.AutoFill Destination:=Range(Cells(StartRow, 7), Cells(EndRow, 7)), Type:=xlFillCopy

'Extending calcs from data logger
    Range(Cells(StartRow, 10), Cells(StartRow, 14)).Select
    Selection.AutoFill Destination:=Range(Cells(StartRow, 10), Cells(EndRow, 14)), Type:=xlFillDefault
    
'Extending data logger calcs
    Range(Cells(StartRow, 30), Cells(StartRow, 46)).Select
    Selection.AutoFill Destination:=Range(Cells(StartRow, 30), Cells(EndRow, 46)), Type:=xlFillDefault
    
'Pink and green sections - pulling FTIR data and doing thermal calculations
    Range(Cells(StartRow, 52), Cells(StartRow, 74)).Select
    Selection.AutoFill Destination:=Range(Cells(StartRow, 52), Cells(EndRow, 74)), Type:=xlFillDefault

    
'Extending logger number**
    Range("D15").Select
    ActiveCell.FormulaR1C1 = "1"
    Range("D15").Select
    Selection.AutoFill Destination:=Range("D15:D40"), Type:=xlFillDefault
    

'Extending colour for MFM full scale values classification - needs input**
    Range("B15").Select
    Selection.AutoFill Destination:=Range("B15:B40"), Type:=xlFillDefault
 

End Sub



