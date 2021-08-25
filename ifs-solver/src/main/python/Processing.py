import pandas as pd # Following naming convention
from bs4 import BeautifulSoup # For reading from XML files (bs4 needs to be installed first)
from xml.dom import minidom # For creating and writing to XML files

#Installed the openpyxl package

coursesFilePath = "src/main/resources/input/CAES-2020-Sem1-Wvl/Courses.xlsx"
studentsFilePath = "src/main/resources/input/CAES-2020-Sem1-Wvl/Students.xlsx"
problemSpecificationFilePath = "src/main/resources/input/CAES-2020-Sem1-Wvl/Specification.xml" # Make txt ?

#coursesEF = pandas.ExcelFile(coursesFile, engine="openpyxl") # Load the Courses spreadsheet as an Excel File
#coursesDF = coursesEF.parse("Sheet1") # Load the first (and only) sheet as a DataFrame

"""
    Read in input files as Pandas Data Frames
    
    Using "openpyxl" engine instead of the default "xlrd" engine as xlrd only supports old-style Excel files (.xls)
    whilst openpyxl supports newer Excel formats
"""
# Although the data types are of int in the Excel file, we are forcing the conversion in case they were entered/read differently
# Load the first (and only) sheet | First line of data is taken as the column headings
# ALT sheet_name="Sheet1"
coursesDF = pd.read_excel(coursesFilePath, sheet_name=0, header=0, engine="openpyxl", dtype={'labNum':int, 'sectionNum':int, 'allocatedTimeslot':int, 'venueCapacity':int, 'sessionLength':int})
totalLabSections = len(coursesDF)
coursesColDF = coursesDF["course"]

print(coursesDF)


"""
    Create the XML input data file for this input
        - Adding both Course and Student information to the data file
"""

# Create XML document with XML Prolog
inputFileXML = minidom.Document()

# Student Sectioning
sectioning = inputFileXML.createElement("sectioning") # Create the root element 'sectioning'
inputFileXML.appendChild(sectioning)

""" Add the attributes of the 'sectioning element'"""
sectioning.setAttribute()

""" Create the 'offerings' and 'students' sub-elements of the sectioning element"""

offerings = inputFileXML.createElement("offerings")
sectioning.appendChild(offerings)

students = inputFileXML.createElement("students")
sectioning.appendChild(students)





inputFileXML = inputFileXML.toprettyxml(indent="\t")

xmlFileName = "src/main/resources/input/CAES-2020-Sem1-Wvl/CAES-2020-Sem1-Wvl.xml"

# Write the input data XML file
with open(xmlFileName, "w") as xmlFile:
    xmlFile.write(inputFileXML)

#print(inputFileXML.childNodes[0].toxml())


#def processProblemSpecification(problemSpecificationFilePath):

