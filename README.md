# flame-dilution-method

### Overview
Often, equipment used for product gas analysis has a limited range and a dilution gases are added so that the measured gas values (such as NOx) do not exceed tolerances. Often the tracer gas (the gas of interest) within the dilution gas can be the one which is also the target species that the user needs to measure. In this case 1 dilution gas is insufficient and 2 dilution gases must be used. This file defines the equations for gas analysis where the product gas may or may not contain a dilution gas. 

Equations and parameters are labelled as per publication below:
https://www.jstage.jst.go.jp/article/mej/advpub/0/advpub_19-00193/_article/-char/ja/

### Functions
These files perform calculations, given an excel spreadsheet of results:

1. Create-New() macro formats a new spreadsheet into the format suitable for the experiment (adding suitable columns, names and formulas into the appropriate cells). 
2. Clear-Click() macro cleans the spreadsheet and provides an input window for the user during the experiment
3. functions.bas provides a list of UDFs that are called in the Main() subroutine but can also be used as standalone functions
4. Given an Excel spreadsheet that is populated with data, Main() calls functions to populate unknown parameters and their uncertainties in the spreadsheet. 

### Standard Format 
1. Calculations are valid whether there is no dilution gas, or when one or two dilution gases are used in the experiment. Each set of measured values should be populated on a new row and the equations used are decided based on the tracer gas value column. 
0 - no dilution gas used
1 - 1st dilution gas used 
2- 2nd dilution gas used

Please note that for using 2 dilution gases, the reading has to be repeated for both dilution gases (at the same diltuion gas flowrate). Hence the same condition has to be recorded twice, on two different rows, and the 1st dilution gas row must always be above the 2nd dilution gas row. If this is not practical during the experiment, rows should be rearranged manually so that the tracer gas column reads as 1,2,1,2... 

2. Spreadsheet structure assumes the use of a datalogger and thermocouples, as well as massflowmeters that contain appropriate calibration values. Columns and code should be adjusted if the user is using a different number of mass flowmeters 

3. User must populate: mass flow meter full-scale calibration values (assigned an arbitrary colour for classification and when mass flowmeters are swapped during experiment), datalogger sheet number, tracer gas value (0,1 or 2..), sheet number (which is sequential and matches tab names 1,2,3...), Xi-tr which is the concentration of tracer gas in the dilution gas, start and end times for the datalogger (if a data logger is used), and measured mole fractions of target and tracer species saved as sequentially numbered data sheets. Please note that Epsilontr values are the measured mole fraction of the tracer species and should also be included in these data sheets. 
Please see paper below for experimental method and further information:

https://www.jstage.jst.go.jp/article/mej/advpub/0/advpub_19-00193/_article/-char/ja/

### Contributions

To contribute please raise an issue then open a pull request for review.
