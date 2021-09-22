package com.talhavawda.ifssolver;

//import org.cpsolver.studentsct.*;

import org.cpsolver.studentsct.Test;
import java.io.*;
import java.io.File;
import java.nio.charset.StandardCharsets;
import java.util.Date;

public class Main {
	public static void main(String [] args) {

		String problemInstanceName = "2020-Sem1-CAES-Wvl-no-extra-requests";
		String problemInstanceDirectoryPath = "src/main/resources/input/" + problemInstanceName; // input data XML file's directory (directory also used to store output)
		String xmlInputFilePath = "src/main/resources/input/" + problemInstanceName + "/" + problemInstanceName + ".xml"; //path of the input file (its name + relative path from Source directory preceding it)
		String configurationFilePath = "src/main/resources/SolverConfiguration.cfg";

		String[] cpsolverArgs = {configurationFilePath, xmlInputFilePath, problemInstanceDirectoryPath};

		java.text.SimpleDateFormat sDateFormat = new java.text.SimpleDateFormat("yyMMdd_HHmmss", java.util.Locale.US);

		//The name of the folder of this solution instance that shall be run - it is the current date and time
		//The actual folder name may be 1 second later
		String solutionDirectoryName = sDateFormat.format(new Date());

		//PrintWriter solutionsFile = new PrintWriter(problemInstanceDirectoryPath + "/solutions.txt", "UTF-8");// a Text File containing the names of the directories of all the solutions generated for this problem input

		try {
			//Writer writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(problemInstanceDirectoryPath + "/Solutions.txt"), StandardCharsets.UTF_8));
			Writer writer = new BufferedWriter(new FileWriter(problemInstanceDirectoryPath + "/Solutions.txt",  StandardCharsets.UTF_8, true)); //ensuring data is appended to file instead of overwriting
			writer.append(solutionDirectoryName + "\n");
			writer.close();
			System.out.println("\tWriting to Solutions.txt file has been successful.");
		} catch (IOException e) { //if FileNotFoundException is thrown (it implements IOException)
			System.out.println("ERROR: " + e);
			System.out.println("\tWriting to Solutions.txt file has been unsuccessful.");
			System.out.println("\tPlease update the Solutions.txt file of this problem instance manually with the following entry: " + solutionDirectoryName);
		}

		//System.out.println(solutionDirectoryName);

		Test.main(cpsolverArgs); //Does Batch Sectioning by default. Will do Online Sectioning if specify a 4th parameter in the args [], with it being the string "online"

	}
}
