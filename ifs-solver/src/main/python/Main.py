import InputProcessing
import ModifiedInputProcessing
import SeparateModifiedInputProcessing
import SectionAllocations
import jpype
import jpype.imports
from pathlib import Path
import os

"""
	The system's 'entry point' file
"""

def main():

	#problemInstanceName = input("Enter the name of the current problem instance: ")
	problemInstanceName = "2021-Sem2-CAES-Wvl"
	print("Problem Instance's name:", problemInstanceName)

	while True:

		try:
			option = int(input("Enter the number indicating the script you wish to run:\n\t"
			                   "0: Main.java\n\t"
			                   "1: InputProcessing.py\n\t"
			                   "2: ModifiedInputProcessing.py\n\t"
			                   "3: SeparateModifiedInputProcessing.py\n\t"
			                   "4: SectionAllocations.py\n"))

			if option == 0:
				print("Running Main.java\n==================\n")
				""" Run Main.java -> using jpype"""
				currentRelativeDirectory = "/src/main/python"
				solverRootDirectory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname( __file__ )))) # Go up 3 directories to reach the root directory of this project
				ifsSolverJarPath = "-Djava.class.path=" + solverRootDirectory + "/out/artifacts/ifs_solver_jar/ifs-solver.jar"
				#"-Djava.class.path=/out/artifacts/ifs_solver_jar/ifs-solver.jar"
				jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", ifsSolverJarPath)
				jpype.JClass("com.talhavawda.ifssolver.Main").main([])
				jpype.shutdownJVM()

				break
			elif option == 1:
				print("Running InputProcessing.py\n===========================\n")
				InputProcessing.main(problemInstanceName)
				break
			elif option == 2:
				print("Running ModifiedInputProcessing.py\n===================================\n")
				ModifiedInputProcessing.main(problemInstanceName)
				break
			elif option == 3:
				print("Running SeparateModifiedInputProcessing.py\n===========================================\n")
				SeparateModifiedInputProcessing.main(problemInstanceName)
				break
			elif option == 4:
				print("Running SectionAllocations.py\n========\n")
				SectionAllocations.main(problemInstanceName)
				break
			else:
				print("Number entered is not one of the options. You will be prompted to re-enter.")
		except ValueError:
			print("Invalid number entered. You will be prompted to re-enter.")


# Run the main method if this python file is being executed/run directly (either from IDE or Command Line)
if __name__ == '__main__':
	main()

	print("Main.py has been executed")