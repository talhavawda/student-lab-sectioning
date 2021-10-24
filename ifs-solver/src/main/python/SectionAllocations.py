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
	writeAllocationsData(allocationsDict, solutionFilePath)


def processSolution(inputXmlFilePath: str, solutionFilePath: str):
	"""
		Read on the solution's XML file and process the data into a dictionary that stores the courses' id-name mappings,
		num course requests, section capacities, and section allocations

		:param inputXmlFilePath: str: the file path of the initial input data XML file
		:param solutionFilePath: str: the file path of this solution's XML file
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

	print("\tFiles have been read in and parsed.\n")

	print("\tObtaining courses and section allocations data...")

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
		courseDict["courseName"] = course.get("courseName")
		courseDict["numCourseRequests"] = 0
		allocationsDict[courseID] = courseDict


	""" Process the courses data from the solution XML file """

	solutionOfferingsTag = solutionBS.find("offerings")  # Extract the 'offerings' tag/element and its attributes from the solution XML file

	solutionOfferingTags = solutionOfferingsTag.find_all("offering")

	for offering in solutionOfferingTags: # each offering contains a course and the configuration for that course
		solutionCourseTag = offering.find("course")
		courseID = solutionCourseTag.get("id")

		solutionConfigTag = offering.find("config")

		courseDict = allocationsDict[courseID]
		# labsDict = dict()
		labsList = list()  # Making it a list instead of a dict as we will be needing to access the labs of a course in their order (course's first lab, course's second lab, etc.) instead of by their ID
		numLabs = 0
		solutionConfigSubpartTags = solutionConfigTag.find_all("subpart")

		for subpart in solutionConfigSubpartTags: # a 'subpart' tag is a Lab
			numLabs += 1
			labDict = dict()
			labID = subpart.get("id")
			labDict["labID"] = subpart.get("id")
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
				sectionDict["sectionAllocated"] = 0
				labCapacity += sectionCapacity
				sectionsDict[sectionID] = sectionDict


			labDict["numLabSections"] = numLabSections
			labDict["labCapacity"] = labCapacity
			labDict["labAllocated"] = 0
			labDict["sectionsDict"] = sectionsDict
			# labsDict[labID] = labDict
			labsList.append(labDict)


		courseDict["numLabs"] = str(numLabs)
		# courseDict["labsDict"] = labsDict
		courseDict["labsList"] = labsList
		allocationsDict[courseID] = courseDict



	""" Process the section allocations from the solution XML file """

	solutionStudentTags = solutionBS.find_all("student")

	for student in solutionStudentTags:  # each student is a Tag object
		solutionCourseRequestTags = student.find_all("course")

		for courseRequest in solutionCourseRequestTags:
			courseRequestCourseID = courseRequest.get("course")
			solutionCRAllocationTags = courseRequest.find_all("section")

			courseDict = allocationsDict[courseRequestCourseID]
			courseDict["numCourseRequests"] += 1
			labsList = courseDict["labsList"]

			labNum = 0

			for sectionAllocation in solutionCRAllocationTags:
				sectionID = sectionAllocation.get("id")
				labDict = labsList[labNum]
				labDict["labAllocated"] += 1

				sectionsDict = labDict["sectionsDict"]
				sectionDict = sectionsDict[sectionID]
				sectionDict["sectionAllocated"] += 1

				labNum += 1

			allocationsDict[courseRequestCourseID] = courseDict

	print("\tCourses and section allocations data have been obtained.\n")

	for course in allocationsDict.items():
		print(course)

	return allocationsDict


def writeAllocationsData(allocationsDict: dict, solutionFilePath: str):
	"""
		Write the courses and allocations data to the end of the solution's XML file and display it to the console

		:param allocationsDict: dictionary containing the courses info, num course requests, section limits, and section
		allocations for this solution
		:param solutionFilePath: str: the file path of this solution's XML file
		:return: None
	"""

	solutionXML = minidom.parse(solutionFilePath)  # Using minidom instead of BeautifulSoup as we shall be writing back to this XML file (I prefer to write using minidom instead of BS)
	sectioningElement = solutionXML.getElementsByTagName("sectioning")[0]  # There is only 1 sectioning element

	allocationsElement = solutionXML.createElement("allocations")

	print("\tCourses and allocations data:")

	for course in allocationsDict:  # traversing a dict using a for loop traverses the keys of the dict | courses are the keys (course IDs) of allocationsDict
		courseDict = allocationsDict[course]
		courseName = courseDict["courseName"]
		numCourseRequests = courseDict["numCourseRequests"]  # an int
		numLabs = courseDict["numLabs"]  # an int

		print("\t\tCourse C", course, " [" + courseName + "] -\tCourse requests = ", numCourseRequests, " |\tLabs = ", numLabs, sep="")
		courseElement = solutionXML.createElement("course")
		courseElement.setAttribute("course", "C" + course)
		courseElement.setAttribute("courseName", courseName)
		courseElement.setAttribute("numCourseRequests", str(numCourseRequests))  # all attribute values of XML files are strings
		courseElement.setAttribute("numLabs", str(numLabs))  # all attribute values of XML files are strings

		labsList = courseDict["labsList"]

		for labDict in labsList:
			labName = labDict["labName"]
			numLabSections = labDict["numLabSections"]  # an int
			labCapacity = labDict["labCapacity"]  # an int
			labAllocated = labDict["labAllocated"]  # an int
			labAllocatedPercentage = round(labAllocated / labCapacity * 100, 2)  # round off percentage to 2 decimal places

			print("\t\t\tLab ", labName, " -\tLab Sections = ", numLabSections, " |\tLab Capacity = ", labCapacity, " |\tLab Allocated = ", labAllocated, " |\t % allocated = ", labAllocatedPercentage, sep="")
			labElement = solutionXML.createElement("lab")
			labElement.setAttribute("lab", labName)
			labElement.setAttribute("numLabSections", str(numLabSections))  # all attribute values of XML files are strings
			labElement.setAttribute("labCapacity", str(labCapacity))  # all attribute values of XML files are strings
			labElement.setAttribute("labAllocated", str(labAllocated))  # all attribute values of XML files are strings
			labElement.setAttribute("%allocated", str(labAllocatedPercentage))  # all attribute values of XML files are strings

			sectionsDict = labDict["sectionsDict"]

			for section in sectionsDict:  # traversing a dict using a for loop traverses the keys of the dict | sections are the keys (section IDs) of sectionsDict
				sectionDict = sectionsDict[section]
				sectionName = sectionDict["sectionName"]
				sectionCapacity = sectionDict["sectionCapacity"]  # an int
				sectionAllocated = sectionDict["sectionAllocated"]  # an int
				sectionAllocatedPercentage = round(sectionAllocated / sectionCapacity * 100, 2)  # round off percentage to 2 decimal places

				print("\t\t\t\tSection ", sectionName, " -\tSection Capacity = ", sectionCapacity, " |\tSection Allocated = ", sectionAllocated, " |\t % allocated = ", sectionAllocatedPercentage, sep="")
				sectionElement = solutionXML.createElement("section")
				sectionElement.setAttribute("section", sectionName)
				sectionElement.setAttribute("sectionCapacity", str(sectionCapacity))  # all attribute values of XML files are strings
				sectionElement.setAttribute("sectionAllocated", str(sectionAllocated))  # all attribute values of XML files are strings
				sectionElement.setAttribute("%allocated", str(sectionAllocatedPercentage))  # all attribute values of XML files are strings

				labElement.appendChild(sectionElement)

			courseElement.appendChild(labElement)

		allocationsElement.appendChild(courseElement)

	sectioningElement.appendChild(allocationsElement)


	solutionXML = solutionXML.toprettyxml(indent="\t")

	# Write the updated solution XML file
	with open(solutionFilePath, "w") as updatedXmlFile:
		updatedXmlFile.write(solutionXML)

	print("\n\nCourses and allocations data have been written to the solution file: '" + solutionFilePath + ".")


main()

