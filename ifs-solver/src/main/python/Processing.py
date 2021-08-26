import pandas as pd # Following naming convention
from bs4 import BeautifulSoup # For reading from XML files (bs4 needs to be installed first)
from xml.dom import minidom # For creating and writing to XML files

#Installed the openpyxl, beautifulsoup4 and lxml packages

def main():
	problemInstanceName = "2020-Sem1-CAES-Wvl"
	coursesFilePath = "src/main/resources/input/" + problemInstanceName + "/Courses.xlsx"
	studentsFilePath = "src/main/resources/input/" + problemInstanceName + "/Students.xlsx"
	problemSpecificationFilePath = "src/main/resources/input/" + problemInstanceName + "/Specification.xml" # Make txt ?

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

	#print(coursesDF)

	studentsDF = pd.read_excel(studentsFilePath, sheet_name=0, header=0, engine="openpyxl", dtype={'numCourses':int})
	#print(studentsDF)

	"""
	for student in range(20):
		for col in range(len(studentsDF.columns)):
			print(studentsDF.iloc[student, col], end="\t")
		print()
	"""

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
	currentCourseRequestID = 0 # A 'course request' is a student-course combination where the student is (already) registered/enrolled for this course (for my SS problem specification) and wants to be assigned to a section for each of the labs (A UniTime Solver 'subpart') of this course

	"""
		A dictionary (map) to keep track of all the assigned ID's for the courses | to be used when processing students' course enrollments/requests
		key = course; value = courseID

	"""
	courseIdDict = {}


	""" Process all course offerings (All LabSections for each Lab for each Course) """

	# [DONE] Todo - Add course code, labNum, sectionNum, allocatedDay (from the Courses.xlsx to the offering elements) and the studentNumber, surname, firstnames (from the Students.xlsx to the student elements) to the XML input doc as additional attributes to their elements
	# Since XML is extensible, this shoudn't break/affect the solver, and it will still appear in the solver's solution xml file (hopefully)
	# which will make me reading that xml file easier (to understand what the id is referring to which specific course/labNum/sectionNum) and
	# reduce processing to generate a readable solution

	# REFER TO SSDataFormatTemplate.xml (and my Problem Modelling Word doc) FOR THE MEANINGS OF THE ELEMENT NAMES AND LOGIC EXPLANATION
	"""
		Links/References to read for iterating/traversing DataFrames:
			https://www.geeksforgeeks.org/different-ways-to-iterate-over-rows-in-pandas-dataframe/
			https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas
			https://www.geeksforgeeks.org/iterating-over-rows-and-columns-in-pandas-dataframe/
			  
	"""
	numLabSections = len(coursesDF)
	for labSection in range(numLabSections): # Each row/entry in the Courses.xlsx file is a LabSection - a section of a lab for a Course
		courseName = coursesDF.loc[labSection, "course"] # The course that this LabSection belongs to

		# if a different course - i.e. a new course to process
		if courseName != currentCourse:  # Create new 'offering' element with its own 'course' and 'config' sub-elements

			currentOfferingElement = inputFileXML.createElement("offering")
			currentCourseID += 1
			currentOfferingElement.setAttribute("id", str(currentCourseID)) # str() because arguments to xmlFile.write() must all be strings - XML attribute values are all strings
			offeringsElement.appendChild(currentOfferingElement)

			currentCourseElement = inputFileXML.createElement("course")
			currentCourseElement.setAttribute("id", str(currentCourseID))
			currentCourseElement.setAttribute("name", str(courseName)) # My own additional atrribute to the XML input doc (See Todo above)
			currentOfferingElement.appendChild(currentCourseElement)

			currentConfigElement = inputFileXML.createElement("config")
			currentConfigElement.setAttribute("id", str(currentCourseID))
			currentOfferingElement.appendChild(currentConfigElement)

			courseIdDict[courseName] = currentCourseID # Add this course as a key and its courseID as the value

			currentCourse = courseName
			currentLabNum = 0 # Reset lab num (to 0 so that when the first lab (labNum=1) of the next course is read, a new subpart tag will be created)

		# else continue with the currentConfigElement variable unmodified

		labNum = coursesDF.loc[labSection, "labNum"] # The lab this LabSection belongs to

		# if a different labNum - i.e. the next lab for the current course to process
		if labNum != currentLabNum:  # Create a new 'subpart' element under this current offering config
			currentSubpartElement = inputFileXML.createElement("subpart")
			currentLabID += 1
			currentSubpartElement.setAttribute("id", str(currentLabID))
			currentSubpartElement.setAttribute("courseLabNum", str(labNum)) # My own additional atrribute to the XML input doc (See Todo above)
			currentConfigElement.appendChild(currentSubpartElement)

			currentLabNum = labNum

		# else continue with the currentSubpartElement variable unmodified

		# Add LabSection (UniTime: 'section') to current lab (UniTime: 'subpart')
		currentSectionElement = inputFileXML.createElement("section")
		currentLabSectionID += 1
		currentSectionElement.setAttribute("id", str(currentLabSectionID))
		sectionNum = coursesDF.loc[labSection, "sectionNum"] # The section number (of its lab) of this LabSection
		currentSectionElement.setAttribute("courseLabSectionNum", str(sectionNum)) # My own additional atrribute to the XML input doc (See Todo above)
		venueCapacity = coursesDF.loc[labSection, "venueCapacity"] # The capacity of this LabSection session
		currentSectionElement.setAttribute("limit", str(venueCapacity))
		currentSubpartElement.appendChild(currentSectionElement)

		# Add 'time' tag for this Lab Section
		currentTimeElement = inputFileXML.createElement("time")
		allocatedDay = coursesDF.loc[labSection, "allocatedDay"] # The allocated day of this LabSection session
		allocatedDayBinary = generateDaysValue(allocatedDay)
		currentTimeElement.setAttribute("days", str(allocatedDayBinary))
		allocatedTimeslot = coursesDF.loc[labSection, "allocatedTimeslot"] # The allocated timeslot of this LabSection session
		currentTimeElement.setAttribute("start", str(allocatedTimeslot))
		sessionLength = coursesDF.loc[labSection, "sessionLength"] # The length of this LabSection session
		currentTimeElement.setAttribute("length", str(sessionLength))
		currentTimeElement.setAttribute("allocatedDay", str(allocatedDay)) # My own additional atrribute to the XML input doc (See Todo above)
		currentSectionElement.appendChild(currentTimeElement)


	""" Process all student enrollments (lab sessions requests) """

	# courseIdDict - dictionary of course ID's

	numStudents = len(studentsDF)

	for student in range(numStudents):
		#print(student)
		currentStudentElement = inputFileXML.createElement("student")
		currentStudentID += 1
		currentStudentElement.setAttribute("id", str(currentStudentID))
		studentNumber = studentsDF.loc[student, "studentNumber"]
		currentStudentElement.setAttribute("studentNumber", str(studentNumber))
		surname = studentsDF.loc[student, "surname"]
		currentStudentElement.setAttribute("surname", str(surname))
		firstnames = studentsDF.loc[student, "firstnames"]
		#print(firstnames)
		currentStudentElement.setAttribute("firstnames", str(firstnames))
		studentsElement.appendChild(currentStudentElement)

	# Todo - cater for qualifications/degrees having their students be allocated to specific timeslots for specific courses
		#try and implement this by having an input file for the degree-course specific allocations, and when processing students
		# add that timeslot as a current allocation for their course request



	inputFileXML = inputFileXML.toprettyxml(indent="\t")

	xmlFileName = "src/main/resources/input/" + problemInstanceName + "/" + problemInstanceName + ".xml"

	# Write the input data XML file
	with open(xmlFileName, "w") as xmlFile:
		try:
			xmlFile.write(inputFileXML)
		except UnicodeEncodeError as error:
			print("ERROR:", error)
			print("\tOne of the input files contains a (at least one) character that is not a valid Unicode symbol.")
			print("\tWriting to input data XML file has been aborted. Please fix Error and re-run this program.")



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


def generateDaysValue(allocatedDay: str) -> str:
	"""
		Generate the binary string that specifies the day of the week that a LabSection session is taking place:

		Convert the day argument given (that specifies a day of the week in full) to a binary string of length 7 indicating
		that day with a 1 and all other days with a 0.

		The UniTime's Student Sectioning Solver wants the days that an event session takes place on to be in a binary string
		encoding format with each character representing a day (from Monday to Sunday) and the char being '1' if the event session takes place on that
		day of the week, else 0. This binary string is the value of the 'days' attribute of the 'time' element.

		For this (my) Student Lab Section Problem, a lab (LabSection) session takes place on one only one specified day of the week,
		so there will be one '1' and six '0''s in the binary string


		:param allocatedDay: The day of the week (in full) that a LabSection session is taking place
		:return: The binary string specifying the given day of the week that the LabSection session is taking place
	"""
	# Using a map to store the conversions and the to extract the relevant one for the allocatedDay day
	# This is simpler than using if-elif-else statements and the current version of Python does not have switch/case statement functionality

	dayConverter = {
		"Monday":       "1000000",
		"Tuesday":      "0100000",
		"Wednesday":    "0010000",
		"Thursday":     "0001000",
		"Friday":       "0000100",
		"Saturday":     "0000010",
		"Sunday":       "0000001",
	}

	"""
		using dayConverter.get(key) instead of dayConverter[key] so that I can specify a default value ("1000000" -> for Monday) 
		if an invalid key (allocated day of the week) is given and avoid a KeyError
	"""
	return dayConverter.get(allocatedDay, "1000000")




# Run the main method if this python file is being executed/run directly (either from IDE or Command Line)
if __name__ == '__main__':
	main()
	print("Processing.py has been executed")