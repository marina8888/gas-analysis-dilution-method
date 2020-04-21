import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import openpyxl as xl


Mode=[]
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


with open("some.xls", "wb") as excel_file:
    #Do something
pass




