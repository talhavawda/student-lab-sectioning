import InputProcessing
import ModifiedInputProcessing
import SeparateModifiedInputProcessing
import SectionAllocations
import jpype
import jpype.imports

"""
	The system's 'entry point' file
"""

def main():

	problemInstanceName = input("Enter problem instance name: ")

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
				jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=out/artifacts/ifs_solver_jar/ifs-solver.jar")
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