import pandas as pd  # Following naming convention
from bs4 import BeautifulSoup  # For reading from XML files (bs4 needs to be installed first)
from xml.dom import minidom  # For creating and writing to XML files
# from time import time, ctime, localtime
import time

"""
	Process the current solution file (solution.xml), along with the input data XML file that was used to obtain it, 
	a modified/updated Students.xlsx input file, and produce an input data XML file containing the new course requests and
	course data with modified capacities, and a solution file that is the current solution file with the old course 
	requests removed
	
	We then process the current solution file (with the old course requests removed) and the solution file for the new 
	course requests and merge them together, resulting in an updated solution
	
	See main comment of ModifiedInputProcessing.py
"""


def main():
	while True:
		try:
			option = int(input("Do you want to (Enter the number):\n\t"
			                   "0: Process a modified Students file to produce an input data XML file for new course requests\n\t"
			                   "1: Process current and new solution files to merge them together\n"))
			if option == 0:
				generateInputXmlFile()
				break
			elif option == 1:
				generateUpdatedSolutionFile()
				break
			else:
				print("Invalid number entered. You will be prompted to re-enter.")
		except ValueError:
			print("Invalid number entered. You will be prompted to re-enter.")

# END main()


def generateInputXmlFile():
	#problemInstanceName = input("Enter problem instance name: ")
	problemInstanceName = "2020-Sem1-CAES-Wvl-no-conflicts-no-STAT130"

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



def generateUpdatedSolutionFile():
	print()

main()
