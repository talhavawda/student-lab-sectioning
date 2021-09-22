package com.talhavawda.ifssolver;

//import org.cpsolver.studentsct.*;

import org.cpsolver.studentsct.Test;

import java.io.File;
import java.util.Date;

public class Main {
	public static void main(String [] args) {

		String problemInstanceName = "2020-Sem1-CAES-Wvl-no-extra-requests";
		String problemInstanceDirectoryPath = "src/main/resources/input/" + problemInstanceName ; // input data XML file's directory (directory also used to store output)
		String xmlInputFilePath = "src/main/resources/input/" + problemInstanceName + "/" + problemInstanceName + ".xml"; //path of the input file (its name + relative path from Source directory preceding it)
		String configurationFilePath = "src/main/resources/SolverConfiguration.cfg";

		String[] cpsolverArgs = {configurationFilePath, xmlInputFilePath, problemInstanceDirectoryPath};

		java.text.SimpleDateFormat sDateFormat = new java.text.SimpleDateFormat("yyMMdd_HHmmss", java.util.Locale.US);
		String solutionDirectoryName = sDateFormat.format(new Date()); //The name of the folder of this solution instance that shall be run - it is the current date and time
		System.out.println(solutionDirectoryName);
		Test.main(cpsolverArgs); //Does Batch Sectioning by default. Will do Online Sectioning if specify a 4th parameter in the args [], with it being the string "online"

	}
}
