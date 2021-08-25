import pandas as pd # Following naming convention
from bs4 import BeautifulSoup # For reading from XML files (bs4 needs to be installed first)
from xml.dom import minidom # For creating and writing to XML files

#Installed the openpyxl, beautifulsoup4 and lxml packages

def main():
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

    specificationDict = processProblemSpecification(problemSpecificationFilePath)
    #print(specificationDict)

    """
        Create the XML input data file for this input
            - Adding both Course and Student information to the data file
    """

    # Create XML document with XML Prolog
    inputFileXML = minidom.Document()

    # Student Sectioning
    sectioning = inputFileXML.createElement("sectioning") # Create the root element 'sectioning'
    inputFileXML.appendChild(sectioning)

    """ Add the attributes of the 'sectioning element' - this is the problem specification information (having being extracted 
    and stored in specificationDict)"""
    sectioning.setAttribute("version", specificationDict["version"])
    sectioning.setAttribute("initiative", specificationDict["initiative"])
    sectioning.setAttribute("term", specificationDict["term"])
    sectioning.setAttribute("year", specificationDict["year"])
    sectioning.setAttribute("created", specificationDict["created"])
    sectioning.setAttribute("nrDays", specificationDict["nrDays"])
    sectioning.setAttribute("slotsPerDay", specificationDict["slotsPerDay"])

    """ Create the 'offerings' and 'students' sub-elements of the sectioning element"""

    offerings = inputFileXML.createElement("offerings")
    sectioning.appendChild(offerings)

    students = inputFileXML.createElement("students")
    sectioning.appendChild(students)

    # Initialise all the ID's that are going to be used
    currentCourse = ""
    currentCourseID = 1  # used for 'offering', 'course', and 'config' tags/elements for their 'id' attributes
    currentLabID = 1  # used for 'subpart' tag/element for its 'id' attribute | labID is a unique course-labNum combination (from the Courses.xlsx file)
    currentSectionID = 1  # used for 'section' tag/element for its 'id' attribute | sectionID is a unique course-labNum-sectionNum combination (from the Courses.xlsx file)
    currentStudentID = 1







    inputFileXML = inputFileXML.toprettyxml(indent="\t")

    xmlFileName = "src/main/resources/input/CAES-2020-Sem1-Wvl/CAES-2020-Sem1-Wvl.xml"

    # Write the input data XML file
    with open(xmlFileName, "w") as xmlFile:
        xmlFile.write(inputFileXML)

    #print(inputFileXML.childNodes[0].toxml())


def processProblemSpecification(problemSpecificationFilePath):
    """
        Read/parse in the Specification file for this Student Sectioning Problem instance,
        extracting and storing all its attributes into a dictionary and returning this dictionary

    :param problemSpecificationFilePath:
    :return:
    """

    # Read in the problem specfication info from it's XML file specified
    with open(problemSpecificationFilePath, "r") as specXMLFile:
        specification = specXMLFile.read()

    # Passing the specification info XML file to the BeatifulSoup parser
    specificationBS = BeautifulSoup(specification, "xml")

    specificationDict = {} # Dictionary to store the attributes and their values of the problem specification

    specificationTag = specificationBS.find("specification") # Extract the 'specification' tag/element and its attributes

    specificationDict["version"] = specificationTag.get("version")
    specificationDict["initiative"] = specificationTag.get("initiative")
    specificationDict["term"] = specificationTag.get("term")
    specificationDict["year"] = specificationTag.get("year")
    specificationDict["created"] = specificationTag.get("created")
    specificationDict["nrDays"] = specificationTag.get("nrDays")
    specificationDict["slotsPerDay"] = specificationTag.get("slotsPerDay")

    return specificationDict


# Run the main method if this python file is being executed/run directly (either from IDE or Command Line)
if __name__ == '__main__':
    main()
    print("Processing.py has been executed")