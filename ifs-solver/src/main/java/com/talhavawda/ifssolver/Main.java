package com.talhavawda.ifssolver;

//import org.cpsolver.studentsct.*;

import org.cpsolver.studentsct.Test;

public class Main {
	public static void main(String [] args) {

		String problemInstanceName = "2020-Sem1-CAES-Wvl";
		String problemInstanceDirectoryPath = "src/main/resources/input/" + problemInstanceName ; // input data XML file's directory (directory also used to store output)
		String xmlInputFilePath = "src/main/resources/input/" + problemInstanceName + "/" + problemInstanceName + ".xml"; //path of the input file (its name + relative path from Source directory preceding it)
		String configurationFilePath = "src/main/resources/SolverConfiguration.cfg";

		String[] cpsolverArgs = {configurationFilePath, xmlInputFilePath, problemInstanceDirectoryPath};
		Test.main(cpsolverArgs);
	}
}
