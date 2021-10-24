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

	""" Get the name of the solution we want to work with """

	while True:
		try:
			solutionName = input("Enter the name of the solution (format: yymmdd_hhmmss) that you want to use process to obtain the Section Allocations data: ")
			solutionFilePath = problemInstanceDirectoryPath + "/" + solutionName + "/solution.xml"  # the file path of the solution.xml file of this solution
			open(solutionFilePath, "r")
			break  # solutionFilePath is valid

		except FileNotFoundError:
			print("Solution folder not found in the problem instance's directory. You will be prompted to re-enter the name of the solution.\n")

	""" Process the solution's XML file and obtain the courses and allocations data """
	allocationsDict = processSolution(solutionFilePath)

	""" Write the allocations data to the end of the solution's XML file and display it to the console """


def processSolution(solutionFilePath: str):
	"""
		Read on the solution's XML file and process the data into a dictionary that stores the courses' id-name mappings,
		num course requests, section capacities, and section allocations

		:param solutionFilePath: str: the file path of the current solution XML file
		:return: allocationsDict: a dictionary containing the courses info, num course requests, section limits, and section
		allocations
	"""

	print("\tReading in and parsing the solution XML file...")

	with open(solutionFilePath, "r") as solutionXMLFile:
		solutionXML = solutionXMLFile.read()

	# Passing the solution XML file to a BeatifulSoup parser
	solutionBS = BeautifulSoup(solutionXML, "xml")

	print("\tFile has been read in and parsed.")

	"""
		allocationsDict: A dictionary (Map) of the courses, their labs and sections, and section allocations
		key = courseID; value = a dictionary of the course's data
	"""
	allocationsDict = dict()
	allocationsDict.clear()

	solutionSectioningTag = solutionBS.find("sectioning") # Extract the 'sectioning' tag/element and its attributes from the solution XML file (BS considers an XML element as a 'tag')
	solutionOfferingsTag = solutionBS.find("offerings")



main()

