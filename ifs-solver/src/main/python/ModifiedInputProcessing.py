import pandas as pd # Following naming convention
from bs4 import BeautifulSoup # For reading from XML files (bs4 needs to be installed first)
from xml.dom import minidom # For creating and writing to XML files

#Installed the openpyxl, beautifulsoup4 and lxml packages

"""
	Process a modified Students.xslx input file and the initial solution file (solution.xml),
	and produce an updated XML file (input data file) that is a partial solution (the unchanged course requests are still
	assigned as is, the new course requests are unassigned/unallocated and the old course requests removed)

	Since the solution file (solution.xml) of the solver removes the student number and names attributes that I added to the
	initial input data XML file, I cannot compare/link students directly to the Students.xslx file as new students added (the
	students are sorted in student number ascending order) or students removed will mean that the student id number in the XML file
	may not necessarily match up with that <number> student in the Students.xlsx file.

	I also want the id attribute of the students to be preserved from the initial input data XML file so that the comparison
	for perturbations is simpler - so new students added to the Students.xlsx file (their position in the file will be based
	on their student number) need to be processed/added to the end of the updated input data XML file.
	
	[However, the student id's of the solution.xml file will match up with the student id's in the initial input data XML file,
	ie. an existing student will have the same student id in both files.]
"""

def main():
	"""

		:return: None
	"""

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

	#problemInstanceName = input("Enter problem instance name: ")
	problemInstanceName = "2020-Sem1-CAES-Wvl-no-extra-requests"

	problemInstanceDirectoryPath = "src/main/resources/input/" + problemInstanceName
	inputXmlFilePath = problemInstanceDirectoryPath + "/" + problemInstanceName + ".xml" # input data XML file
	problemInstanceSolutionsFile = problemInstanceDirectoryPath + "/Solutions.txt"

	problemInstanceSolutions = list()

	with open(problemInstanceSolutionsFile) as solutionsFile:
		for line in solutionsFile:
			line = line[:len(line)-2]  # Remove the "\n" part at the end of the string
			problemInstanceSolutions.append(line)

	latestSolution = problemInstanceSolutions[-1] # The last element of the list
	problemInstanceLatestSolutionDirectoryPath = problemInstanceDirectoryPath + "/" + latestSolution
	latestSolutionFilePath = problemInstanceLatestSolutionDirectoryPath + "/solution.xml"

	studentsDict = dict()
	studentsDict.clear()

	studentCourseRequestsList = list()
	courseRequest = {'courseRequestID': , 'courseID': , 'courseName': , 'allocatedSection':}
	studentCourseRequestsList.append(courseRequest)

	studentsDict[studentNumber] = {'id':, 'surname': , 'firstnames': , 'numCourses': , 'classificationArea': , 'majorArea': , studentCourseRequestsList}




main()
