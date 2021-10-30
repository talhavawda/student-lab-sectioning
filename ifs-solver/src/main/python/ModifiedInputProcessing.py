import pandas as pd  # Following naming convention
from bs4 import BeautifulSoup  # For reading from XML files (bs4 needs to be installed first)
from xml.dom import minidom  # For creating and writing to XML files
# from time import time, ctime, localtime
import time
import copy

#Installed the openpyxl, beautifulsoup4 and lxml packages (lxml is a parser)

"""
	Process the current solution file (solution.xml) along with the input data XML file that was used to obtain it,
	a modified/updated Students input file, and produce an updated input data XML file that is a partial solution 
	(the unchanged/existing course requests from the current input data XML file are still assigned as is, the new course 
	requests are unassigned/unallocated and the old course requests removed)
	
	This current input data XML file and current solution file do not have to be the first/initial solution to the problem instance.
	This means that the user can modify the Students data as many times as they want and obtain a new updated solution. 
	[Each modified version (later modified versions being a modification of the previous modified version) of the initial 
	Students.xlsx input file has a (version modification) number and will be named (by the user) as follows: 'Students-<ModVerNum>.xlsx',
	with the first modified Students input file having the version num being 1, the second being 2, and so on.]
	
	Everytime an updated input data XML file is generated based on the modified/updated Students input, it replaces/overrides
	the previous input data XML file (as my solver code (Main.java) assumes that the name of input data XML file is the same as that
	of the problem instance). So over here, we make the same assumption and the input data XML file that we obtained is the 
	current one instead of the first input data XML file for this problem instance.
	If the user wants to obtain a completely new solution from scratch, they can rerun the InputProcessing.py script
	to obtain an input data XML file with all course requests being unassigned.
	The reason why I ask the user to select the solution (of the current input data XML file) to work with as the 
	current solution (and not also for the input XML file, and not just taking the latest solution) is that the solver can 
	be run many times on the current input data XML file (obtaining parallel/sibling independent solutions to each other) 
	and they may not want to use the last solution obtained. 
	
	This program script assumes that the Courses.xlsx input file remains the same. If the Courses.xlsx file has been updated,
	a new solution needs to be obtained from scratch using the InputProcessing.py script.
	
	In this program, what is referred to in research papers as the 'initial' obtained solution (after which the input will be modified and
	a new solution obtained), I am calling it the current (obtained) solution. Using 'current' instead of 'initial' will make
	more sense to the user.
"""

def main():
	"""

		:return: None
	"""

	#problemInstanceName = input("Enter problem instance name: ")
	problemInstanceName = "2020-Sem1-CAES-Wvl-no-conflicts"

	problemInstanceDirectoryPath = "src/main/resources/input/" + problemInstanceName
	inputXmlFilePath = problemInstanceDirectoryPath + "/" + problemInstanceName + ".xml"  # current input data XML file
	problemInputInstanceSolutionsFile = problemInstanceDirectoryPath + "/CurrentSolutions.txt"


	""" Get the solution of this problem instance's input data XML file instance that we want to work with (the current solution, to the current input data XML file) """

	problemInstanceSolutions = list()
	solutionIndex = 0

	print("Solutions of this problem instance's input data XML file instance:")

	with open(problemInputInstanceSolutionsFile, "r") as solutionsFile:
		for line in solutionsFile:
			line = line[:len(line)-1]  # Remove the "\n" part at the end of the string | Doing -2 cuts out the last digit in the solution name so it seems that '\n' is being treated as one character
			problemInstanceSolutions.append(line)
			print("\t", solutionIndex, ":", line)
			solutionIndex += 1
		solutionsFile.close()

	print()

	try:
		currentSolutionIndex = int(input("Enter the number of the solution that you want to use as the current solution to\nprocess with the modified Students input to obtain the updated solution: "))

		if currentSolutionIndex < 0 or currentSolutionIndex > solutionIndex:  # Validation
			currentSolution = problemInstanceSolutions[-1] # Default is the last element of the list (the latest solution that was generated using the solver) | Alt. we can use solutionIndex
		else:
			currentSolution = problemInstanceSolutions[currentSolutionIndex]

	except ValueError:
		currentSolution = problemInstanceSolutions[-1] # Default is the last element of the list (the latest solution that was generated using the solver)

	currentSolution, currentSolutionFilePath = getCurrentSolutionFilePath(currentSolution, problemInstanceDirectoryPath)


	# Get the modified Students input file, and its modification version number
	modifiedStudentsFilePath, modVerNum = getModifiedStudentsFilePath(problemInstanceDirectoryPath)


	""" Process the current input data and solution XML files and store them in a dictionary """
	currentSolutionDict = processCurrentSolution(inputXmlFilePath, currentSolutionFilePath)

	""" Process the modified Students input Excel file"""
	updatedInputDict = processModifiedStudentsData(modifiedStudentsFilePath, currentSolutionDict)

	""" Generate/Produce the updated input data XML file """
	generateUpdatedInputXmlFile(updatedInputDict, inputXmlFilePath)


	"""
	# Reset/Overwrite CurrentSolutions.txt file to an empty file
	currentSolutionsFile = open(problemInputInstanceSolutionsFile, "w")
	#currentSolutionsFile.write("") # The above line will overwrite so I don't need this line
	currentSolutionsFile.close()
	"""

# END main()


def isEndofMonth(day: int, month: int, year: int):
	"""
		Determine whether the current day of a month is the last day of that month or not.
		Assume day and month are valid values (the initial date-time we got as the initial solution is a valid date-time
		and  we are validating the date-time when incrementing the date-time by 1 second).

		:param day: int: day of a month (as an int). Range: 1-31
		:param month: int: month of a year (as an int). Range: 1-12
		:param year: int: year (as a 2-digit int). Range: 0-99
		:return: boolean, whether the current date (day-month) is the end of that month or not
	"""
	lastDayOfMonth = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

	# The year value in the date-time of the current solution is specificed in 2-digits so we need to convert it into 4 digits to check for leap year. Assume 21st century
	yearStr = "20" + str(year)
	year = int(yearStr)

	# A sub-function of this function
	def isLeapYear(year):
		return (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0)

	if isLeapYear(year) and month == 2:
		return day == 29
	else:
		return day == lastDayOfMonth[month]


def getCurrentSolutionFilePath(currentSolution: str, problemInstanceDirectoryPath: str):
	"""
		The actual folder name (the current  date and time that the solver started, in the yymmdd_hhmmss format) of the
		directory of the current solution instance may not be exactly the same as the name I got from the CurrentSolutions.txt file.
		In my Main.java program where I ran the solver on the current problem instance's input data XML file, I obtained
		the current date and time just before running the solver, and stored it in the CurrentSolutions.txt file thereafter.
		So the actual folder name of the solution (that the solver obtained) may possibly be 1 (or a few) second later than
		the current date-time that I obtained and stored.
		So if the current solution path doesn't exist, increment the date-time of the current solution by 1 second each
		time till the path is valid.

		:param currentSolution: str: the current solution name obtained from the CurrentSolutions.txt file
		:param problemInstanceDirectoryPath: str:
		:return: currentSolution:str: actual name of the current solution, currentSolutionFilePath: str: path of the current solution's solution.xml file
	"""
	problemInstanceCurrentSolutionDirectoryPath = problemInstanceDirectoryPath + "/" + currentSolution
	currentSolutionFilePath = problemInstanceCurrentSolutionDirectoryPath + "/solution.xml"

	while True:
		try:
			open(currentSolutionFilePath, "r")
			break  # currentSolutionFilePath is valid - we have found the current solution folder
		except FileNotFoundError:

			seconds = int(currentSolution[-2] + currentSolution[-1])
			minutes = int(currentSolution[-4] + currentSolution[-3])
			hours = int(currentSolution[-6] + currentSolution[-5])

			year = int(currentSolution[0] + currentSolution[1])
			month = int(currentSolution[2] + currentSolution[3])
			day = int(currentSolution[4] + currentSolution[5])

			#print(year, month, day, hours, minutes, seconds)  # For testing

			# Increment time by 1 second
			if seconds < 59:
				seconds += 1
			elif minutes < 59:  # and seconds == 59
				seconds = 0
				minutes += 1
			elif hours < 23:  # and minutes == 59 and seconds == 59
				seconds = 0
				minutes = 0
				hours += 1
			else:  # hours == 23 and minutes == 59 and seconds == 59
				seconds = 0
				minutes = 0
				hours = 0

				# Increment date by 1 day
				if not isEndofMonth(day, month, year):
					day += 1
				elif month != 12:  # and isEndofMonth(day, month, year)
					day = 1
					month += 1
				else:  # isEndofMonth(day, month, year) and month == 12
					day = 1
					month = 1

					# year value is specified in 2 digits only
					if year < 99:
						year += 1
					else:
						year = 0

			yearStr = str(year)
			monthStr = str(month)
			dayStr = str(day)
			hoursStr = str(hours)
			minutesStr = str(minutes)
			secondsStr = str(seconds)

			if year < 10:
				yearStr = "0" + yearStr

			if month < 10:
				monthStr = "0" + monthStr

			if day < 10:
				dayStr = "0" + dayStr

			if hours < 10:
				hoursStr = "0" + hoursStr

			if minutes < 10:
				minutesStr = "0" + minutesStr

			if seconds < 10:
				secondsStr = "0" + secondsStr


			currentSolution = yearStr + monthStr + dayStr + "_" + hoursStr + minutesStr + secondsStr
			#print(currentSolution)   # For testing

			problemInstanceCurrentSolutionDirectoryPath = problemInstanceDirectoryPath + "/" + currentSolution
			currentSolutionFilePath = problemInstanceCurrentSolutionDirectoryPath + "/solution.xml"


	print("Current solution:\t", currentSolution, end="\n\n")

	return currentSolution, currentSolutionFilePath


def getModifiedStudentsFilePath(problemInstanceDirectoryPath: str):
	"""
		Get the the correct file name of the modified Students input Excel file from the user, and return
		the file path of the modified Students input file
		:param problemInstanceDirectoryPath: str:
		:return: modifiedStudentsFilePath
	"""
	while True:
		try:
			modVerNum = int(input("Enter the modification version number of the modified Students input file that you want to process: "))
			modifiedStudentsFilePath = problemInstanceDirectoryPath + "/Students-" + str(modVerNum) + ".xlsx"
			modifiedStudentsFile = open(modifiedStudentsFilePath, "r")
			modifiedStudentsFile.close()
			break  # If the file was opened successfully
		except FileNotFoundError:
			print("Modified Students input file with that modification version number does not exist. You will be prompted to re-enter\n")
		except ValueError:
			print("Invalid number value entered. You will be prompted to re-enter.")


	print("Modified Students file:\t", "Students-" + str(modVerNum) + ".xlsx", end="\n\n")
	return modifiedStudentsFilePath, modVerNum


def processCurrentSolution(inputXmlFilePath: str, currentSolutionFilePath: str):
	"""
		Read in the current input data XML file and the current solution XML file, and process the data into a dictionary
		that stores all the student details, their course requests and allocated/assigned sections for each of their
		requests from the current solution.

		:param inputXmlFilePath: str: the file path of the current input data XML file
		:param currentSolutionFilePath: str: the file path of the current solution XML file
		:return: currentSolutionDict: a dictionary containing the number of students, the number of courses, the number
		of course requests and a sub-dictionary (studentsDict) containing the student details, requests and allocations, from the current
		solution
	"""
	print("Processing the current input data XML file and current solution XML file...")

	print("\tReading in and parsing the input data and solution XML files...")

	with open(inputXmlFilePath, "r") as inputXMLFile:
		inputXML = inputXMLFile.read()

	with open(currentSolutionFilePath, "r") as solutionXMLFile:
		solutionXML = solutionXMLFile.read()

	# Passing the current input and solution XML files to BeatifulSoup parsers
	inputBS = BeautifulSoup(inputXML, "xml")

	# For efficiency, we are going to concurrently traverse the solution XML file as we traverse the input data XML file to build the studentsDict
	# i.e. so that we do not have to traverse the entire studentsDict afterwards to add the allocated sections to the students' course requests
	solutionBS = BeautifulSoup(solutionXML, "xml")

	print("\tFiles have been read in and parsed.")


	"""
		Obtain the courseID-courseName mappings
	"""
	print("\tObtaining course IDs and names...")

	"""
		courseIdDict: A dictionary (map) to keep track of all the assigned ID's for the courses (the courses from the 
		Courses.xlsx input file - the courses in this problem instance's input). 
		To be used when processing students' new course enrollments/requests i.e. to check if a course that a student is 
		registered for exists in this problem instance's input.
		key = course; value = courseID
		
		courseNameDict: A 	dictionary (map) to keep track of all the course names for the assigned course ID's | opposite 
		to / reverse of courseIdDict
		key = courseID; value = courseName 
		
		The input data XML file has a 'courses' element, as a sub-element of the sectioning element, that stores the 
		courseID-courseName mappings.
	"""
	courseIdDict = {}
	courseNameDict = {}

	inputCoursesTag = inputBS.find("courses") # Extract the 'courses' tag/element and its attributes from the input data XML file (BS considers an XML element as a 'tag')
	courseMappingsTags = inputCoursesTag.find_all("course")

	for course in courseMappingsTags:  # Each course is a tag object
		courseID = course.get("id")
		courseName = course.get("courseName")
		courseNameDict[courseID] = courseName
		courseIdDict[courseName] = courseID

	print("\tCourse IDs and names have been obtained.")


	"""
		studentsDict: A dictionary (Map) of student details (the student's personal info, their course requests, and 
		assigned sections for each of their requests from the current solution.) 
		
		key = studentNumber (their ID); value = a dictionary of the student's details
		
		We are making the key be the students' student number (or ID) according to the institute. This is also the
		id attribute value of the student in the XML file. 
		Using the students' student number as the key helps us quickly check if a student we encounter in the 
		modified Students file already exists in our current solution or is a new student, and also to find a particular student
		with their details (this wouldn't have been possible if we had used a list as the outermost container / data structure).
		
		We will initially populate it with the data from the current input data XML file and current solution XML file,
		and will update it using the modified Students input file. 
	"""
	studentsDict = dict()
	studentsDict.clear()

	inputSectioningTag = inputBS.find("sectioning") # Extract the 'sectioning' tag/element and its attributes from the input data XML file (BS considers an XML element as a 'tag')
	numStudents = int(inputSectioningTag.get("numStudents"))
	numCourses = int(inputSectioningTag.get("numCourses"))
	numCourseRequests = int(inputSectioningTag.get("numCourseRequests"))
	lastCourseRequestID = int(inputSectioningTag.get("lastCourseRequestID"))

	"""
		Obtain student details and course requests from the current input data XML file, the allocated/assigned sections 
		for student course requests from the current solution XML file and process them into studentsDict
	"""
	print("\n\tObtaining student details, their course requests, and allocated sections...")
	print("\t\tProcessing student:")
	inputStudentsTags = inputBS.find_all("student")  # Extract all 'student' tags from the input data XML file

	for student in inputStudentsTags:  # each student is a Tag object
		studentDict = dict() # A dictionary to store the details (attributes from the input data XML file) of this student. This will be the value to the studentNumber key in studentsDict

		# Since all values for attributes in an XML file are strings, all the values obtained below are strings, and will be stored as strings

		studentNumber = student.get("id")
		solutionStudentTag = solutionBS.find("student", id=studentNumber) # Get the student tag/element of this student in the solution.xml file | Source: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#the-keyword-arguments
		print("\t\t\t", studentNumber, sep="")

		studentSurname = student.get("surname")
		studentDict["surname"] = studentSurname
		studentFirstnames = student.get("firstnames")
		studentDict["firstnames"] = studentFirstnames
		studentNumCourses = student.get("numCourses")
		studentDict["numCourses"] = studentNumCourses
		studentNumProcessedCourses = student.get("numProcessedCourses")
		studentDict["numProcessedCourses"] = studentNumProcessedCourses

		studentClassificationTag = student.find("classification")
		studentClassificationArea = studentClassificationTag.get("area")
		studentDict["classificationArea"] = studentClassificationArea

		studentMajorTag = student.find("major")
		studentMajorArea = studentMajorTag.get("area")
		studentDict["majorArea"] = studentMajorArea

		# Changed studentCourseRequests from a List to a Dict
		# studentCourseRequestsList = list() # A list of dictionaries, each dictionary representing a course request
		studentCourseRequestsDict = dict() # A dictionary of course requests; key = courseRequestID, value = dictionary representing the course request details
		studentCourseRequestsTags = student.find_all("course")

		for courseRequest in studentCourseRequestsTags:
			courseRequestDict = dict() # Each key is an attribute of this course request and the value is the corresponding value of the key

			courseRequestID = courseRequest.get("id")
			#courseRequestDict["courseRequestID"] = courseRequestID
			courseRequestPriority = courseRequest.get("priority")
			courseRequestDict["priority"] = courseRequestPriority
			courseRequestCourseID = courseRequest.get("course")
			courseRequestDict["courseID"] = courseRequestCourseID
			courseRequestCourseName = courseRequest.get("courseName")
			courseRequestDict["courseName"] = courseRequestCourseName

			solutionStudentCourseRequestTag = solutionStudentTag.find("course", id=courseRequestID) # The course request tag/element of this course request of this student in the solution XML file

			courseRequestAllocationsList = list() # To store the allocated sections for each subpart class (Lab) of this course (Each course can have multiple labs, with (at most) one allocated section for each lab
			# If there is no allocations for this course request, this course request will not have a 'best' sub-element, and thus will not have any 'section' sub-sub-elements
			# Thus the list will remain empty

			courseRequestAllocationsTags = solutionStudentCourseRequestTag.find_all("section")

			for sectionAllocation in courseRequestAllocationsTags:
				sectionID = sectionAllocation.get("id")
				courseRequestAllocationsList.append(sectionID)

			courseRequestDict["allocations"] = courseRequestAllocationsList

			# studentCourseRequestsList.append(courseRequestDict)
			studentCourseRequestsDict[courseRequestID] = courseRequestDict

		# studentDict["courseRequests"] = studentCourseRequestsList
		studentDict["courseRequests"] = studentCourseRequestsDict

		studentsDict[studentNumber] = studentDict

	print("\n\tStudent details, course requests, and section allocations have been obtained.")
	print("Current input data and solution XML files have been processed.")


	currentSolutionDict = dict()
	currentSolutionDict["numStudents"] = numStudents
	currentSolutionDict["numCourses"] = numCourses
	currentSolutionDict["numCourseRequests"] = numCourseRequests
	currentSolutionDict["lastCourseRequestID"] = lastCourseRequestID
	currentSolutionDict["studentsDictionary"] = studentsDict
	currentSolutionDict["courseIDDict"] = courseIdDict
	currentSolutionDict["courseNameDict"] = courseNameDict

	return currentSolutionDict


def getStudentProcessedCourses(row, studentNumCourses: int, courseIdDict: dict):
	"""
		Determine and return the courses (their names) that thus student (represented by row) is enrolled/registered for,
		based on the data from the (modified) Students input file, which will be used to make a course request for this
		course or check if an existing course request for this course exists.

		Issue #1:

			Some courses that some students may be doing (enrolled/registered for) may have been specified in the problem
			input's Courses.xlsx input file.
			CURRENTLY, we shall ignore such a course enrollment/registration for the sectioning process (as we do not have
			the details about that course's lab sessions and allocated timeslots) - thus we're returning only the courses
			that do appear in the Courses.xlsx input file (i.e. the 'processed' courses)
			If such a course was not in the Courses.xlsx input file then we shall get a KeyError when trying
			to get its courseID from the courseIdDict

		A function has been created for this sub-problem, as it will be used twice in processModifiedStudentsData() -
		when adding a new student, and when processing a student whose course requests have been changed.

		:param row: a student (their details and course requests) from the modificationsDF data frame
		:param studentNumCourses: the actual number of courses that this student is enrolled for
		:param courseIdDict: a dictionary of courseName-courseID mappings
		:return: studentProcessedCourses, a list of (processed) course names that this student is enrolled for
	"""

	studentProcessedCourses = list()

	for courseName in range(1, studentNumCourses + 1):  # For each course the student is registered for (course number starting from 1)

		courseName = row["course" + str(courseName)]

		try:
			courseID = courseIdDict[courseName]  # Get the courseID of this course
		except KeyError:
			# Do Nothing - Do not add this registered/enrolled course as a course request  for sectioning
			print("\t\t\t\tInvalid Course: '" + courseName + "' was not specified in the problem input's Courses.xlsx file")
		else:  # if no KeyError thrown - code executed perfectly -> we were able to get the courseID of this course -> this course was specified in the input
			# Process this course enrollment - add it to the student details for sectioning
			studentProcessedCourses.append(courseName)

	return studentProcessedCourses


def processModifiedStudentsData(modifiedStudentsFilePath: str, currentSolutionDict: dict):
	"""
		Read in the modified Students input Excel file, the dictionary containing the current solution (that stores all
		the student details, their course requests and allocated/assigned sections for each of their requests),
		process the modified Students data (the updated students and course requests details) by updating the dictionary,
		and return the updated dictionary, which represents the updated input for the problem instance.
		This updated dictionary (updatedInputDict) represents a partial solution containing the allocations of the
		unchanged course requests from the current solution.

		Since for SeparateModifiedInputProcessing.py we want the new course requests separately, we have created an
		additional dictionary, studentsNewRequestsDict, that represents the students who have new course requests, and
		their new course requests, which will be added as a sub-dictionary of updatedInputDict (key="studentsNewRequestsDictionary")

		:param modifiedStudentsFilePath: the file path of the modified Students input Excel file, obtained and validated
		using getModifiedStudentsFilePath()
		:param currentSolutionDict: dict: a dictionary representing the current solution. See processCurrentSolution() for
		its' structure
		:return: updatedInputDict, containing the updated input data for this problem instance
	"""
	updatedInputDict = currentSolutionDict

	numStudents = updatedInputDict["numStudents"]
	numCourses = updatedInputDict["numCourses"]
	numCourseRequests = updatedInputDict["numCourseRequests"]
	lastCourseRequestID = updatedInputDict["lastCourseRequestID"]
	studentsDict = updatedInputDict["studentsDictionary"]
	courseIdDict = updatedInputDict["courseIDDict"]
	courseNameDict = updatedInputDict["courseNameDict"]

	studentsNewRequestsDict = dict()  # A dictionary of student's who have new course requests, and containing only their new requests | To be used by SeparateModifiedInputProcessing.py

	print("\nProcessing the modified Students input Excel file...")

	print("\tReading the modified Students input file into a DataFrame...")
	modifiedStudentsDF = pd.read_excel(modifiedStudentsFilePath, sheet_name=0, header=0, engine="openpyxl", dtype={'numCourses':int})


	print("\tReading the current Students input file into a DataFrame...")

	# Since the modifiedStudentsFilePath has been generated by getModifiedStudentsFilePath, it will definitely
	# contain a "-" that separates the 'Solution' substring and the mod. ver. number of this modified Students file, so
	# a valid index value definitely gets returned. And also the name of the problem instance (which is contained in the
	# path) also contains dashes. And there's nothing I can do here if it does not contain the dash ("-").
	# So I will be using rindex() (which raises a ValueError exception if substring not found)
	# instead of rfind() (which returns a -1 if substring not found) - rindex() instead of index() as I want the index
	# of the last occurrence of a dash as the problem instance name will also contain dashes
	# Converting the modification version number to an int type will also raise a ValueError exception if the string is not a valid number
	dashIndex = modifiedStudentsFilePath.rindex("-")
	xlsxIndex = modifiedStudentsFilePath.rindex(".xlsx")
	modVerNum = int(modifiedStudentsFilePath[dashIndex+1:xlsxIndex]) # the modification version number of this modified Students input file

	"""
		Get the file path of the current Students input file (either the initial Students input file or the previous 
		modified Students file) - the input file that was used to produce the current input data XML file that was used 
		to generate the current solution, and use it to read in the current Students input file as a Pandas Data Frame 
	"""
	if modVerNum == 1:  # the first modified Students file
		currentStudentsFilePath = modifiedStudentsFilePath[:dashIndex] + ".xlsx"
	else:
		currentStudentsFilePath = modifiedStudentsFilePath[:dashIndex+1] + str(modVerNum-1) + ".xlsx"
	# print(currentStudentsFilePath)
	currentStudentsDF = pd.read_excel(currentStudentsFilePath, sheet_name=0, header=0, engine="openpyxl", dtype={'numCourses':int})


	"""
		Get the modifications (to student registrations) made to the current Students input file (which are reflected in 
		the modified students input file) by finding rows that are not in both Data Frames that represent these 2 files 
		(i.e. removing all rows that are duplicated in both). We do this by first merging both Data Frames into one (doing 
		concatenation).
		
		In the modificationsDF Data Frame, all the rows taken from currentStudentsDF will appear first, and then the 
		rows from modifiedStudentsDF will follow (since in the concat() parameter I placed currentStudentsDF first). 
		
		For drop_duplicates(), I did not specify a value for the subset parameter as I want to use all the columns (attributes
		of the students) to identify duplicates - in this case a duplicate is if a student exists in both Student input 
		files with their personal details unchanged and having the exact same course requests
		
		For drop_duplicates(), the default value for the ignore_index parameter is False. This means that the indexes of 
		the rows (representing the students) in the modificationsDF are the index of that row from the DF it was taken 
		from (i.e. currentStudentsDF or modifiedStudentsDF). And if a student appears twice in modificationsDF then both 
		of its rows will have the same index. And since we don't know beforehand which students have been placed in 
		modificationsDF, it will be harder to get the indexes of modificationDF so that we can traverse it. 
		So instead we set ignore_index to True so that the usual default indexing (0 ... n-1) for modificationsDF is used.
				
		Observations from my testing:
		If an entire student (with their course registrations) [i.e. an entire row] was added to or removed from the current
		Students input (this addition/removal is reflected in the modified students input, the current input file remains
		unchanged) then the modificationsDF Data Frame will have 1 row for that student - that row will either be from 
		currentStudentsDF or modifiedStudentsDF depending on whether that student was added or removed. 
		However, if an existing student has their personal details or course registrations (course request details) 
		modified, then the modificationsDF Data Frame will have 2 rows for that student - the row from currentStudentsDF 
		and also the row from modifiedStudentsDF. 
	"""
	print("\tObtaining Student modifications made...")
	modificationsDF = pd.concat([currentStudentsDF, modifiedStudentsDF]).drop_duplicates(keep=False, ignore_index=True)
	# print(modificationsDF)

	numModifications = len(modificationsDF)


	"""
		In the updated input data XML file, we want the unchanged course requests to maintain their same course request 
		IDs (so that it is easier to check if existing section allocations were preserved in the updated solution).
		[In the initial input data XML file, students were adding according to the order in which they were in, in the
		Students input file, which is probably in some sorted order]
		So if a course request of an existing student gets deleted (or we remove an entire student), we will not reset 
		the course request IDs by 'shifting down' the IDs of all the course requests that follow. 
		And also if a course request(s) gets added, we will not be 'shifting up' the IDs of all the course requests that 
		follow.
		So all the new course requests that get added (even for existing students with existing course requests) will 
		have their course request ID's be after than the last course request ID used in the current input data XML file.
	"""
	currentCourseRequestID = lastCourseRequestID

	print("\tProcessing modifications...")
	print("\t\tProcessing student:")
	for i, row in modificationsDF.iterrows(): #i represents the index, row represents the student (a row) at this index
		studentNumber = row["studentNumber"]
		numOccurrences = modificationsDF.studentNumber.value_counts()[studentNumber]  # The number of times this student appears in modificationsDF (including this occurrence)
		# print(i, studentNumber, numOccurrences, sep="\t")

		if numOccurrences == 2:
			studentIndexes = modificationsDF.index[modificationsDF["studentNumber"] == studentNumber].tolist()

			# if i == studentIndexes[0] - if it is the student's first occurrence/appearance in modificationsDF - this row is from currentStudentsDF
			# Do nothing - we shall process this student's changed details and/or course requests on the second occurrence

			if i == studentIndexes[1]:  # if it is the student's second occurrence/appearance in modificationsDF - this row is from modifiedStudentsDF
				print("\t\t\t", studentNumber, " - student has been modified", sep="")
				# Get their updated details and course requests and update it in the studentsDict
				# print("Second occurrence")
				studentDict = studentsDict[str(studentNumber)]

				studentDict["surname"] = row["surname"]
				studentDict["firstnames"] = row["firstnames"]
				studentDict["classificationArea"] = row["faculty"]
				studentDict["majorArea"] = row["qualification"]

				studentCurrentNumCourses = int(studentDict["numCourses"])
				studentCurrentNumProcessedCourses = int(studentDict["numProcessedCourses"])
				studentNewNumCourses = row["numCourses"]  # I set the data type of numCourses to 'int' when I read in the Excel file into the DataFrame
				studentNewNumProcessedCourses = 0

				studentNewRequestsDict = copy.deepcopy(studentDict)  # For studentsNewRequestsDict, which is for SeparateModifiedInputProcessing.py
				studentNewRequestsCourseRequestsDict = dict()
				studentNewRequestsNumProcessedCourses = 0

				# Get current course requests
				studentCourseRequestsDict = studentDict["courseRequests"]
				studentCourseRequestsIdsList = list(studentCourseRequestsDict.keys())

				studentCurrentProcessedCourses = list()  # course names of all the current processed courses of this student
				studentCurrentCourseToCRMapping = dict()  # key = course name; value = Course Request ID

				for courseRequestID in studentCourseRequestsIdsList:
					courseRequestDict = studentCourseRequestsDict[courseRequestID]
					courseName = courseRequestDict["courseName"]
					studentCurrentProcessedCourses.append(courseName)
					studentCurrentCourseToCRMapping[courseName] = courseRequestID
				# print(studentCurrentProcessedCourses)

				studentNewProcessedCourses = getStudentProcessedCourses(row, studentNewNumCourses, courseIdDict)
				studentNewNumProcessedCourses = len(studentNewProcessedCourses)
				# print(studentNewProcessedCourses)

				# Compare current processed courses to new processed courses
				for courseName in studentCurrentProcessedCourses:
					if courseName not in studentNewProcessedCourses:
						# Remove the course request of this course from the student's course requests
						courseRequestID = studentCurrentCourseToCRMapping[courseName]
						del studentCourseRequestsDict[courseRequestID]
						print("\t\t\t\t", courseName, " has been removed", sep="")


				for courseName in studentNewProcessedCourses:
					if courseName not in studentCurrentProcessedCourses:
						# Create and add a course request of this course to the student's course requests
						courseRequestDict = dict()

						courseRequestDict["priority"] = "0"
						courseRequestCourseID = courseIdDict[courseName]
						courseRequestDict["courseID"] = courseRequestCourseID
						courseRequestDict["courseName"] = courseName
						courseRequestDict["allocations"] = list()  # an empty list since this is a new course request (no allocations from the current solution)

						currentCourseRequestID += 1
						studentCourseRequestsDict[str(currentCourseRequestID)] = courseRequestDict
						studentNewRequestsCourseRequestsDict[str(currentCourseRequestID)] = courseRequestDict
						studentNewRequestsNumProcessedCourses += 1

						print("\t\t\t\t", courseName, " has been added", sep="")


				studentDict["numCourses"] = str(studentNewNumCourses)  # All 'primitive' values in the dict are strings
				studentDict["numProcessedCourses"] = str(studentNewNumProcessedCourses)

				numCourseRequests -= studentCurrentNumProcessedCourses
				numCourseRequests += studentNewNumProcessedCourses

				studentDict["courseRequests"] = studentCourseRequestsDict
				studentsDict[str(studentNumber)] = studentDict

				studentNewRequestsDict["numCourses"] = str(studentNewRequestsNumProcessedCourses)  # we can't actually get the number of new courses the student is enrolled for as the code above traverses through the processed courses from the modified Students input file
				studentNewRequestsDict["numProcessedCourses"] = str(studentNewRequestsNumProcessedCourses)
				studentNewRequestsDict["courseRequests"] = studentNewRequestsCourseRequestsDict
				studentsNewRequestsDict[str(studentNumber)] = studentNewRequestsDict

		else:  # if this student only appears once in modificationsDF
			print("\t\t\t", studentNumber, sep="", end=" - ")
			if studentNumber in currentStudentsDF["studentNumber"].values:  # If this only appearance is in currentStudentsDF
				# this student has been removed from the updated Students input, so remove them from the studentsDict
				print("student has been removed")
				studentNumProcessedCourses = int(studentsDict[str(studentNumber)]["numProcessedCourses"]) # The number of courses of this student that are processed and added (i.e. the courses that were specified in the problem input's Courses.xlsx file)
				numCourseRequests -= studentNumProcessedCourses
				numStudents -= 1
				del studentsDict[str(studentNumber)] # This will raise a KeyError exception if studentNumber is invalid, but it will always be valid for this case
			else:  # if studentNumber in modifiedStudentsDF["studentNumber"].values | If this only appearance is in modifiedStudentsDF
				# this student has been added to the updated Students input, so add them to the studentsDict by processing their details and course requests
				print("student has been added")

				studentDict = dict() # The dictionary for this student. The values element in studentsDict to the studentNumber key

				surname = row["surname"]
				studentDict["surname"] = surname
				firstnames = row["firstnames"]
				studentDict["firstnames"] = firstnames

				studentNumCourses = row["numCourses"]  # The number of courses that this student is registered for | I set the data type to 'int' when I read in the Excel file into the DataFrame
				studentDict["numCourses"] = str(studentNumCourses)  # All 'primitive' values in the dict are strings

				studentProcessedCourses = getStudentProcessedCourses(row, studentNumCourses, courseIdDict)

				studentNumProcessedCourses = len(studentProcessedCourses)  # The number of courses of this student that are processed and added (i.e. the courses that were specified in the problem input's Courses.xlsx file)
				studentDict["numProcessedCourses"] = str(studentNumProcessedCourses)  # All 'primitive' values in the dict are strings
				numCourseRequests += studentNumProcessedCourses

				faculty = row["faculty"]  # XML file: Student.Classification.area
				studentDict["classificationArea"] = faculty
				qualification = row["qualification"]  # XML file: Student.Major.area
				studentDict["majorArea"] = qualification

				studentCourseRequestsDict = dict()

				for courseName in studentProcessedCourses: # Each course is the name of the course for the course requests of the student that have been processed
					courseRequestDict = dict()

					courseRequestDict["priority"] = "0"
					courseRequestCourseID = courseIdDict[courseName]
					courseRequestDict["courseID"] = courseRequestCourseID
					courseRequestDict["courseName"] = courseName

					courseRequestDict["allocations"] = list()  # an empty list since this is a new course request (no allocations from the current solution)

					currentCourseRequestID += 1
					studentCourseRequestsDict[str(currentCourseRequestID)] = courseRequestDict
					print("\t\t\t\t", courseName, " has been added", sep="")



				studentDict["courseRequests"] = studentCourseRequestsDict

				studentsDict[str(studentNumber)] = studentDict
				studentsNewRequestsDict[str(studentNumber)] = studentDict  # Since this is a completely new student (all course requests are new) , we can assign studentDict directly
				numStudents += 1

	print("\tStudent modifications have been processed.")
	print("The modified Students input Excel file has been processed.")

	# Update the updated input dict: the numCourses, courseIdDict, and courseNameDict remain unchanged so we don't have to update them
	updatedInputDict["numStudents"] = numStudents
	updatedInputDict["numCourseRequests"] = numCourseRequests
	updatedInputDict["lastCourseRequestID"] = currentCourseRequestID
	updatedInputDict["studentsDictionary"] = studentsDict
	updatedInputDict["studentsNewRequestsDictionary"] = studentsNewRequestsDict  # For SeparateModifiedInputProcessing.py

	# for student in studentsDict.items():
	# 	print(student)

	return updatedInputDict


def generateUpdatedInputXmlFile(updatedInputDict: dict, inputXmlFilePath: str):
	"""
		Create an updated input data XML file (that is a partial solution) based on the updated input data (the
		unchanged/existing course requests from the current input data XML file are still assigned as is, the new course
		requests are unassigned/unallocated and the old course requests removed)

		:param updatedInputDict: the updated input data for this problem instance, containing a partial solution - a
		dictionary containing the number of students, the number of courses, the number of course requests and a
		sub-dictionary (studentsDict) containing the student details, course requests, and allocations from the current
		solution (for existing course requests)
		:param inputXmlFilePath: str: the file path of the current input data XML file. To be used to extract courses data
		:return: None
	"""
	# Convert values to strings as an XML file stores all attribute values as strings
	numStudents = str(updatedInputDict["numStudents"])
	numCourses = str(updatedInputDict["numCourses"])
	numCourseRequests = str(updatedInputDict["numCourseRequests"])
	lastCourseRequestID = str(updatedInputDict["lastCourseRequestID"])
	studentsDict = updatedInputDict["studentsDictionary"]
	courseIdDict = updatedInputDict["courseIDDict"]
	courseNameDict = updatedInputDict["courseNameDict"]

	print("\nGenerating updated input data XML file...")
	print("\tReading in and parsing the current input data XML file...")


	with open(inputXmlFilePath, "r") as inputXMLFile:
		inputXML = inputXMLFile.read()

	# Passing the current input and solution XML files to BeatifulSoup parsers
	inputBS = BeautifulSoup(inputXML, "xml")


	"""
	Create the updated XML input data file for this input
	"""

	# Create XML document with XML Prolog
	updatedInputFileXML = minidom.Document()

	# Student Sectioning
	sectioningElement = updatedInputFileXML.createElement("sectioning")  # Create the root element 'sectioning'

	""" 
		Add the attributes of the 'sectioning element' - this is the problem specification information along with the
		current input information. Extracting it from the current input data XML file
	"""
	currentInputSectioningTag = inputBS.find("sectioning") # Extract the 'sectioning' tag/element and its attributes from the current input data XML file (BS considers an XML element as a 'tag')

	currentVersion = currentInputSectioningTag.get("version")
	periodIndex = currentVersion.rfind(".")

	# Todo - ensure the Problem Specification XML file part in the comment below
	"""
		modVerNum is the modification version number of the modified Students input data XML file.
		The Problem Specification XML file, used to create the first/initial input data XML file for this problem
		instance should have the "version" attribute be either "0" or "<x>.0" so that modVerNum here matches up with the 
		modification version number of the modified Students input data XML file 
	"""
	if periodIndex < 0:
		modVerNum = int(currentVersion) + 1
		updatedVersion = str(modVerNum)
	else:  # updating the subversion instead if there is one
		modVerNum = int(currentVersion[periodIndex+1:]) + 1
		updatedVersion = currentVersion[:periodIndex+1] + str(modVerNum)


	sectioningElement.setAttribute("version", updatedVersion)

	sectioningElement.setAttribute("initiative", currentInputSectioningTag.get("initiative"))
	sectioningElement.setAttribute("term", currentInputSectioningTag.get("term"))
	sectioningElement.setAttribute("year", currentInputSectioningTag.get("year"))

	currentDateTime = time.ctime(time.time())  # current time as a string
	# timezone = time.localtime().tm_zone
	sectioningElement.setAttribute("created", currentDateTime)

	sectioningElement.setAttribute("nrDays", currentInputSectioningTag.get("nrDays"))
	sectioningElement.setAttribute("slotsPerDay", currentInputSectioningTag.get("slotsPerDay"))

	sectioningElement.setAttribute("numStudents", numStudents)
	sectioningElement.setAttribute("numCourses", numCourses)
	sectioningElement.setAttribute("numCourseRequests", numCourseRequests)
	sectioningElement.setAttribute("lastCourseRequestID", lastCourseRequestID)

	updatedInputFileXML.appendChild(sectioningElement)


	"""
		Create the 'offerings', 'students', and 'courses' sub-elements of the sectioning element 
		
		Even though I'll be adding the course id-name pairs (via the coursesElement) in the code before I add the 
		student course requests and allocations (via the studentsElement) [as I want to do all the data related to the 
		courses first], the 'students' element has been added here to the 'sectioning' element before the 'courses' 
		element, so in the XML file, the student's element will come before the 'courses' element, as I want (as in the 
		initial input data XML file, it was in the order of 'offerings', 'students' and 'courses')
	"""

	offeringsElement = updatedInputFileXML.createElement("offerings")
	sectioningElement.appendChild(offeringsElement)

	studentsElement = updatedInputFileXML.createElement("students")
	sectioningElement.appendChild(studentsElement)

	coursesElement = updatedInputFileXML.createElement("courses")
	sectioningElement.appendChild(coursesElement)


	print("\t\tExtracting courses data from current input data XML file and writing it to the updated input data XML file...")

	""" Process all course offerings (All LabSections for each Lab for each Course) """

	currentInputOfferingTags = currentInputSectioningTag.find_all("offering")

	for currentInputOfferingTag in currentInputOfferingTags:  # each offering is a Tag object
		offeringElement = updatedInputFileXML.createElement("offering")
		offeringElement.setAttribute("id", currentInputOfferingTag.get("id"))
		offeringsElement.appendChild(offeringElement)

		currentInputCourseTag = currentInputOfferingTag.find("course")  # There's only 1 "course" tag/element of this offering tag
		courseElement = updatedInputFileXML.createElement("course")
		courseElement.setAttribute("id", currentInputCourseTag.get("id"))
		courseElement.setAttribute("name", currentInputCourseTag.get("name"))
		courseElement.setAttribute("numLabs", currentInputCourseTag.get("numLabs"))
		offeringElement.appendChild(courseElement)

		currentInputConfigTag = currentInputOfferingTag.find("config")  # There's only 1 "config" tag/element of this offering tag
		configElement = updatedInputFileXML.createElement("config")
		configElement.setAttribute("id", currentInputConfigTag.get("id"))
		offeringElement.appendChild(configElement)

		currentInputSubpartTags = currentInputConfigTag.find_all("subpart")

		for currentInputSubpartTag in currentInputSubpartTags:
			subpartElement = updatedInputFileXML.createElement("subpart")
			subpartElement.setAttribute("id", currentInputSubpartTag.get("id"))
			subpartElement.setAttribute("itype", currentInputSubpartTag.get("itype"))
			subpartElement.setAttribute("courseLabNum", currentInputSubpartTag.get("courseLabNum"))
			configElement.appendChild(subpartElement)


			currentInputSectionTags = currentInputSubpartTag.find_all("section")

			for currentInputSectionTag in currentInputSectionTags:
				sectionElement = updatedInputFileXML.createElement("section")
				sectionElement.setAttribute("id", currentInputSectionTag.get("id"))
				sectionElement.setAttribute("courseLabSectionNum", currentInputSectionTag.get("courseLabSectionNum"))
				sectionElement.setAttribute("limit", currentInputSectionTag.get("limit"))
				subpartElement.appendChild(sectionElement)

				currentInputTimeTag = currentInputSectionTag.find("time")  # There's only 1 "time" tag/element of this offering tag
				timeElement = updatedInputFileXML.createElement("time")
				timeElement.setAttribute("days", currentInputTimeTag.get("days"))
				timeElement.setAttribute("start", currentInputTimeTag.get("start"))
				timeElement.setAttribute("length", currentInputTimeTag.get("length"))
				timeElement.setAttribute("dates", currentInputTimeTag.get("dates"))
				timeElement.setAttribute("sessionDay", currentInputTimeTag.get("sessionDay"))
				sectionElement.appendChild(timeElement)


	""" Add the course id-name pairs"""
	for courseID in range(1, int(numCourses)+1):
		courseElement = updatedInputFileXML.createElement("course")
		courseElement.setAttribute("id", str(courseID))
		courseElement.setAttribute("courseName", courseNameDict[str(courseID)])
		coursesElement.appendChild(courseElement)

	print("\t\tCourses data has been written to the updated input data XML file.")

	print("\tWriting updated students data to the updated input data XML file...")


	""" Process all student enrollments (lab sessions requests and section allocations) """

	studentNumbersList = list(studentsDict.keys())

	for studentNumber in studentNumbersList:
		studentDict = studentsDict[studentNumber]

		# Add the student's details

		studentElement = updatedInputFileXML.createElement("student")
		studentElement.setAttribute("id", studentNumber)
		studentElement.setAttribute("surname", studentDict["surname"])
		studentElement.setAttribute("firstnames", studentDict["firstnames"])
		studentElement.setAttribute("numCourses", studentDict["numCourses"])
		studentElement.setAttribute("numProcessedCourses", studentDict["numProcessedCourses"])
		studentsElement.appendChild(studentElement)

		classificationElement = updatedInputFileXML.createElement("classification")
		classificationElement.setAttribute("area", studentDict["classificationArea"])
		studentElement.appendChild(classificationElement)

		majorElement = updatedInputFileXML.createElement("major")
		majorElement.setAttribute("area", studentDict["majorArea"])
		studentElement.appendChild(majorElement)


		# Add the student's course requests (and allocations, if any, from current solution)

		studentCourseRequestsDict = studentDict["courseRequests"]
		studentCourseRequestsIdsList = list(studentCourseRequestsDict.keys())

		for courseRequestID in studentCourseRequestsIdsList:
			courseRequestDict = studentCourseRequestsDict[courseRequestID]

			courseRequestElement = updatedInputFileXML.createElement("course")
			courseRequestElement.setAttribute("id", courseRequestID)
			courseRequestElement.setAttribute("priority", courseRequestDict["priority"])
			courseRequestElement.setAttribute("course", courseRequestDict["courseID"])
			courseRequestElement.setAttribute("courseName", courseRequestDict["courseName"])
			studentElement.appendChild(courseRequestElement)

			courseRequestAllocationsList = courseRequestDict["allocations"]

			if courseRequestAllocationsList:  # if courseRequestAllocationsList contains any elements (if it is not empty)
				bestElement = updatedInputFileXML.createElement("best")
				bestElement.setAttribute("course", courseRequestDict["courseID"])
				courseRequestElement.appendChild(bestElement)

				for allocatedSectionID in courseRequestAllocationsList:
					sectionElement = updatedInputFileXML.createElement("section")
					sectionElement.setAttribute("id", allocatedSectionID)
					bestElement.appendChild(sectionElement)



	print("\tThe updated students data has been written to the updated input data XML file...")


	updatedInputFileXML = updatedInputFileXML.toprettyxml(indent="\t")

	print("\nUpdated input data XML file has been generated.")

	# Todo - uncomment this out after doing experimentation, and comment out the part below
	# updatedXmlFileName = inputXmlFilePath  # Overwrite current input data XML file (user system version)

	# For my experimentation process, I will be using a different XML file name for the updated input data XML file, to
	# allow for easy comparison, and multiple independent solver runs (with different modified Students input file) on the
	# same input data XML file
	periodIndex = inputXmlFilePath.rfind(".xml")
	updatedXmlFileName = inputXmlFilePath[:periodIndex] + "-updated-1.xml"


	# Write the updated input data XML file
	with open(updatedXmlFileName, "w") as updatedXmlFile:
		updatedXmlFile.write(updatedInputFileXML)

	print("Updated input data XML file has been written to file: '" + updatedXmlFileName + "'.")



# Run the main method if this python file is being executed/run directly (either from IDE or Command Line)
if __name__ == '__main__':
	main()
	print("ModifiedInputProcessing.py has been executed")
