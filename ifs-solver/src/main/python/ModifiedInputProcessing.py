import pandas as pd # Following naming convention
from bs4 import BeautifulSoup # For reading from XML files (bs4 needs to be installed first)
from xml.dom import minidom # For creating and writing to XML files

#Installed the openpyxl, beautifulsoup4 and lxml packages (lxml is a parser)

"""
	Process the current solution file (solution.xml) along with the input data XML file that was used to obtain it,
	a modified/updated Students input file, and produce an updated input data XML file that is a partial solution 
	(the unchanged course requests from the current input data XML file are still assigned as is, the new course 
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
	problemInstanceName = "2020-Sem1-CAES-Wvl-no-extra-requests"

	problemInstanceDirectoryPath = "src/main/resources/input/" + problemInstanceName
	inputXmlFilePath = problemInstanceDirectoryPath + "/" + problemInstanceName + ".xml" # current input data XML file
	problemInputInstanceSolutionsFile = problemInstanceDirectoryPath + "/CurrentSolutions.txt"


	""" Get the solution of this problem instance's input data XML file instance that we want to work with (the current solution, to the current input data XML file) """

	problemInstanceSolutions = list()
	solutionIndex = 0

	print("Solutions of this problem instance's input data XML file instance:")

	with open(problemInputInstanceSolutionsFile, "r") as solutionsFile:
		for line in solutionsFile:
			line = line[:len(line)-1]  # Remove the "\n" part at the end of the string | Doing -2 cuts out the last digit in the solution name so it seems that '\n' is being treated as one character
			problemInstanceSolutions.append(line)
			print("\t", solutionIndex,":", line)
			solutionIndex += 1
		solutionsFile.close()

	print()

	try:
		currentSolution = input("Enter the number of the solution that you want to use as the current solution to\nprocess with the modified Students input to obtain the updated solution: ")

		if currentSolution < 0 or currentSolution > solutionIndex:
			currentSolution = problemInstanceSolutions[-1] # Default is the last element of the list (the latest solution that was generated using the solver) | Alt. we can use solutionIndex

	except TypeError:
		currentSolution = problemInstanceSolutions[-1] # Default is the last element of the list (the latest solution that was generated using the solver)

	currentSolutionFilePath = getCurrentSolutionFilePath(currentSolution, problemInstanceDirectoryPath)


	# Get the modified Students input file
	modifiedStudentsFilePath = getModifiedStudentsFilePath(problemInstanceDirectoryPath)


	""" Process the current input data and solution XML files and store them in a dictionary """
	studentsDict = processCurrentSolution(inputXmlFilePath, currentSolutionFilePath)

	""" Process the modified Students input Excel file"""


	# Write the input data XML file

	# Reset/Overwrite CurrentSolutions.txt file to an empty file
	currentSolutionsFile = open(problemInputInstanceSolutionsFile, "w")
	#currentSolutionsFile.write("") # The above line will overwrite so I don't need this line
	currentSolutionsFile.close()


# END main()


def isEndofMonth(day: int, month: int, year: int):
	"""
		Determine whether the current day of a month is the last day of that month or not.
		Assume day and month are valid values (the initial date-time we got as the initial solution is a valid date-time
		and  we are validating the date-time when incrementing the date-time by 1 second).

		:param day: day of a month (as an int). Range: 1-31
		:param month: month of a year (as an int). Range: 1-12
		:param year: year (as a 2-digit int). Range: 0-99
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


def getCurrentSolutionFilePath(currentSolution, problemInstanceDirectoryPath):
	"""
		The actual folder name (the current  date and time that the solver started, in the yymmdd_hhmmss format) of the
		directory of the current solution instance may not be exactly the same as the name I got from the CurrentSolutions.txt file.
		In my Main.java program where I ran the solver on the current problem instance's input data XML file, I obtained
		the current date and time just before running the solver, and stored it in the CurrentSolutions.txt file thereafter.
		So the actual folder name of the solution (that the solver obtained) may possibly be 1 (or a few) second later than
		the current date-time that I obtained and stored.
		So if the current solution path doesn't exist, increment the date-time of the current solution by 1 second each
		time till the path is valid.

		:param currentSolution: the current solution name obtained from the CurrentSolutions.txt file
		:param problemInstanceDirectoryPath:
		:return: currentSolutionFilePath
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

	return currentSolutionFilePath


def getModifiedStudentsFilePath(problemInstanceDirectoryPath):
	"""
		Get the the correct file name of the modified Students input Excel file from the user, and return
		the file path of the modified Students input file
		:param problemInstanceDirectoryPath:
		:return: modifiedStudentsFilePath
	"""
	while True:
		try:
			modVerNum = input("Enter the modification version number of the modified Students input file that you want to process: ")
			modifiedStudentsFilePath = problemInstanceDirectoryPath + "/Students-" + modVerNum + ".xlsx"
			modifiedStudentsFile = open(modifiedStudentsFilePath, "r")
			break  # If the file was opened successfully
		except FileNotFoundError:
			print("Invalid modification version number entered. You will be prompted to re-enter\n")
		finally:
			modifiedStudentsFile.close()

	print("Modified Students file:\t", "Students-" + modVerNum + ".xlsx", end="\n\n")
	return modifiedStudentsFilePath


def processCurrentSolution(inputXmlFilePath, currentSolutionFilePath):
	"""
		Read in the current input data XML file and the current solution XML file, and process the data into a dictionary
		that stores all the student details, their course requests and allocated/assigned sections and assigned sections
		for each of their requests from the current solution.

		:param inputXmlFilePath: the file path of the current input data XML file
		:param currentSolutionFilePath: the file path of the current solution XML file
		:return: currentSolutionDict, a dictionary containing the number of students, the number of courses, the number
		of course requests and a sub-dictionary containing the student details, requests and allocations, from the current
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
	solutionBS = BeautifulSoup(solutionXML, "xml")

	print("\tFiles have been read in and parsed.")


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


	"""
		Obtain student details and course requests from the current input data XML file, the allocated/assigned sections 
		for student course requests from the current solution XML file and process them into studentsDict
	"""
	print("\tObtaining student details, their course requests, and allocated sections...")
	print("\t\tProcessing student:")
	inputstudentsTags = inputBS.find_all("student")  # Extract all 'student' tags from the input data XML file

	for student in inputstudentsTags: # each student is a Tag object
		studentDict = dict() # A dictionary to store the details (attributes from the input data XML file) of this student. This will be the value to the studentNumber key in studentsDict

		studentNumber = student.get("id")
		solutionStudentTag = solutionBS.find("student", id=studentNumber) # Get the student tag/element of this student in the solution.xml file | Source: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#the-keyword-arguments
		print("\t\t\t", studentNumber)

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

		studentCourseRequestsList = list() # A list of dictionaries, each dictionary representing a course request
		studentCourseRequestsTags = student.find_all("course")

		for courseRequest in studentCourseRequestsTags:
			courseRequestDict = dict() # Each key is an attribute of this course request and the value is the corresponding value of the key

			courseRequestID = courseRequest.get("id")
			courseRequestDict["courseRequestID"] = courseRequestID
			courseRequestPriority = courseRequest.get("priority")
			courseRequestDict["priority"] = courseRequestPriority
			courseRequestCourseID = courseRequest.get("course")
			courseRequestDict["courseID"] = courseRequestCourseID
			courseRequestCourseName = courseRequest.get("courseName")
			courseRequestDict["courseName"] = courseRequestCourseName

			solutionStudentCourseRequestTag = solutionStudentTag.find("course", id=courseRequestID) # The course request tag/element of this course request of thus student

			courseRequestAllocationsList = list() # To store the allocated sections for each subpart class (Lab) of this course (Each course can have multiple labs, with (at most) one allocated section for each lab
			courseRequestAllocationsTags = solutionStudentCourseRequestTag.find_all("section")

			for sectionAllocation in courseRequestAllocationsTags:
				sectionID = sectionAllocation.get("id")
				courseRequestAllocationsList.append(sectionID)

			courseRequestDict["allocations"] = courseRequestAllocationsList

			studentCourseRequestsList.append(courseRequestDict)

		studentDict["courseRequests"] = studentCourseRequestsList

		studentsDict[studentNumber] = studentDict

	print("\n\tStudent details, course requests, and section allocations have been obtained.")
	print("Current input data and solution XML files have been processed.")


	currentSolutionDict = dict()
	currentSolutionDict["numStudents"] = numStudents
	currentSolutionDict["numCourses"] = numCourses
	currentSolutionDict["numCourseRequests"] = numCourseRequests
	currentSolutionDict["studentsDictionary"] = studentDict

	return currentSolutionDict




# Todo - update (re processes) the input data XML file for all other problem instances (based on additions made to InputProcessing.py on 22/09/2021

main()
