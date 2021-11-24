package com.talhavawda.ifssolver;

//import org.cpsolver.studentsct.*;

import org.cpsolver.studentsct.Test;
import java.io.*;
import java.io.File;
import java.nio.charset.StandardCharsets;
import java.util.Date;
import java.util.InputMismatchException;
import java.util.Scanner;

public class Main {
	public static void main(String [] args) {
		/*
			args[0] is solverRootDirectory (the local absolute directory of the root folder of this project)
			args[1] is problemInstanceAbsDirectory (the local absolute directory of the problem instance's folder)
			args[2] is problemInstanceName
			args[3] is option
			solverRootDirectory, problemInstanceAbsDirectory and problemInstanceName  must be specified in the args parameter
		 */

		Scanner input = new Scanner(System.in);

		String solverRootDirectory = args[0]; //local absolute directory of the root folder of this project
		String problemInstanceDirectoryPath = args[1]; // input data XML file's directory (directory also used to store output)

		//String problemInstanceName = problemInstanceDirectoryPath.substring(problemInstanceDirectoryPath.lastIndexOf("\\")+1); // In problemInstanceDirectoryPath, the slashes separating the directories are backslashes
		String problemInstanceName = args[2];


		// String xmlInputFilePath = "problemInstanceDirectoryPath + "/" + problemInstanceName + ".xml"; //path of the input file (its name + relative path from Source directory preceding it)

		String xmlInputFilePath;

		String configurationFilePath;

		int option; //type of solution we're obtaining

		if (args.length == 4) {
			try {
				option = Integer.parseInt(args[3]);
			} catch (NumberFormatException e) { // if string contains an invalid (not parsable) integer
				option = 0; //assign a default
			}

			System.out.println("Option: " + option + "\n");

		} else { //get option from user
			int userAnswer;
			input = new Scanner(System.in);
			System.out.println("Are you (Enter the number):\n\t0: Obtaining an initial solution to the problem instance" +
					"\n\t1: Obtaining an updated solution to the problem instance (updated input data XML file)" +
					"\n\t2: Obtaining an updated solution to the problem instance on only the new course requests (new requests input data XML file)");


			try {
				userAnswer = input.nextInt();
			} catch (InputMismatchException e) { // if invalid integer number entered
				userAnswer = 0;
			}

			option = userAnswer;
		}


		if (option == 0) {
			System.out.println("Obtaining an initial solution to the problem instance.");
			xmlInputFilePath = solverRootDirectory +  "/src/main/resources/input/" + problemInstanceName + "/" + problemInstanceName + ".xml";
			configurationFilePath = solverRootDirectory + "/src/main/resources/SolverConfiguration.cfg";
		} else if (option == 1) {
			System.out.println("Obtaining an updated solution to the problem instance (updated input data XML file.)");
			xmlInputFilePath = solverRootDirectory + "/src/main/resources/input/" + problemInstanceName + "/" + problemInstanceName + "-updated-1.xml";
			configurationFilePath = solverRootDirectory + "/src/main/resources/SolverConfiguration-resolving.cfg";

		}  else if (option == 2) {
			System.out.println("Obtaining an updated solution to the problem instance on only the new course requests (new requests input data XML file.)");
			xmlInputFilePath = solverRootDirectory + "/src/main/resources/input/" + problemInstanceName + "/" + problemInstanceName + "-newrequests-1.xml";
			configurationFilePath = solverRootDirectory + "/src/main/resources/SolverConfiguration.cfg"; // Not the resolving one as in this input XML file, none of the course requests are allocated - treating it as an initial input
		} else {
			// do default (option == 0)
			System.out.println("Obtaining an initial solution to the problem instance.");
			xmlInputFilePath = solverRootDirectory +  "/src/main/resources/input/" + problemInstanceName + "/" + problemInstanceName + ".xml";
			configurationFilePath = solverRootDirectory + "/src/main/resources/SolverConfiguration.cfg";
		}


		String[] cpsolverArgs = {configurationFilePath, xmlInputFilePath, problemInstanceDirectoryPath};

		java.text.SimpleDateFormat sDateFormat = new java.text.SimpleDateFormat("yyMMdd_HHmmss", java.util.Locale.US);

		//The name of the folder of this solution instance that shall be run - it is the current date and time
		//The actual folder name may be 1 second later
		String solutionDirectoryName = sDateFormat.format(new Date());


		try {
			//Writer writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(problemInstanceDirectoryPath + "/Solutions.txt"), StandardCharsets.UTF_8));
			Writer solutionsWriter = new BufferedWriter(new FileWriter(problemInstanceDirectoryPath + "/Solutions.txt",  StandardCharsets.UTF_8, true)); //ensuring data is appended to file instead of overwriting
			solutionsWriter.append(solutionDirectoryName + "\n");
			solutionsWriter.close();

			Writer currentSolutionsWriter = new BufferedWriter(new FileWriter(problemInstanceDirectoryPath + "/CurrentSolutions.txt",  StandardCharsets.UTF_8, true)); //ensuring data is appended to file instead of overwriting
			currentSolutionsWriter.append(solutionDirectoryName + "\n");
			currentSolutionsWriter.close();

			System.out.println("\tWriting to Solutions.txt and CurrentSolutions.txt files has been successful.");
		} catch (IOException e) { //if FileNotFoundException is thrown (it implements IOException)
			System.out.println("ERROR: " + e);
			System.out.println("\tWriting to Solutions.txt and CurrentSolutions.txt files has been unsuccessful.");
			System.out.println("\tPlease update the Solutions.txt file of this problem instance manually with the following entry: " + solutionDirectoryName);
		}

		//System.out.println(solutionDirectoryName);

		Test.main(cpsolverArgs); //Does Batch Sectioning by default. Will do Online Sectioning if specify a 4th parameter in the args [], with it being the string "online"

	}
}
