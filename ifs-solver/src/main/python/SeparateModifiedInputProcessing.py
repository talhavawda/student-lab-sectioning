import pandas as pd  # Following naming convention
from bs4 import BeautifulSoup  # For reading from XML files (bs4 needs to be installed first)
from xml.dom import minidom  # For creating and writing to XML files
# from time import time, ctime, localtime
import time
import ModifiedInputProcessing
import SectionAllocations

"""
	Process the current solution file (solution.xml), along with the input data XML file that was used to obtain it, 
	a modified/updated Students.xlsx input file, and produce an (updated) input data XML file containing the new course requests and
	course data with modified capacities, and a solution file that is the current solution file with the old course 
	requests removed
	[The updated input data XML file generated by ModifiedInputProcess.py shall represent the current solution with the 
	old course requests removed [the new course requests are already added there (without their allocations)], 
	and the updated input data XML file containing the new course requests is named as the current input data XML file name 
	with "-newrequests-<modVerNum>" appended]
	
	We then process the current solution file (with the old course requests removed) and the solution file for the new 
	course requests and merge them together, resulting in an updated solution
	
	
	We are having to do the resolving part separately as passing in an updated input data XML file (representing 
	a partial solution, generated by ModifiedInputProcessing.py) to the CPSolver may result in unnecessary 
	perturbations (section allocation changes to existing course requests) - see the main Readme.md file for details.
	For the resolving part, if we only pass in an input data XNL file containing only the new course requests to the solver,
	the the unchanged/existing course  requests' section allocations will not be changed.

	
	See main comment of ModifiedInputProcessing.py
"""


def main():
	while True:
		try:
			option = int(input("Do you want to (Enter the number):\n\t"
			                   "0: Process a modified Students file to produce an input data XML file for new course requests\n\t"
			                   "1: Process current and new solution files to merge them together\n"))
			if option == 0:
				generateNewRequestsInputXmlFile()
				break
			elif option == 1:
				generateUpdatedSolutionFile()
				break
			else:
				print("Invalid number entered. You will be prompted to re-enter.")
		except ValueError:
			print("Invalid number entered. You will be prompted to re-enter.")

# END main()


def generateNewRequestsInputXmlFile():
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



	currentSolution, currentSolutionFilePath = ModifiedInputProcessing.getCurrentSolutionFilePath(currentSolution, problemInstanceDirectoryPath)

	# Get the modified Students input file, and its modification version number
	modifiedStudentsFilePath, modVerNum = ModifiedInputProcessing.getModifiedStudentsFilePath(problemInstanceDirectoryPath)


	""" Process the current input data and solution XML files and store them in a dictionary """
	currentSolutionDict = ModifiedInputProcessing.processCurrentSolution(inputXmlFilePath, currentSolutionFilePath)

	""" Process the modified Students input Excel file to obtain a dictionary containing the updated input data"""
	updatedInputDict = ModifiedInputProcessing.processModifiedStudentsData(modifiedStudentsFilePath, currentSolutionDict)


	""" Generate/Produce the updated input data XML file, which we shall use to represent the current solution """
	ModifiedInputProcessing.generateUpdatedInputXmlFile(updatedInputDict, inputXmlFilePath)


	# The code of this function of this point is very similar to ModifiedInputProcessing.main()


	studentsNewRequestsDict = updatedInputDict["studentsNewRequestsDictionary"]


	""" Process Section Allocations data for the current solution and get its allocations.xml file 
	This Section Allocations file will be used to update the lab sections's capacities in the input data XML file 
	with only the new course requests"""

	SectionAllocations.main(currentSolutionFilePath, currentSolution)
	allocationsXmlFilePath = problemInstanceDirectoryPath + "/" + currentSolution + "/allocations.xml"


	with open(allocationsXmlFilePath, "r") as allocationsXMLFile:
		allocationsXML = allocationsXMLFile.read()

	# Passing the current section allocations XML file of the current solution to a BeatifulSoup parser
	allocationsBS = BeautifulSoup(allocationsXML, "xml")


	""" Obtaining the updated input data XML file - the file generated by ModifiedInputProcessing.generateUpdatedInputXmlFile(), 
	which we shall use to represent the current solution - so that I can extract its sectioning element's attribute values """

	periodIndex = inputXmlFilePath.rfind(".xml")
	updatedXmlFilePath = inputXmlFilePath[:periodIndex] + "-updated-1.xml"

	with open(updatedXmlFilePath, "r") as updatedXMLFile:
		updatedXML = updatedXMLFile.read()

	# Passing the updated input data XML file to a BeatifulSoup parser
	updatedBS = BeautifulSoup(updatedXML, "xml")



	""" Create an updated input data XML file with only the new course requests, 
	and with the lab section capacities being updated to reflect the already allocated students"""

	# Create XML document with XML Prolog
	newRequestsInputFileXML = minidom.Document()

	# Student Sectioning
	sectioningElement = newRequestsInputFileXML.createElement("sectioning")  # Create the root element 'sectioning'

	""" 
		Add the attributes of the 'sectioning element' - this is the problem specification information (I'm not adding the
		current input information for this new requests input XML file). Extracting it from the updated input data XML file
	"""

	updatedBSSectioningTag = updatedBS.find("sectioning") # Extract the 'sectioning' tag/element and its attributes from the updated input data XML file (BS considers an XML element as a 'tag')

	sectioningElement.setAttribute("version", updatedBSSectioningTag.get('version'))
	sectioningElement.setAttribute("initiative", updatedBSSectioningTag.get("initiative"))
	sectioningElement.setAttribute("term", updatedBSSectioningTag.get("term"))
	sectioningElement.setAttribute("year", updatedBSSectioningTag.get("year"))

	currentDateTime = time.ctime(time.time())  # current time as a string
	# timezone = time.localtime().tm_zone
	sectioningElement.setAttribute("created", currentDateTime)

	sectioningElement.setAttribute("nrDays", updatedBSSectioningTag.get("nrDays"))
	sectioningElement.setAttribute("slotsPerDay", updatedBSSectioningTag.get("slotsPerDay"))

	newRequestsInputFileXML.appendChild(sectioningElement)


	"""
		Create the 'offerings' and  'students' sub-elements of the sectioning element
		[Not adding the 'courses' sub-element that contains the courses ID-name pairs as this data is already present in the 
		updated input data XMl file and is not used by the solver] 
	"""

	offeringsElement = newRequestsInputFileXML.createElement("offerings")
	sectioningElement.appendChild(offeringsElement)

	studentsElement = newRequestsInputFileXML.createElement("students")
	sectioningElement.appendChild(studentsElement)


	print("\t\tExtracting courses data from the updated input data XML file, modifiying the lab section capacities and "
	      "writing it to the new course requests input data XML file...")

	""" Process all course offerings (All LabSections for each Lab for each Course) """

	updatedInputOfferingTags = updatedBSSectioningTag.find_all("offering")

	for updatedInputOfferingTag in updatedInputOfferingTags:  # each offering is a Tag object
		offeringElement = newRequestsInputFileXML.createElement("offering")
		offeringElement.setAttribute("id", updatedInputOfferingTag.get("id"))
		offeringsElement.appendChild(offeringElement)

		updatedInputCourseTag = updatedInputOfferingTag.find("course")  # There's only 1 "course" tag/element of this offering tag
		courseElement = newRequestsInputFileXML.createElement("course")
		courseElement.setAttribute("id", updatedInputCourseTag.get("id"))
		courseElement.setAttribute("name", updatedInputCourseTag.get("name"))
		courseElement.setAttribute("numLabs", updatedInputCourseTag.get("numLabs"))
		offeringElement.appendChild(courseElement)

		updatedInputConfigTag = updatedInputOfferingTag.find("config")  # There's only 1 "config" tag/element of this offering tag
		configElement = newRequestsInputFileXML.createElement("config")
		configElement.setAttribute("id", updatedInputConfigTag.get("id"))
		offeringElement.appendChild(configElement)

		updatedInputSubpartTags = updatedInputConfigTag.find_all("subpart")

		for updatedInputSubpartTag in updatedInputSubpartTags:
			subpartElement = newRequestsInputFileXML.createElement("subpart")
			subpartElement.setAttribute("id", updatedInputSubpartTag.get("id"))
			subpartElement.setAttribute("itype", updatedInputSubpartTag.get("itype"))
			subpartElement.setAttribute("courseLabNum", updatedInputSubpartTag.get("courseLabNum"))
			configElement.appendChild(subpartElement)


			updatedInputSectionTags = updatedInputSubpartTag.find_all("section")

			for updatedInputSectionTag in updatedInputSectionTags:
				sectionElement = newRequestsInputFileXML.createElement("section")
				sectionID = updatedInputSectionTag.get("id")
				sectionElement.setAttribute("id", sectionID)
				sectionElement.setAttribute("courseLabSectionNum", updatedInputSectionTag.get("courseLabSectionNum"))

				# initialCapacity = int(updatedInputSectionTag.get("limit"))  # gives same value as allocationsSectionTag.get("sectionCapacity") below
				allocationsSectionTag = allocationsBS.find("section", section="S"+sectionID) # Get the section tag/element of this section in the solution.xml file
				initialCapacity = int(allocationsSectionTag.get("sectionCapacity"))
				numAllocated = int(allocationsSectionTag.get("sectionAllocated"))
				newCapacity = initialCapacity - numAllocated
				sectionElement.setAttribute("limit", str(newCapacity))
				subpartElement.appendChild(sectionElement)

				updatedInputTimeTag = updatedInputSectionTag.find("time")  # There's only 1 "time" tag/element of this offering tag
				timeElement = newRequestsInputFileXML.createElement("time")
				timeElement.setAttribute("days", updatedInputTimeTag.get("days"))
				timeElement.setAttribute("start", updatedInputTimeTag.get("start"))
				timeElement.setAttribute("length", updatedInputTimeTag.get("length"))
				timeElement.setAttribute("dates", updatedInputTimeTag.get("dates"))
				timeElement.setAttribute("sessionDay", updatedInputTimeTag.get("sessionDay"))
				sectionElement.appendChild(timeElement)

	print("\t\tCourses data has been written to the new course requests input data XML file.")

	print("\tWriting updated students data to the new course requests input data XML file...")

	""" Process all student enrollments (lab sessions requests and section allocations) """





	print("\tThe new course requests data has been written to the updated input data XML file...")

	newRequestsInputFileXML = newRequestsInputFileXML.toprettyxml(indent="\t")

	print("\nUpdated input data XML file containing only the new course requests has been generated.")

	periodIndex = inputXmlFilePath.rfind(".xml")
	newRequestsXmlFileName = inputXmlFilePath[:periodIndex] + "-newrequests-1.xml"

	# Write the updated input data XML file
	with open(newRequestsXmlFileName, "w") as newRequestsXmlFile:
		newRequestsXmlFile.write(newRequestsInputFileXML)

	print("Updated input data XML file with only the new course requests has been written to file: '" + newRequestsXmlFileName + "'.")


def generateUpdatedSolutionFile():
	print()


# Run the main method if this python file is being executed/run directly (either from IDE or Command Line)
if __name__ == '__main__':
	main()
	print("SeparateModifiedInputProcessing.py has been executed")