import pandas as pd # Following naming convention
from bs4 import BeautifulSoup # For reading from XML files (bs4 needs to be installed first)
from xml.dom import minidom # For creating and writing to XML files

#Installed the openpyxl, beautifulsoup4 and lxml packages

"""
	Process a modified Students.xlsx input file, the initial input data XML file, and the initial solution file (solution.xml),
	and produce an updated XML file (input data file) that is a partial solution (the unchanged course requests are still
	assigned as is, the new course requests are unassigned/unallocated and the old course requests removed)

"""

def main():
	"""

		:return: None
	"""


	#problemInstanceName = input("Enter problem instance name: ")
	problemInstanceName = "2020-Sem1-CAES-Wvl-no-extra-requests"

	problemInstanceDirectoryPath = "src/main/resources/input/" + problemInstanceName
	inputXmlFilePath = problemInstanceDirectoryPath + "/" + problemInstanceName + ".xml" # input data XML file
	problemInstanceSolutionsFile = problemInstanceDirectoryPath + "/Solutions.txt"

	studentsFilePath = "src/main/resources/input/" + problemInstanceName + "/Students.xlsx"

	problemInstanceSolutions = list()

	with open(problemInstanceSolutionsFile) as solutionsFile:
		for line in solutionsFile:
			line = line[:len(line)-2]  # Remove the "\n" part at the end of the string
			problemInstanceSolutions.append(line)

	latestSolution = problemInstanceSolutions[-1] # The last element of the list
	problemInstanceLatestSolutionDirectoryPath = problemInstanceDirectoryPath + "/" + latestSolution
	latestSolutionFilePath = problemInstanceLatestSolutionDirectoryPath + "/solution.xml"


	"""
		Read in the initial input data XML file, initial solution XML file, and the modified Students.xlsx input file
	"""

	with open(inputXmlFilePath, "r") as inputXMLFile:
		inputXML = inputXMLFile.read()

	with open(latestSolutionFilePath, "r") as solutionXMLFile:
		solutionXML = solutionXMLFile.read()


	# Todo - read in the modified Students.xlsx input file (See InputProcessing.py)

	# Todo - update (re processes) the input data XML file for all other problem instances (based on additions made to InputProcessing.py on 22/09/2021


	"""
		Maintain a dictionary (Map) of student details, their course requests, and assigned sections for each of their requests
		from the initial solution. 
		
		We are making the key be the student number (or ID, according to the institute. This differs from the id attribute of the student
		in the XML file). The id attribute orders the students in that XML file and does not help us with identifying a specific student. 
		This also helps us quickly check if a student we encounter in the modified Students.xlsx file already exists in
		our initial solution or is a new student.
		
		We will initially populate it with the data from the initial input data XML file and initial solution XML file,
		and will update it using the modified Students.xlsx input file. 
	"""
	studentsDict = dict()
	studentsDict.clear()





	studentCourseRequestsList = list()

	# Todo - each course can have multiple labs so remove allocatedSection field and add a list of labs to hold the allocatedSection value for each lab
	courseRequest = {'courseRequestID': , 'courseID': , 'courseName': , 'allocatedSection':}
	studentCourseRequestsList.append(courseRequest)

	studentsDict[studentNumber] = {'id':, 'surname': , 'firstnames': , 'numCourses': , 'classificationArea': , 'majorArea': , studentCourseRequestsList}




main()
