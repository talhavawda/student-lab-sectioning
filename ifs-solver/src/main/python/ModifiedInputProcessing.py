import pandas as pd # Following naming convention
from bs4 import BeautifulSoup # For reading from XML files (bs4 needs to be installed first)
from xml.dom import minidom # For creating and writing to XML files

#Installed the openpyxl, beautifulsoup4 and lxml packages (lxml is a parser)

"""
	Process the current solution file (solution.xml) along with the input data XML file that was used to obtain it,
	a modified/updated Students.xlsx input file, and produce an updated input data XML file that is a partial solution 
	(the unchanged course requests from the current input data XML file are still assigned as is, the new course 
	requests are unassigned/unallocated and the old course requests removed)
	
	This current input data XML file and current solution file do not have to be the first/initial solution to the problem instance.
	This means that the user can modify the Students.xlsx input file as many times as they want and obtain a new updated solution. 
	
	Everytime an updated input data XML file is generated based on the modified/updated Students input, it replaces/overrides
	the previous input data XML file (as my solver code (Main.java) assumes that the name of input data XML file is the same as that
	of the problem instance). So over here, we make the same assumption and the input data XML file that we obtained is the 
	current one instead of the first input data XML file for this problem instance.
	If the user wants to obtain a completely new solution from scratch, they can rerun the InputProcessing.py script
	to obtain an input data XML file will all course requests being unassigned.
	The reason why I ask the user to select the current solution to work with (and not also for the input XML file, and not
	just taking the latest solution) is that the solver can be run many times on the current input data XML file and they
	may not want to use the last solution obtained. 
	
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
	problemInstanceSolutionsFile = problemInstanceDirectoryPath + "/Solutions.txt"

	studentsFilePath = "src/main/resources/input/" + problemInstanceName + "/Students.xlsx" # Todo - get file path of the modified students file


	""" Get the solution of this problem instance that we want to work with (the current solution) """

	problemInstanceSolutions = list()
	solutionIndex = 0

	print("Solutions of this problem instance:")

	with open(problemInstanceSolutionsFile) as solutionsFile:
		for line in solutionsFile:
			line = line[:len(line)-1]  # Remove the "\n" part at the end of the string | Doing -2 cuts out the last digit in the solution name so it seems that '\n' is being treated as one character
			problemInstanceSolutions.append(line)
			print("\t", solutionIndex,":", line)
			solutionIndex += 1

	print()

	try:
		currentSolution = input("Enter the solution (it's number above) that you want to use as the current solution to\nprocess with the modified Students input to obtain the updated solution: ")

		if currentSolution < 0 or currentSolution > solutionIndex:
			currentSolution = problemInstanceSolutions[-1] # Default is the last element of the list (the latest solution that was generated using the solver) | Alt. we can use solutionIndex

	except TypeError:
		currentSolution = problemInstanceSolutions[-1] # Default is the last element of the list (the latest solution that was generated using the solver)

	problemInstanceCurrentSolutionDirectoryPath = problemInstanceDirectoryPath + "/" + currentSolution
	currentSolutionFilePath = problemInstanceCurrentSolutionDirectoryPath + "/solution.xml"



	# Todo - get and read in the modified Students.xlsx input file (See InputProcessing.py)



	studentsDict = processCurrentSolution(inputXmlFilePath, currentSolutionFilePath)


# END main()

def processCurrentSolution(inputXmlFilePath, currentSolutionFilePath):
	"""
		Read in the current input data XML file and the current solution XML file, and process the data into a dictionary
		that stores all the student details, course requests and assigned sections

		:param inputXmlFilePath: the file path of the current input data XML file
		:param currentSolutionFilePath: the file path of the current solution XML file
		:return: studentsDict, a dictionary of student details, their course requests, and assigned sections for each of their requests
		from the current solution.
	"""

	with open(inputXmlFilePath, "r") as inputXMLFile:
		inputXML = inputXMLFile.read()

	with open(currentSolutionFilePath, "r") as solutionXMLFile:
		solutionXML = solutionXMLFile.read()

	# Passing the current input and solution XML files to BeatifulSoup parsers
	inputBS = BeautifulSoup(inputXML, "xml")
	solutionBS = BeautifulSoup(solutionXML, "xml")

	"""
		Maintain a dictionary (Map) of student details, their course requests, and assigned sections for each of their requests
		from the current solution. 
		
		We are making the key be the student number (or ID, according to the institute. This is also the id attribute value of the student
		in the XML file). 
		Usung the students' student number as the key helps us quickly check if a student we encounter in the 
		modified Students.xlsx file already exists in our current solution or is a new student.
		
		We will initially populate it with the data from the current input data XML file and current solution XML file,
		and will update it using the modified Students.xlsx input file. 
	"""
	studentsDict = dict()
	studentsDict.clear()

	inputSectioningTag = inputBS.find("sectioning") # Extract the 'sectioning' tag/element and its attributes from the input data XML file (BS considers an XML element as a 'tag')
	numStudents = int(inputSectioningTag.get("numStudents"))
	numCourses = int(inputSectioningTag.get("numCourses"))
	numCourseRequests = int(inputSectioningTag.get("numCourseRequests"))


	"""Obtain student details and course requests from the current input data XML file and process them into studentsDict"""


	"""Obtain assigned sections for student course requests from the current solution XML file and process them into studentsDict"""


	return studentsDict



	#studentCourseRequestsList = list()

	# Todo - each course can have multiple labs so remove allocatedSection field and add a list of labs to hold the allocatedSection value for each lab

	#courseRequest = {'courseRequestID': , 'courseID': , 'courseName': , 'allocatedSection':}
	#studentCourseRequestsList.append(courseRequest)
	#studentsDict[studentNumber] = {'id':, 'surname': , 'firstnames': , 'numCourses': , 'classificationArea': , 'majorArea': , studentCourseRequestsList}



# Todo - update (re processes) the input data XML file for all other problem instances (based on additions made to InputProcessing.py on 22/09/2021

main()
