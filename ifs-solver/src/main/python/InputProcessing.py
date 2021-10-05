import pandas as pd # Following naming convention
from bs4 import BeautifulSoup # For reading from XML files (bs4 needs to be installed first)
from xml.dom import minidom # For creating and writing to XML files

#Installed the openpyxl, beautifulsoup4 and lxml packages

def main():
	problemInstanceName = "2020-Sem1-CAES-Wvl-no-extra-requests-testing"
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
	# Although some of the data types are of int in the Excel file, we are forcing the conversion in case they were entered/read differently
	# sessionStartTime also needs to be specified as a string otherwise Pandas will interpret it as a datatime.time object
	# Load the first (and only) sheet | First line of data is taken as the column headings
	# ALT sheet_name="Sheet1"
	coursesDF = pd.read_excel(coursesFilePath, sheet_name=0, header=0, engine="openpyxl", dtype={'labNum':int, 'sectionNum':int, 'sessionStartTime':str, 'sessionLength':str, 'venueCapacity':int})
	#coursesColDF = coursesDF["course"]

	print(coursesDF)

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
	sectioningElement = inputFileXML.createElement("sectioning")  # Create the root element 'sectioning'

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

	currentCourseRequestID = 0 # A 'course request' is a student-course combination where the student is (already) registered/enrolled for this course (for my SS problem specification) and wants to be assigned to a section for each of the labs (A UniTime Solver 'subpart') of this course

	"""
		courseIdDict: A dictionary (map) to keep track of all the assigned ID's for the courses (the courses from the 
		Courses.xlsx input file - the courses in this problem instance's input). 
		To be used when processing students' new course enrollments/requests i.e. to check if a course that a student is 
		registered for exists in this problem instance's input.
		key = course; value = courseID
		
		courseNameDict: A 	dictionary (map) to keep track of all the course names for the assigned course ID's | opposite to / reverse of courseIdDict
		key = courseID; value = courseName 
		
		I am going to add a 'courses' element to the input data XML file as a sub-element of the sectioning element that
		stores the courseID-courseName mappings so that I can access the name of a course based on its ID later on if 
		I want to (for e.g. in ModifiedInputProcessing.py).

	"""
	courseIdDict = {}
	courseNameDict = {}

	coursesElement = inputFileXML.createElement("courses")
	sectioningElement.appendChild(coursesElement)


	""" Process all course offerings (All LabSections for each Lab for each Course) """

	# [DONE] Todo - Add course name/code/numLabs, labNum, sectionNum, sessionDay (from the Courses.xlsx to the offering elements) and the studentNumber, surname, firstnames,
	#  numCourses, numProcessedCourses (from the Students.xlsx to the student elements), as well as the course name (to each course request) to the XML input doc as additional
	#  attributes to their elements

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

			if currentCourseID > 0: # If this course is not the first course to be processed
				previousCourseNumLabs = labNum
				currentCourseElement.setAttribute("numLabs", str(previousCourseNumLabs)) # the previous course element as I haven't reassigned it yet | My own additional attribute to the XML input doc (See Todo above)


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
			courseNameDict[currentCourseID] = courseName # Add this courseID as a key and this course's name as the value

			currentCourse = courseName
			currentLabNum = 0 # Reset lab num (to 0 so that when the first lab (labNum=1) of the next course is read, a new subpart tag will be created)

		# else continue with the currentConfigElement variable unmodified

		labNum = coursesDF.loc[labSection, "labNum"] # The lab this LabSection belongs to

		# if a different labNum - i.e. the next lab for the current course to process
		if labNum != currentLabNum:  # Create a new 'subpart' element under this current offering config
			currentSubpartElement = inputFileXML.createElement("subpart")
			currentLabID += 1
			currentSubpartElement.setAttribute("id", str(currentLabID))
			currentSubpartElement.setAttribute("itype", "Laboratory") #itype: Instructional Type | All events in this lab sectioning project are Labs
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
		sessionDay = coursesDF.loc[labSection, "sessionDay"] # The allocated day of this LabSection session
		sessionDayBinary = generateDaysValue(sessionDay)
		currentTimeElement.setAttribute("days", str(sessionDayBinary))
		sessionStartTime = coursesDF.loc[labSection, "sessionStartTime"]
		startTimeslot = generateTimeslot(sessionStartTime) # The timeslot number that this LabSection session starts at
		currentTimeElement.setAttribute("start", str(startTimeslot))
		sessionLength = coursesDF.loc[labSection, "sessionLength"] # The length of this LabSection session
		sessionLength = generateTimeslot(sessionLength) # sessionLength in terms of a timeslot value
		currentTimeElement.setAttribute("length", str(sessionLength))
		currentTimeElement.setAttribute("dates", "1") # Setting a random dates binary string (cannot make it an empty string as it is being used to detect time overlap conflicts)
		currentTimeElement.setAttribute("sessionDay", str(sessionDay)) # My own additional atrribute to the XML input doc (See Todo above)
		currentSectionElement.appendChild(currentTimeElement)

	# For the last course
	currentCourseElement.setAttribute("numLabs", str(labNum))


	""" Process all student enrollments (lab sessions requests) """

	numStudents = len(studentsDF)

	for student in range(numStudents):

		# Student's details
		currentStudentElement = inputFileXML.createElement("student")
		studentNumber = studentsDF.loc[student, "studentNumber"]
		currentStudentElement.setAttribute("id", str(studentNumber))
		#currentStudentElement.setAttribute("studentNumber", str(studentNumber))  # My own additional atrribute to the XML input doc (See Todo above)
		surname = studentsDF.loc[student, "surname"]
		currentStudentElement.setAttribute("surname", str(surname))  # My own additional atrribute to the XML input doc (See Todo above)
		firstnames = studentsDF.loc[student, "firstnames"]
		currentStudentElement.setAttribute("firstnames", str(firstnames))  # My own additional atrribute to the XML input doc (See Todo above)

		studentsElement.appendChild(currentStudentElement)

		currentClassifcationElement = inputFileXML.createElement("classification")
		faculty = studentsDF.loc[student, "faculty"]
		currentClassifcationElement.setAttribute("area", str(faculty))
		currentStudentElement.appendChild(currentClassifcationElement)

		currentMajorElement = inputFileXML.createElement("major")
		qualification = studentsDF.loc[student, "qualification"]
		currentMajorElement.setAttribute("area", str(qualification))
		currentStudentElement.appendChild(currentMajorElement)


		# Add the student's courses
		numCoursesStudent = studentsDF.loc[student, "numCourses"] # The number of courses that this student is registered for | I set the data type to 'int' when I read in the Excel file into the DataFrame

		numProcessedCourses = 0  # The number of course of this student that are processed and added (i.e. the courses that were specified in the problem input's Courses.xlsx file)
		for course in range(1, numCoursesStudent+1): # For each course the student is registered for (course number starting from 1)
			courseName = studentsDF.loc[student, "course" + str(course)]

			"""
				Issue #1:
				
				Some courses that some students may be doing (enrolled/registered for) may not be in the problem input's Courses.xlsx input file.
				CURRENTLY, we shall ignore such a course enrollment/registration for the sectioning process (as we do not have 
				the details about that course's lab sessions and allocated timeslots)
				
				If such a course was not in the Courses.xlsx input file then we shall get a KeyError when trying
				to get its courseID from the courseIdDict
			"""
			try:
				courseID = courseIdDict[courseName] # Get the courseID of this course
			except KeyError:
				# Do Nothing - Do not add this registered/enrolled course as a course request  for sectioning
				print("Invalid Course: '" + courseName + "' was not specified in the problem input's Courses.xlsx file")
			else: # if no KeyError thrown - code executed perfectly -> we were able to get the courseID of this course -> this course was specified in the input
				# Process this course enrollment - add it to the student for sectioning
				numProcessedCourses += 1
				currentCourseRequestElement = inputFileXML.createElement("course")
				currentCourseRequestID += 1
				currentCourseRequestElement.setAttribute("id", str(currentCourseRequestID))
				currentCourseRequestElement.setAttribute("priority", "0") # All course requests will have the lowest priority value - all are equal
				currentCourseRequestElement.setAttribute("course", str(courseID))
				currentCourseRequestElement.setAttribute("courseName", str(courseName))  # My own additional attribute to the XML input doc (See Todo above)
				currentStudentElement.appendChild(currentCourseRequestElement)

		currentStudentElement.setAttribute("numCourses", str(numCoursesStudent)) # My own additional atrribute to the XML input doc (See Todo above)
		currentStudentElement.setAttribute("numProcessedCourses", str(numProcessedCourses)) # My own additional atrribute to the XML input doc (See Todo above)


	numCourses = currentCourseID # The number of courses in the problem instance | the last course id used = num courses since first course id == 1

	"""Add the course id-name pairs"""
	for courseID in range(1, numCourses+1):
		currentCourseElement = inputFileXML.createElement("course")
		currentCourseElement.setAttribute("id", str(courseID))
		currentCourseElement.setAttribute("courseName", courseNameDict[courseID])
		coursesElement.appendChild(currentCourseElement)


	sectioningElement.setAttribute("numStudents", str(numStudents))
	sectioningElement.setAttribute("numCourses", str(numCourses))

	# Since this is the initial/first/original input XML file for this problem instance, num course requests is the last CR ID used as CR ID started from 1 for this input data XML file
	sectioningElement.setAttribute("numCourseRequests", str(currentCourseRequestID))

	# last CR ID used
	sectioningElement.setAttribute("lastCourseRequestID", str(currentCourseRequestID))



	inputFileXML = inputFileXML.toprettyxml(indent="\t")

	xmlFileName = "src/main/resources/input/" + problemInstanceName + "/" + problemInstanceName + ".xml"

	# Write the input data XML file
	with open(xmlFileName, "w") as xmlFile:
		try:
			xmlFile.write(inputFileXML)
		except UnicodeEncodeError as error:
			print("ERROR:", error)
			print("\tOne of the input files contains a (at least one) character that is not a valid Unicode symbol.")
			print("\tWriting to input data XML file has been unsuccessful. Process aborted. Please fix Error and re-run this program.")
		else:
			print("Writing to input data XML file '" + xmlFileName + "' has been successful.")

	# Reset/Overwrite CurrentSolutions.txt file to an empty file
	currentSolutionsFilePath = "src/main/resources/input/" + problemInstanceName + "/CurrentSolutions.txt"
	currentSolutionsFile = open(currentSolutionsFilePath, "w")
	#currentSolutionsFile.write("") # The above line will overwrite so I don't need this line
	currentSolutionsFile.close()


# END main()


def processProblemSpecification(problemSpecificationFilePath):
	"""
		Read/parse in the Specification file for this Student Sectioning Problem instance,
		extracting and storing all its attributes into a dictionary and returning this dictionary

	:param problemSpecificationFilePath:
	:return:
	"""

	# Read in the problem specification info from it's XML file specified
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


def generateTimeslot(timeslotTime: str) -> int:
	"""
		Generate the timeslot number of this time (that UniTime's CP Solver uses) based on this time in the 24 hour format (hh:mm).

		The number of tineslots per day is 288 and the length of each slot is 5 minutes. The timeslot numbers are 0 to 277,
		with the first timeslot 0 being 00:00 - 00:05.

	:param time: the time (in a hh:mm format) to convert to a CP Solver timeslot
	:return: a CP Solver timeslot value for the specified time
	"""

	try:
		hour = int(timeslotTime[0:2])
		minute = int(timeslotTime[3:5])
	except ValueError as error:
		print("ERROR:", error)
		print("\tOne of the times specifies in the Courses.xlsx input file is not in the specified time format.")
		print("\tPlease ensure that all times (both in the startTime and sessionLength fields) are in the following format: hh:mm")
		print("\tWriting to input data XML file has been unsuccessful. Process aborted. Please fix Error and re-run this program.")

	return ((hour * 60) + minute) // 5



# Run the main method if this python file is being executed/run directly (either from IDE or Command Line)
if __name__ == '__main__':
	main()
	print("InputProcessing.py has been executed")