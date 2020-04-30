# gas-analysis-dilution-method

### Overview
Often, the equipment used for product gas analysis has a limited measurement range and a dilution gas(es) is added so that the measured gas values (such as NOx) do not exceed equipment tolerances. Often the tracer gas (within the dilution gas mixture) can also be the target species that the user needs to measure (as can often be the case with CO2 and N2). In this case one dilution gas is insufficient and two dilution gases must be used during the experiment. Calculating parameters and uncertainties for two dilution gases involves long equations and multiple parameters, that can be cumbersome and time-consuming to write within the constraints of the standard excel functions. This file defines the user defined functions for gas analysis (when zero, one or two dilution gases are used).

Equations and parameters are labelled and defined in Hayakawa et. al, 2020. 

### Notes
Recently, the project has been moved from VBA to Python as the base language - using Pandas for data manipulation. The Woorkbook class will split the sheet based on number of dilution gases used and perform the relevant calculations. 

### Functions
These files perform calculations, given an excel spreadsheet of results:

1. The Workbook class contains all methods for calculating the uncertainties and values for the dilution gas. 

2. The graph functions file contains all functions to plot the graphs required

3. To run, please run from the src/main folder.  

### Standard Format 
1. The code will only work given the requirements.txt is installed to the user's environment and that the inital column headers and formats listed in the code match the spreadsheet used. When running the code, as initial input, please list the starting row number (as given by excel) that the data is taken from (excluding MFM calibration data rows) and the gases for which data has been transferred into the spreadsheet as 2 seperate lists - first those measured by ppmv and then those measured by %. 

2. Calculations are valid whether there is no dilution gas, or when one or two dilution gases are used in the experiment. Each set of measured values should be populated on a new row and the equations used are decided based on the tracer gas value column. 
0 - no dilution gas used
1 - single dilution gas method used (all values should be marked as 1)
2- 2nd dilution gas used
Please note that for using 2 dilution gases, the reading has to be repeated for both dilution gases (at the same dilution gas flowrate). Hence the same condition has to be recorded twice, on two different rows, and the 1st dilution gas row must always be above the 2nd dilution gas row. If this is not practical during the experiment, rows should be rearranged manually so that the tracer gas column reads as 1,2,1,2... for any sections that use two dilution gases. 

3. Spreadsheet structure assumes the use of a datalogger and thermocouples, as well as massflowmeters that contain appropriate calibration values. Columns need to be added if additional gases and mass flowmeters are used. Additional rows should be added, labelled with a colour in the first column and also added to the formula sheet if more than 4 different combinations of mass flowmeters (and hence full scale values) were used. These cells can be set to 1s if the data logger values already take into account the full scale calibration values. 

4. User must populate: mass flow meter full-scale calibration values (assigned an arbitrary colour for classification and when mass flowmeters are swapped during experiment), datalogger sheet number, tracer gas value (0,1 or 2..), sheet number (which is sequential and matches tab names 1,2,3...), Xi-tr which is the concentration of tracer gas in the dilution gas, start and end times for the datalogger (if a data logger is used), and measured mole fractions of target and tracer species saved as sequentially numbered data sheets. Please note that Epsilontr values are the measured mole fraction of the tracer species and should also be included in these data sheets. 

5. Please note that colours listed on template (especially for MFM full scale value) can change depending on colour theme that the user has installed locally. 

Please see references for experimental method and further information:
### References 
<a id="1">[1]</a> Akihiro HAYAKAWA, Yuta HIRANO, Akinori ICHIKAWA, Keishi MATSUO, Taku KUDO, Hideaki KOBAYASHI, Novel dilution sampling method for gas analysis with a low sampling rate, Mechanical Engineering Journal, 論文ID 19-00193, [早期公開] 公開日 2020/03/09, Online ISSN 2187-9745, https://doi.org/10.1299/mej.19-00193, https://www.jstage.jst.go.jp/article/mej/advpub/0/advpub_19-00193/_article/-char/ja, 抄録:

### Contributions
To contribute please raise an issue then open a pull request for review.
