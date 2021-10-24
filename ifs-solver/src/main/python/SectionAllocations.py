from bs4 import BeautifulSoup  # For reading from XML files (bs4 needs to be installed first)
from xml.dom import minidom  # For creating and writing to XML files

"""
	Process a solution file to obtain the number of course requests for each course, the total capacity across all sections
	of each of its labs, and the number of allocations for each of its lab sections, and append this info to the end of 
	the solution xml file.
"""
# current Assumption - each course only has 1 lab, with possibly many sections

def main():

	#problemInstanceName = input("Enter problem instance name: ")
	problemInstanceName = "2020-Sem1-CAES-Wvl-no-conflicts"

	problemInstanceDirectoryPath = "src/main/resources/input/" + problemInstanceName
	inputXmlFilePath = problemInstanceDirectoryPath + "/" + problemInstanceName + ".xml"  # initial input data XML file for the problem instance


	""" Get the name of the solution we want to work with """

	while True:
		try:
			solutionName = input("Enter the name of the solution (format: yymmdd_hhmmss) that you want to use process to obtain the Section Allocations data: ")
			solutionFilePath = problemInstanceDirectoryPath + "/" + solutionName + "/solution.xml"  # the file path of the solution.xml file of this solution
			open(solutionFilePath, "r")
			break  # solutionFilePath is valid

		except FileNotFoundError:
			print("Solution folder not found in the problem instance's directory. You will be prompted to re-enter the name of the solution.")
			print("Please ensure that the solution's folder is located in this problem instance's directory.\n")

	""" Process the solution's XML file and obtain the courses and allocations data """
	allocationsDict = processSolution(inputXmlFilePath, solutionFilePath)

	""" Write the allocations data to the end of the solution's XML file and display it to the console """


def processSolution(inputXmlFilePath: str, solutionFilePath: str):
	"""
		Read on the solution's XML file and process the data into a dictionary that stores the courses' id-name mappings,
		num course requests, section capacities, and section allocations

		:param inputXmlFilePath: str: the file path of the initial input data XML file
		:param solutionFilePath: str: the file path of the current solution XML file
		:return: allocationsDict: a dictionary containing the courses info, num course requests, section limits, and section
		allocations
	"""

	print("\tReading in and parsing the input data and solution XML files...")

	with open(inputXmlFilePath, "r") as inputXMLFile:
		inputXML = inputXMLFile.read()

	with open(solutionFilePath, "r") as solutionXMLFile:
		solutionXML = solutionXMLFile.read()

	# Passing the input data and solution XML files to BeatifulSoup parsers
	inputBS = BeautifulSoup(inputXML, "xml")
	solutionBS = BeautifulSoup(solutionXML, "xml")

	print("\tFiles have been read in and parsed.")


	"""
		allocationsDict: A dictionary (Map) of the courses, their labs and sections, and section allocations
		key = course ID; value = a dictionary of the course's data
	"""
	allocationsDict = dict()
	allocationsDict.clear()


	""" Since the solution's XML file doesn't contain the course names, we'll need to obtain it from the input data XML file of this problem instance """
	inputCoursesTag = inputBS.find("courses") # Extract the 'courses' tag/element and its attributes from the input data XML file (BS considers an XML element as a 'tag')
	courseMappingsTags = inputCoursesTag.find_all("course")

	for course in courseMappingsTags:  # Each course is a tag object
		courseDict = dict()

		courseID = course.get("id")
		courseName = course.get("courseName")

		courseDict["courseName"] = courseName
		allocationsDict[courseID] = courseDict


	""" Process the courses data from the solution XML file """

	solutionOfferingsTag = solutionBS.find("offerings")  # Extract the 'offerings' tag/element and its attributes from the solution XML file

	solutionOfferingTags = solutionOfferingsTag.find_all("offering")

	for offering in solutionOfferingTags: # each offering contains a course and the configuration for that course
		solutionCourseTag = offering.find("course")
		courseID = solutionCourseTag.get("id")

		solutionConfigTag = offering.find("config")

		courseDict = allocationsDict[courseID]
		labsDict = dict()
		numLabs = 0
		solutionConfigSubpartTags = solutionConfigTag.find_all("subpart")

		for subpart in solutionConfigSubpartTags:
			numLabs += 1
			labDict = dict()
			labID = subpart.get("id")
			labDict["labName"] = subpart.get("name")

			sectionsDict = dict()
			numLabSections = 0
			labCapacity = 0
			solutionSubpartSectionsTags = subpart.find_all("section")

			for section in solutionSubpartSectionsTags:
				numLabSections += 1
				sectionDict = dict()
				sectionID = section.get("id")
				sectionDict["sectionName"] = section.get("name")
				sectionCapacity = int(section.get("limit"))
				sectionDict["sectionCapacity"] = sectionCapacity
				labCapacity += sectionCapacity
				sectionsDict[sectionID] = sectionDict


			labDict["numLabSections"] = numLabSections
			labDict["labCapacity"] = labCapacity
			labDict["sectionsDict"] = sectionsDict
			labsDict[labID] = labDict


		courseDict["numLabs"] = str(numLabs)
		courseDict["labsDict"] = labsDict
		allocationsDict[courseID] = courseDict

		for course in allocationsDict.items():
			print(course)






main()

