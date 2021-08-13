import pandas as pd # Following naming convention

#Installed the openpyxl package

coursesFile = "src/main/resources/input/CAES-2020-Sem1-Wvl/Courses.xlsx"


#coursesEF = pandas.ExcelFile(coursesFile, engine="openpyxl") # Load the Courses spreadsheet as an Excel File
#coursesDF = coursesEF.parse("Sheet1") # Load the first (and only) sheet as a DataFrame

"""
    Using "openpyxl" engine instead of the default "xlrd" engine as xlrd only supports old-style Excel files (.xls)
    whilst openpyxl supports newer Excel formats
"""
# Although the data types are of int in the Excel file, we are forcing the conversion in case they were entered/read differently
# Load the first (and only) sheet | First line of data is taken as the column headings
# ALT sheet_name="Sheet1"
coursesDF = pd.read_excel(coursesFile, sheet_name=0, header=0, engine="openpyxl", dtype={'labNum':int, 'sectionNum':int, 'allocatedTimeslot':int, 'venueCapacity':int, 'sessionLength':int})
totalLabSections = len(coursesDF)
coursesColDF = coursesDF["course"]

print(coursesDF)
