VERSION 5.00
Begin {C62A69F0-16DC-11CE-9E98-00AA00574A4F} InitialInput 
   Caption         =   "Initial Input Form"
   ClientHeight    =   3360
   ClientLeft      =   45
   ClientTop       =   390
   ClientWidth     =   4515
   OleObjectBlob   =   "InitialInput.frx":0000
   StartUpPosition =   1  'CenterOwner
End
Attribute VB_Name = "InitialInput"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False

Dim StartRow As Integer
Dim EndRow As Integer
Dim RowCount As Integer


Private Sub Data_Click()

'Provide row numbers for spreadsheet
StartRow = InputBox("What row number does data collection start on?")
RowCount = InputBox("How many rows would you like to populate?")
EndRow = StartRow + RowCount


'Setting up intial parameters in sheet

'Extending tracer gas column and formula
    Cells(StartRow, 8).Select
    Selection.AutoFill Destination:=Range(Cells(StartRow, 8), Cells(EndRow, 8)), Type:=xlFillCopy
    

'Extending sheet numbers
    Cells(StartRow, 9).Select
    Selection.AutoFill Destination:=Range(Cells(StartRow, 9), Cells(EndRow, 9)), Type:=xlFillSeries
    
'Extending book number - needs input
    Cells(StartRow, 1).Select
    ActiveCell.Value = BookNumInput
    Selection.AutoFill Destination:=Range(Cells(StartRow, 1), Cells(EndRow, 1)), Type:=xlFillCopy
    

'Extending date
    Cells(StartRow, 3).Select
    ActiveCell.Value = DateInputForm
    Selection.AutoFill Destination:=Range(Cells(StartRow, 3), Cells(EndRow, 3)), Type:=xlFillCopy
    Range("C15:C40").Select
    
   
'Extending room pressure
    Cells(StartRow, 5).Select
    ActiveCell.Value = PressureInputForm
    Selection.AutoFill Destination:=Range(Cells(StartRow, 5), Cells(EndRow, 5)), Type:=xlFillCopy

'Extending laminar flame speed
    Cells(StartRow, 7).Select
    ActiveCell.Value = FlameSpeedInput
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
    Range("AZ34:BD46").Select

Unload Me
 

End Sub


Private Sub Finish_Click()
Dim iExit As VbMsgBoxResult

iExit = MsgBox("Confirm that you want to exit", vbQuestion + vbYesNo, "Data Entry Form")

If iExit = vbYes Then
Unload Me

End If

End Sub


Private Sub Clear_Click()
BookNumInput = Null
DateInputForm = Null
PressureInputForm = Null
FlameSpeedInput = Null

End Sub



