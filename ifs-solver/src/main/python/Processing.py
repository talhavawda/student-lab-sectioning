import pandas

coursesFile = "src/main/resources/input/CAES-2020-Sem1-Wvl/Courses.xlsx"
#coursesFile = "Courses.xlsx"
coursesEF = pandas.ExcelFile(coursesFile, engine="openpyxl") # Load the Courses spreadsheet as an Excel File
coursesDF = coursesEF.parse("Sheet1") # Load the first (and only) sheet as a DataFrame
print(coursesDF)