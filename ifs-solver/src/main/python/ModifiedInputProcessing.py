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
	problemInstanceName = "2020-Sem1-CAES-Wvl-no-extra-requests-testing"

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
	currentSolutionDict = processCurrentSolution(inputXmlFilePath, currentSolutionFilePath)

	""" Process the modified Students input Excel file"""
	updatedInputDict = processModifiedStudentsData(modifiedStudentsFilePath, currentSolutionDict)

	# Generate/Produce the updated input data XML file


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
		:return: currentSolutionFilePath: str:
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


def getModifiedStudentsFilePath(problemInstanceDirectoryPath: str):
	"""
		Get the the correct file name of the modified Students input Excel file from the user, and return
		the file path of the modified Students input file
		:param problemInstanceDirectoryPath: str:
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


def processCurrentSolution(inputXmlFilePath: str, currentSolutionFilePath: str):
	"""
		Read in the current input data XML file and the current solution XML file, and process the data into a dictionary
		that stores all the student details, their course requests and allocated/assigned sections for each of their
		requests from the current solution.

		:param inputXmlFilePath: str: the file path of the current input data XML file
		:param currentSolutionFilePath: str: the file path of the current solution XML file
		:return: currentSolutionDict: , a dictionary containing the number of students, the number of courses, the number
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
	print("\tObtaining student details, their course requests, and allocated sections...")
	print("\t\tProcessing student:")
	inputstudentsTags = inputBS.find_all("student")  # Extract all 'student' tags from the input data XML file

	for student in inputstudentsTags: # each student is a Tag object
		studentDict = dict() # A dictionary to store the details (attributes from the input data XML file) of this student. This will be the value to the studentNumber key in studentsDict

		# Since all values for attributes in an XML file are strings, all the values obtained below are strings, and will be stored as strings

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
	currentSolutionDict["lastCourseRequestID"] = lastCourseRequestID
	currentSolutionDict["studentsDictionary"] = studentsDict

	return currentSolutionDict


def processModifiedStudentsData(modifiedStudentsFilePath: str, currentSolutionDict: dict):
	"""
		Read in the modified Students input Excel file, the dictionary containing the current solution (that stores all
		the student details, their course requests and allocated/assigned sections for each of their requests),
		process the modified Students data (the updated students and course requests details) by updating the dictionary,
		and return the updated dictionary, which represents the updated input for the problem instance.
		This updated dictionary (updatedInputDict) represents a partial solution containing the allocations of the
		unchanged course requests from the current solution.

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


	modifiedStudentsDF = pd.read_excel(modifiedStudentsFilePath, sheet_name=0, header=0, engine="openpyxl", dtype={'numCourses':int})

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
	if modVerNum == 1: # the first modified Students file
		currentStudentsFilePath = modifiedStudentsFilePath[:dashIndex] + ".xlsx"
	else:
		currentStudentsFilePath = modifiedStudentsFilePath[:dashIndex+1] + str(modVerNum-1) + ".xlsx"
	print(currentStudentsFilePath)
	currentStudentsDF = pd.read_excel(currentStudentsFilePath, sheet_name=0, header=0, engine="openpyxl", dtype={'numCourses':int})


	"""
		Get the modifications (to student registrations) made to the current Students input file (which are reflected in 
		the modified students  input file) by finding rows that are not in both Data Frames that represent these 2 files 
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
	modificationsDF = pd.concat([currentStudentsDF, modifiedStudentsDF]).drop_duplicates(keep=False, ignore_index=True)


	numModifications = len(modificationsDF)

	print(modificationsDF)
	print(modificationsDF[0:5].values)
	print(modificationsDF.studentNumber.value_counts()[220112256]) #Number of times the value 220112256 appears in the studentNumber column

	"""
		In the updated input data XML file, we want the unchanged course requests to maintain their same course request 
		IDs (so that it is easier to check if existing section allocations were preserved in the updated solution).
		So if a course request of an existing student gets deleted (or we remove an entire student), we will not reset 
		the course request IDs by 'shifting down' the IDs of all the course requests that follow. 
		And also if a course request(s) gets added, we will not be 'shifting up' the IDs of all the course requests that 
		follow.
		So all the new course requests that get added (even for existing students with existing course requests) will 
		have their course request ID's be after than the last course request ID used in the current input data XML file.
	"""
	currentCourseRequestID = lastCourseRequestID + 1

	for i, row in modificationsDF.iterrows(): #i represents the index
		studentNumber = row["studentNumber"]
		numOccurrences = modificationsDF.studentNumber.value_counts()[studentNumber] # The number of times this student appears in modificationsDF (including this occurrence)
		print(i, studentNumber, numOccurrences, sep="\t")

		if numOccurrences == 2:
			studentIndexes = modificationsDF.index[modificationsDF["studentNumber"] == studentNumber].tolist()

			if i == studentIndexes[0]:  # if it is the student's first appearance in modificationsDF
				# Do nothing ?
				print("First occurrence")
			else:  # if it is the student's second appearance in modificationsDF
				# Get their updated details and course requests and update it in the studentsDict
				print("Second occurrence")
		else:  # if this student only appears once in modificationsDF
			print("Only appearance")
			if studentNumber in currentStudentsDF["studentNumber"].values:  # If this only appearance is in currentStudentsDF
				# this student has been removed from the updated Students input
				# so remove them from the studentsDict
				print("IN currentStudentsDF")
				print(studentsDict[str(studentNumber)])
				numStudentProcessedCourses = int(studentsDict[str(studentNumber)]["numProcessedCourses"])
				print(numStudentProcessedCourses)
				numCourseRequests -= numStudentProcessedCourses
				del studentsDict[str(studentNumber)]
				print(studentsDict[str(studentNumber)])
			else: # if studentNumber in modifiedStudentsDF["studentNumber"].values # If this only appearance is in modifiedStudentsDF
				# this student has been added to the updated Students input
				# so add them from the studentsDict
				print("IN modifiedStudentsDF")

	#for j in indexesOfThisStudent:
		#	modificationsDF.drop(index=j, inplace=True)
		#if :
		#	modificationsDF.drop(index=i, inplace=True)
	print(modificationsDF)

	#print(modificationsDF.loc[2545, "studentNumber"])

	# Consider also writing to the input data XML file here to improve efficiency / lower the execution time (doing the writing after processing
	# the entire data first will lead to double execution time as we will have to traverse the entire dictionary again from the beginning

	# Todo - what numbers do i give the course requests in the updated input data XML file (really applicable when this isnt the first modification - CANT start from numCourseRequests+! for first new course request)
	# maybe add a filed to the sectioning element that states the last course request id used?

	return updatedInputDict


# Todo - update (re processes) the input data XML file for all other problem instances (based on additions made to InputProcessing.py on 22/09/2021

main()
#processModifiedStudentsData("src/main/resources/input/2020-Sem1-CAES-Wvl-no-extra-requests/Students-1.xlsx")
#modifiedStudentsDF = pd.read_excel("src/main/resources/input/2020-Sem1-CAES-Wvl-no-extra-requests/Students.xlsx", sheet_name=0, header=0, engine="openpyxl", dtype={'numCourses':int})
#print(modifiedStudentsDF)

