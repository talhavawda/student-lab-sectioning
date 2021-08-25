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
    #coursesColDF = coursesDF["course"]

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
    sectioningElement = inputFileXML.createElement("sectioning") # Create the root element 'sectioning'

    """ Add the attributes of the 'sectioning element' - this is the problem specification information (having being extracted 
    and stored in specificationDict)"""
    sectioningElement.setAttribute("version", specificationDict["version"])
    sectioningElement.setAttribute("initiative", specificationDict["initiative"])
    sectioningElement.setAttribute("term", specificationDict["term"])
    sectioningElement.setAttribute("year", specificationDict["year"])
    sectioningElement.setAttribute("created", specificationDict["created"])
    sectioningElement.setAttribute("nrDays", specificationDict["nrDays"])
    sectioningElement.setAttribute("slotsPerDay", specificationDict["slotsPerDay"])

    inputFileXML.appendChild(sectioningElement)

    """ Create the 'offerings' and 'students' sub-elements of the sectioning element"""

    offeringsElement = inputFileXML.createElement("offerings")
    sectioningElement.appendChild(offeringsElement)

    studentsElement = inputFileXML.createElement("students")
    sectioningElement.appendChild(studentsElement)

    # Initialise all the ID variables's that are going to be used
    # All id's start with 1 in the UniTime SS Data Format so the variables will be incremented before they'll be assigned
    currentCourse = ""
    currentLabNum = 0
    currentCourseID = 0  # used for 'offering', 'course', and 'config' tags/elements for their 'id' attributes | for my SS problem, all offerings consists of only 1 course and 1 configuration, so the id's will be matching for all
    currentLabID = 0  # used for 'subpart' tag/element for its 'id' attribute | currentLabID is a unique course-labNum combination (from the Courses.xlsx file)
    currentLabSectionID = 0  # used for 'section' tag/element for its 'id' attribute | currentLabSectionID is a unique course-labNum-sectionNum combination (from the Courses.xlsx file)
    currentStudentID = 0

    # Process all course offerings (All LabSections for each Lab for each Course)

    # REFER TO SSDataFormatTemplate.xml (and my Problem Modelling Word doc) FOR THE MEANINGS OF THE ELEMENT NAMES
    """
        Links/References to read for iterating/traversing DataFrames:
            https://www.geeksforgeeks.org/different-ways-to-iterate-over-rows-in-pandas-dataframe/
            https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas
            https://www.geeksforgeeks.org/iterating-over-rows-and-columns-in-pandas-dataframe/
              
    """
    totalLabSections = len(coursesDF)
    for labSection in range(totalLabSections): # Each row/entry in the Courses.xlsx file is a LabSection - a section of a lab for a Course
        courseName = coursesDF.loc[labSection, "course"] # The course that this LabSection belongs to

        if courseName != currentCourse:  # Create new 'offering' element

            currentOfferingElement = inputFileXML.createElement("offering")
            currentCourseID += 1
            currentOfferingElement.setAttribute("id", str(currentCourseID))
            offeringsElement.appendChild(currentOfferingElement)

            currentCourseElement = inputFileXML.createElement("course")
            currentCourseElement.setAttribute("id", str(currentCourseID))
            currentOfferingElement.appendChild(currentCourseElement)

            currentConfigElement = inputFileXML.createElement("config")
            currentConfigElement.setAttribute("id", str(currentCourseID))
            currentOfferingElement.appendChild(currentConfigElement)

            currentCourse = courseName
            currentLabNum = 0 # Reset lab num (to 0 so that when the first lab (labNum=1) of the next course is read, a new subpart tag will be created)

        # else continue with the currentOfferingElement and currentConfigElement variables unmodified

        labNum = coursesDF.loc[labSection, "labNum"] # The course that this LabSection belongs to

        if labNum != currentLabNum:  # Create a new 'subpart' element under this current offering config
            currentSubpartElement = inputFileXML.createElement("subpart")
            currentLabID +=1
            currentSubpartElement.setAttribute("id", str(currentLabID))
            currentConfigElement.appendChild(currentSubpartElement)

            currentLabNum = labNum

        # else continue with the currentSubpartElement variable unmodified

        # Add LabSection
        currentSectionElement = inputFileXML.createElement("section")
        currentLabSectionID += 1
        currentSectionElement.setAttribute("id", str(currentLabSectionID))
        currentSubpartElement.appendChild(currentSectionElement)






        #print(labSection, coursesDF.loc[labSection, "sectionNum"])





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