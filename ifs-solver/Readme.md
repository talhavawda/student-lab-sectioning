# IFS Solver

This project is for testing UniTime's CPSolver (that makes use of the Iterative Forward Search (IFS) algorithm) 
to solve my Student Sectioning problem.

This project is being developed using Java (for the solver, as the CPSolver is available in Java only) and Python in IntelliJ IDEA.

CPSolver/UniTime Student Sectioning Solver (UniTime site Links):
 - Constraint Solver Examples: Constraint Solver Examples: https://www.cpsolver.org/cpsolver_examples.php
 - Student Sectioning Problem Description: https://www.unitime.org/sct_description.php
 - Student Sectioning Data Format: https://www.unitime.org/sct_dataformat.php
 - Student Sectioning Benchmark Datasets: https://www.unitime.org/sct_datasets.php
 - Student Sectioning Solver Execution: https://www.unitime.org/sct_execution.php
 - CPSolver API Documentation: https://www.unitime.org/api/cpsolver-1.3/index.html
 [put links from Issue #7]
 
## What I've done (Steps)
1. Created this project (ifs-solver) in IntelliJ inside my local copy of the student-lab-sectioning repository
    - This automatically adds the project to Git and I can access Git features inside IntelliJ
        - I've also got the repository opened in GitHub Desktop and I'm using this as my main tool for version control
2. I created a 'lib' folder (Right Click -> New -> Directory), created a sub-folder inside it called 'cpsolver-1.3.232'
 and added the CPSolver jar files (and the dom4j and log4j jar files) to the 'cpsolver-1.3.232' folder.
3. I right-clicked the 'cpsolver-1.3.232' folder and selected 'Add as library'
    - The folder automatically gets added as a Library in the Project Structure -> Libraries tab
4. Created sub-directories in the src folder
    - 'main' and 'test' sub-directories
        - In the 'main' sub-directory, I created 'java' and 'resources' sub-directories and marked them as Sources 
        and Resources respectively in the Project Structure
        - In the 'test' sub-directory, I created a 'java' sub-directory and marked it
        as Tests in the Project Structure
5. Studying the Data Format of the UniTime Student Sectioning solver
6. Creating my Excel template input files
7. Creating input files for 2020-Sem1-CAES-Wvl dataset (/problem instance) according to my templates
8. Creating a Python program script (InputProcessing.py) inside this ifs-solver project to read in and process input files, and produce an XML file (input data XML file)
 for the UniTime Student Sectioning solver according to their data format structure/template
    - Current input files I'm using are the 2020-Sem1-CAES-Wvl problem instance
    - How to run Python in IntelliJ:
        - Links
            - https://www.jetbrains.com/help/idea/configuring-local-python-interpreters.html
            - https://www.jetbrains.com/help/idea/configuring-python-sdk.html
            - https://www.jetbrains.com/help/idea/run-debug-configuration-python.html#1
        - Then go to Project Settings -> Modules -> Dependencies -> Add Python interpreter
        - When wanting to run a Python script, switch to the Python configuration in the 'Edit Run/Debug Configurations' dialog dropdown 
    - For the main software, when adding the Python interpreter, consider using a virtual environment interpreter
    instead of the System interpreter
    - I have decided to store the Problem Specification data in an XML file instead of a text file.
    I am using the BeautifulSoup library to read in the XML file. It needs to first be installed (package name is 'beautifulsoup4')
    along with the 'lxml' package
    - Python modules for creating XML files: Minidom and ElementTree
        - I have chosen to use Minimdom as it seems a bit simpler and it formats the tags nicely (puts them on new lines)
            - References for using Mindom:
                - https://www.geeksforgeeks.org/create-xml-documents-using-python/
                - https://www.guru99.com/manipulating-xml-with-python.html
        - However apparently ElementTree is faster for parsing (reading in) XML files, but I don't think this will affect me (hopefully) as I'm just creating the XML files
            - References:
                - https://stackoverflow.com/questions/192907/xml-parsing-elementtree-vs-sax-and-dom
                - https://www.mirketa.com/xml-parsing-python/
                - https://www.edureka.co/community/52537/difference-between-elementtree-and-minidom
                
    - For the 2020-Sem1-CAES-Wvl's Students.xlsx input file, I used the COUNTA() Excel function (with the cell range being the 10 courses for that row) 
    to populate the numCourses column as the "CAES Tutorial Allocations 2020BC1 - WVC" given by the College did not have 
    column specifying the number of modules (courses) the student is doing.
        - The default Excel cell format is 'General' and if a cell is empty (in our case, the extra courses columns up till course10), then 
        when reading into a Pandas' DataFrame, the value 'NaN' will be stored 
            - I will be using the numCourses value for that student to extract the courses that that student will be doing as it will be quicker 
            than iterating through all 10 columns and checking if the cell value is non-empty/non-NaN
    - SEE src/main/resources/Readme.md        
 9. Running the UniTime's Student Sectioning CPSolver (on the 2020-Sem1-CAES-Wvl problem instance)
    - Tried running from command line first (using the execution command on the UniTime website) and was playing around with the command to get the file paths right
        - The execution command on the UniTime website has the java jar file to run called 'studentsct-1.3.jar' but there doesn't exist such a file (and the output was
        giving an error about that file not being found) - we're only given the cpsolver jar file that contains everything.
        So I used the CPSolver jar file in the cmd command. 
        - CMD command I settled on using that didn't give an error:
            - java -Xmx1g -jar lib/cpsolver-1.3.232/cpsolver-1.3.232.jar src/main/resources/SolverConfigurationFile.cfg src/main/resources/input/2020-Sem1-CAES-Wvl/2020-Sem1-CAES-Wvl.xml src/main/resources/input/2020-Sem1-CAES-Wvl
        - However, the solver interpreted the problem I'm trying to solve as a Course Timetabling problem and gave an error about input being incorrect.
             - `Reading 2020-Sem1-CAES-Wvl.x: [main] Test failed.
               java.lang.IllegalArgumentException: Given XML file is not large lecture room timetabling problem.
                       at org.cpsolver.coursett.TimetableXMLLoader.load(TimetableXMLLoader.java:159)
                       at org.cpsolver.coursett.TimetableXMLLoader.load(TimetableXMLLoader.java:147)
                       at org.cpsolver.coursett.Test.<init>(Test.java:231)
                       at org.cpsolver.coursett.Test.main(Test.java:292)`
    - So I decided to skip cmd and go straight to executing from code. 
        - Created an org.talhavawda.ifssolver package inside the src/main/java directory and added a Main file with a main() method. 
        Then I added code to my Main.main() method to set up the string parameter variables, and then called org.cpsolver.studentsect.Test.main() with its arg param being the array of my string parameter variables.
        - Was getting a NullPointerException error during the XML Loading process - I didn't specify a 'dates' attribute for the 'time' element of the 'section' element in my XML input file generation
            - I fixed this by setting a 'dates' attribute with the value being an empty string
                - Todo: Consider changing this 'dates' value to something more meaningful [UPDATE: Done below]
        - Then I was getting an error cos I didn't put priority attribute for course requests (NumberFormatException). Fixed that also.
        - It's working now
            - Observations:
                - The solution.xml file did not include all the attributes I added to the input file in addition
                 to what was in the UniTime's SS Data Format
                 - tableau.csv is a csv file of the solution - it indicates the sections assigned to each course request (1 section per subpart of a course)
                    - Each row is a course request
                 - request-priorities.csv and tableau.csv in the solution folder seems to indicate that if a student has more than 1 course request,
                 then the priorities of their course requests will be in the listed/ascending order (and not the same priority)
                 even if the priority attribute values for those course requests are the same.
                - Config file changes I made (see below)
        - I modified the default configuration file given by UniTime to tune it to my specific Student Sectioning Problem
            - Default values were Termination.StopWhenComplete=false and Termination.TimeOut=28800 so it was continuing even though it was solved.
            I changed Timeout to 60 secs and upon observation of the log file (210902_105758), the CAES-Wvl case was solved
            within 4 seconds. The solution kept finding other solutions for the remaining 56 seconds, but returned the BEST 
            solution at the end. The BEST solution wasn't a very big improvement on the first solution, and the quality of the solutions
            seemed to have decreased over time. 
            - Further changed StopWhenComplete to true and Timeout to 300      
            - SEE src/main/resources/Readme.md for info about the configuration file I'm using for the solver (and more changes I made to it)
    - Upon relooking at the raw input data files given by UKZN, I noticed that in the "Final Practical allocations Semester 1 2020 Overall"
    file (also containing the scheduled practical timetables but for both campuses), that it includes additional 
    courses that were not included in the  Wvl/pmb" sem1 2020 table" files. So I need to go remodify the Courses.xlsx input file
    for the 2020-Sem1-CAES-Wvl problem instance
        - I have updated the Courses.xlsx file for the 2020-Sem1-CAES-Wvl problem instance with the additional
        courses (and their scheduled allocations), and ran InputProcessing.py on the now updated dataset to create the updated
        2020-Sem1-CAES-Wvl XML input data file. The initial problem instance before this update is now called 2020-Sem1-CAES-Wvl-OLD 
            - Tried running IFS-Solver on updated 2020-Sem1-CAES-Wvl problem instance. 
            See [src/main/resources/Readme.md#2020-sem1-caes-wvl - 210905_212507 solution](src/main/resources/Readme.md#2020-sem1-caes-wvl) 
            for the error that occurred. I found the error to be in the following line of code: 
            `cmp = a.getSubpart().getInstructionalType().compareTo(b.getSubpart().getInstructionalType());`
            in the SectionConflictTable.java file. I remember now that I did not set an Instructional Type attribute for the subparts of the courses 
            in the XML input file.
            I fixed the error by updating the Python program script (InputProcessing.py) to add the "itype" attribute (with "Laboratory" value)
            to each of the subparts, then reran InputProcessing.py and then the IFS-Solver
        - There are 56 unassigned course requests as  2 courses are filled to capacity and have more course requests than their capacity (See 210906_143728 solution)
        
    - Attended to and fixed the Timeslots issue (See https://github.com/talhavawda/student-lab-sectioning/issues/10 for details)
        - Timeslots are now according to the default of 288 slots per day and thus 5 minutes per slot
        - I modified the CoursesInputTemplate.xlsx and the corresponding Courses input file for the current 2020-Sem1-CAES-Wvl problem instance, 
        as well as the 2020-Sem1-CAES-Wvl-OLD problem instance, and generated their new/updated input data XML files.        
    - Dealing with the unassigned course requests due to filled capacities. 
        - I created a modified instance (2020-Sem1-CAES-Wvl-no-extra-requests) of this 2020-Sem1-CAES-Wvl problem instance and
        increased the capacities of the BIOL103 and BIOL195 courses to 218 and 238 respectively in the Courses.xlsx input file
        so that there is no extra requests above the capacity for these courses (the number of requests matches the capacity),
        and ran the solver to obtain a complete solution
        - I did this as I want a complete solution that I can use to do the Minimal Perturbation 
        experimentation part - making changes to the input and resolving.

10. Creating a Python program script (ModifiedInputProcessing.py) to process a modified/updated Students.xlsx input file, 
the initial solution file (solution.xml), along with the input data XML file that was used to obtain it, and to produce 
an updated XML file (input data file) that is a partial solution (the unchanged course requests are still assigned as is, 
the new course requests are unassigned/unallocated, and the old course requests removed)
    - Will be using the 2020-Sem1-CAES-Wvl-no-extra-requests instance to test the script as it gives a complete initial solution
        - Although I don't really require an initial solution that is complete, I would like to use one for the experimentation process 
    - Rule/assumption when modifying the input - the number of course requests for each course (for this problem instance, each 
    course only has one lab, so a request for a course is for that course's lab) shall not be more than the total capacity for that
    course (the sum of the capacities of each section of that course's lab). Thus we shall not have any availability conflicts.
        - Todo: Since in the user system we won't have any control over the modified input given, we'll also need to ensure that there
        are no availability conflicts (See https://github.com/talhavawda/student-lab-sectioning/issues/9; we may even allow availability conflicts). 
            - **UPDATE**: This has not been done yet by me
    - Discovered a bug when preparing to add the solutions (assigned sections) to the studentsDict. 
        - BUG: Time overlap conflicts are not being detected by the solver and students' in my problem instance are 
        being assigned to sections that occur at the same time
        - I discovered this bug as I was thinking what will reflect in the solution.xml file if there is a time 
        conflict and thus the student will not be assigned a section for that course request. So I took a student (218047643)
        and added a course request  for a course that they were already doing that contained only 1 section for its lab (BIOL196).
        So now this student had two course requests for BIOL196. When I generated the updated input data XML file, and 
        ran the solver on it, to my surprise I saw that the (same) section of BIOL196 was assigned to both 
        course requests (thus a time overlap conflict) [See solution 210926_202819].
        I then thought that maybe the solver detects if two course requests are for the same course and doesn't consider
        time conflicts for it. So for the second BIOL196 course request for this student, I replaced BIOL196 with another course,
        BIOL222, a course that doesn't (currently) exist, and went to Courses.xlsx and added BIOL222 with only 1 section, whose timeslot
        is the exact same as that of BIOL196 and set the capacity to 1, so that I can test time overlap conflict for two different courses.
        Yet, still both course requests were assigned to the respective sections (both of which occur at the same time) [See solution 210926_204519]. 
        - I've looked in the SolverConfiguration.cfg file and Use Time Overlaps (StudentSct.TimeOverlaps) is set to true.
        - BUG FOUND AND FIXED
            - On the UniTime CPSolver's Student Sectioning Data Format link (https://www.unitime.org/sct_dataformat.php),
            for the two time placements overlap condition, the 'dates', 'days', and 'times' conditions are all joined by
            'AND'. This means that for there to be a time overlap conflict for a student, two  sections have to also be taking
            place on the same date. In InputProcessing.py, when I added the 'dates' attribute for a section, I set it to an
            empty string (i.e. it will be an empty string for all sections [Lab Section sessions]). 
            So a binary XOR of two empty strings probably returns a zero value by the solver, meaning that
            according to the solver there is no date overlap thus no time overlap. 
            - So I fixed the bug by setting the 'dates' attribute of a section's time element to "1". 
            - Solution obtained is 210926_225901. Solution had 9 course requests unassigned, meaning there is 8 time overlap conflicts
            in this solution to the actual input of this problem instance.
            - To answer my question: In the solution.xml, for a course request that has a Time Overlap conflict with an existing assigned 
            section of a course request for that student (i.e. no section was assigned to the course request) 
            there is no 'best' element added as a sub-element to this course request's ('course') element
                - i.e. Unassigned course requests in the solution.xml file will not have a <best> sub-element added to it.
            - After I obtained the 210926_225901 solution, I undid the changes that I made to the Courses.xslx and Students.xlsx file
            to test the time overlap conflict (i.e. removed the BIOL222 course and its course request for the student 218047643)
        - **This bug means that all my previously obtained solutions up to this point probably have Time overlap conflicts
        within them, and that they went unchecked, and that the time taken by the solver are quite shorter than what they should have been.**
            - The solver would've taken the Termination.TimeOut time as no complete solution would've been found. But if there was a complete 
            solution, the solver would've probably taken longer as it would have needed to check for and solve time conflicts from already
            allocated course requests
        - Due to this bug, 2020-Sem1-CAES-Wvl-no-extra-requests instance no longer gives a complete initial solution
            - I've created a child of this problem instance - 2020-Sem1-CAES-Wvl-no-extra-requests-testing - to use to develop and test
            ModifiedInputProcessing.py on.
                -  The change I made: In the initial Students.xlsx input file, I only kept the last 100 students and removed the rest above them.
                - I've created this instance as processCurrentSolution() takes too long (for my liking), a couple of minutes, to process the 
                entire Students input (as I'm making small changes and then running and testing). Furthermore, there is no Time overlaps conflicts
                in this problem instance - we get a complete solution
                                
11. Minimal Perturbation Experimentation process                
    - Simulating students making changes to their registrations/enrollments, and resolving on updated input to get an updated solution
     and evaluating number of existing variables (course requests) whose assigned values (allocated sections) get changed
    
    - Default functionality of my system: Everytime an updated input data XML file is generated by ModifiedInputProcessing.py based on the modified/updated 
    Students input, it replaces/overrides the previous input data XML file (as my solver code (Main.java) assumes that the name of input data 
    XML file is the same as that of the problem instance). So ModifiedInputProcessing.py makes the same assumption and the input data XML file 
    that we obtained is the current one instead of the first input data XML file for this problem instance.
    If the user wants to obtain a completely new solution from scratch, they can rerun the InputProcessing.py script
    to obtain an input data XML file with all course requests being unassigned. 
    **HOWEVER**, for my experimentation process, I will be using a different XML file name for the (first) updated input data XML file 
    (suffixing 'updated-1' to the file name), so the initial input data XML file remains unchanged so that I can run multiple 
    different experiments (multiple independent solver runs) on the same initial input and initial solution but with different 
    modified Students input files (different Student changes -> different [but parallel] updated input data XML files to obtain different updated solutions)

    - Dealing with the Time Overlap conflicts in the 2020-Sem1-CAES-Wvl-no-extra-requests problem instance. 
        - I created a modified/child instance (2020-Sem1-CAES-Wvl-no-conflicts) of this 2020-Sem1-CAES-Wvl-no-extra-requests problem instance
        by removing the 8 course requests for MATH196 from those 8 students who also do BIOL196. [Discovered this conflict in solution 210926_225901]
            - Students: 219009466, 219013287, 219018827, 219021664, 219027743, 219030037, 219033547, 218000612
        - I did this as I would like to use a complete initial solution when experimenting
            - I also intend to use the other problem instances (containing incomplete initial solutions) for experimentation
            to show the different cases (TODO)
            
    - Using the 2020-Sem1-CAES-Wvl-no-conflicts problem instance for this Minimal Perturbation Experimentation process
    
    - Creating multiple parallel (first) modified/updated Students excel input files (i.e. Students-1.xlsx) representing different 
    Scenarios (% of additions and modifications, % of individual capacities filled etc.) for this problem instance.
        - The modified Students.xlsx files are the entire Students' input data for the problem instance, not just containing
        the course requests that need to be added/removed. 
        - The current scenario's Students-1.xlsx file will be placed in the folder of this problem instance so that
        the updated input data XML file and updated solution folder can be obtained. Thereafter a folder inside this problem instance's 
        folder will be created for this current scenario and these 3 items will be placed inside it, so that the next scenario's updated 
        Students file can be placed in the problem instances folder so that the next scenario can be run, and so on.
            - Update: for SeparateModifiedInputProcessing.py, additional files are also generated for this current 
            scenario and stored in the problem instance's folder - the full updated solution XML file and the TXT and XML files 
            for this updated solution's section allocations - and so they will also need to be placed inside the folder of the 
            current scenario
        
    - Creating a separate solver config file (SolverConfiguration-resolving.cfg) to be used here so that I can set the 
    Termination condition to be MPPTerminationCondition.
        - I'm doing this as for the (first) updated solution I got for Scenario 1, there are a number of existing course requests that have 
        their allocated sections being changed. So I'm using MPPTerminationCondition instead of GeneralTerminationCondition
        for the resolving part to see if we can get an updated solution that minimises the number of existing course requests
        that get their allocated sections changed (ideally we want 0, so I set the attribute MinPerturbances's value to 0). 
            - See Issue #7
            - Upon obtaining another updated solution after changing the termination condition to MPPTerminationCondition, 
            but there are still changes being made to existing course requests.
    - BUG FOUND AND FIXED
        - Bug: In ModifiedInputProcessing.py when I am asking the user to enter the number/index of the solution that they want to use
        as the current solution, I did not convert the input to an int, so when I was doing validation checking on the input
        they entered, a TypeError would've been raised (when comparing the current solution string to the ints' 0 and solutionIndex) 
        and the current solution would have been set to the default (the last of the solutions from the CurrentSolutions.txt file) in the
        'except' block. This didn't actually cause a problem until now as I was resetting the CurrentSolutions.txt file when processing/reprocessing
        the input so there would've been only 1 solution listed, which would've also been the last of the solutions. But for the Experimentation part,
        I'm not resetting the CurrentSolutions.txt file as I want to use keep on using the initial solution to obtained different updated solutions
        for different scenarios.
    - Trying to fix perturbations problem
        - Testing changes on the SolverConfiguration-resolving.cfg file (modifying parameter values and adding parameters) on Scenario 1, Scenario 2, 
         and Scenario 3 (See Exp-S1, Exp-S2 & Exp-S3 folders containing the solutions generated)
            - Still got the unnecessary perturbations, and the number of permutations is not going down much
            - Got extra parameters for the config file from: https://www.unitime.org/text.php?file=mpp12
            - Also see:
                - https://www.unitime.org/api/cpsolver-1.3/org/cpsolver/ifs/heuristics/GeneralValueSelection.html
                - https://www.unitime.org/api/cpsolver-1.3/org/cpsolver/ifs/heuristics/GeneralVariableSelection.html
                - https://www.unitime.org/api/cpsolver-1.3/org/cpsolver/ifs/solution/GeneralSolutionComparator.html
            - Parameters experimented with
                - Changed: Termination.MinPerturbances, Comparator.Class, Value.Class, Value.WeightNrAssignments, 
                Neighbour.RandomUnassignmentProb, Neighbour.RandomUnassignmentOfProblemStudentProb
                    - Comparator.Class: tried out org.cpsolver.ifs.solution.MPPSolutionComparator
                    - Value.Class: tried out org.cpsolver.ifs.heuristics.GeneralValueSelection 
                - Added: General.MPP, Value.MPPLimit, Value.InitialSelectionProb, Variable.RandomSelection   
        - I've tried using a new initial solution (211018_210933) but the  same number of STAT130 perturbations (18) are coming up              
        - There seems to be a problem with STAT130
            - Most perturbations are for STAT130 course requests
                - In the case of Scenario 2 & 3, all perturbations are for STAT130 course requests
            - In Scenario 3, there's no STAT130 course requests additions/deletions in the student modifications but all the 
            perturbations are for STAT130 course requests
            - There seems to be a section allocation disbalance for STAT130 in both the initial solutions I've obtained
                - AND it seems that all the updated solutions (resolving on updated input) are trying to fix this section 
                allocation disbalance for STAT130. **I think this is what is resulting in the perturbations for STAT130**
                    - For disbalance details, search for the following in /../resources/Readme.md:
                        - "Looking at STAT130 since it had the most number of changes"
                        - "Initial (complete) solution: 211018_210933"
                    - Maybe its happening for STAT130 cos it is the last course in the courses list? If true, does this mean
                    that this will happen to whatever the last course is?
                    
        - I've relooked at the UniTime API online and I've discovered that there's also EqualStudentWeights class. 
        The current Comparator.Class and StudentWeights.Class values in both config files are set to PriorityStudentWeights. 
        So I've gone and changed these parameters to EqualStudentWeights. It seems that for PriorityStudentWeights, the solver 
        assigns different weights to a student's course requests, with higher priorities having higher weights. 
        EqualStudentWeights gives equal weight to all the student's course requests. 
        Even though I've set the course request priorities to be the same (priority="0") when generating the initial input data XML file, 
        it seems that the solver is setting its own priorities for student's course requests - the request-priorities.csv file 
        in a solution folder has priorities numbered from 1 to numProcessedCourseRequests for each student. Maybe its setting its own 
        priorities as the StudentWeights.Class is PriorityStudentWeights.
                - Student Sectioning weights package: https://www.unitime.org/api/cpsolver-1.3/org/cpsolver/studentsct/weights/package-summary.html
            - I want to see if I set  Comparator.Class and StudentWeights.Class to EqualStudentWeights, if this will solve 
            the STAT130 section allocation disbalance
            - I've changed the parameter values and then obtained a new initial solution (211019_000822)
            - However, the same disbalance is still present, and request-priorities.csv still has different priorities 
            for each student's course requests
                
        - Created a Python program script (SectionAllocations.py) that processes a solution file to obtain the number of allocations
        for each of the sections (and related data - num course requests for each course, total num allocated for each lab, section's timeslot, 
        % allocated for each section, and % allocated for the lab in total), displays it to the console and writes it to an XML file (allocations.xml) 
        and a text file (allocations.txt) in the folder of the solution
            - I've done this so I can look at how well balanced the sections of each lab are, for the initial solutions, 
            and which courses have a section allocation disbalance
            - I'm defining a section allocation disbalance to be when a lab's allocation %'s for its sections differ by 5% or more.
            - Courses that have a section allocation disbalance (occurs on all 3 initial solutions I've got for 2020-Sem1-CAES-Wvl-no-conflicts)
                - CHEM196
                    - all 4 sections' capacities are 48
                    - S17 allocated 46-48 students whilst S16, S18, S19 allocated 33-37, 33-37, 30-33 students respectively
                - STAT130
                    - S42 allocated to 267-270 students; capacity = 491; % allocated = 54%-55%
                    - S43 allocated to 253-250 students; capacity = 544; % allocated = 47%-46%
                    
        - Created a sub-instance (2020-Sem1-CAES-Wvl-no-conflicts-no-STAT130 problem instance) of this problem instance that 
        removes STAT130 from the courses input file (so that course requests for it don't get processed), to see if any perturbations
        still occur after simulating students making changes
            - Ran the solver and obtained an initial and updated solution (used Scenario 1 for student modifications)
                - There are NO perturbations (NO section allocation changes to existing course requests)

12. Since we're getting some perturbations (existing course requests that get their allocated sections changed) that 
shouldn't occur (due to possible section allocation disbalances) - although it's occurring only for STAT130 in the 
2020-Sem1-CAES-Wvl-no-conflicts problem instance, for other problem instances it could occur for any other course, 
and more than one course, and a much larger number of perturbances - we are going to solve the new course 
requests separately and merge the obtained solution with the current solution to represent the updated solution.  
    - Creating a Python program script (SeparateModifiedInputProcessing.py) to do so. It contains two processes, the first being to
    generate an updated input data XML file that represents only the new course requests (with the updated capacity values of the lab sections), 
    along with the initial(current) solution file with the old course requests removed (and also the new course requests added), 
    and the second being to take the (updated) solution file that was obtained by running the solver on the input data XML file generated by 
    the first process (i.e. this solution file contains the solutions of the new course requests) and merge it together with the 
    initial solution (i.e. the previous current solution) that has the old course requests removed (and also the new course requests added), 
    resulting in an entire/full updated solution file. This 'merging' that was done to obtain the entire/full updated solution file 
    was basically adding/assigning the section allocations of the new course requests to a copy of the initial solution XML file (it had the
    unassigned course requests already there)
        - For the first process, I first though of doing the entire code from scratch, and to just generate an input data XML 
        file of the new course requests (instead of the entire input data & all course requests with the initial solutions added, 
        which ModifiedInputProcessing.py does). And the solution obtained on thus input data XML file, I'd merge it with the actual solution file.
        But then I thought of using some of the code from ModifiedInputProcessing.py - reusing some of the functions, as some
        of the initial program functionality of SMIP.py  is the same as that of MIP.py.  
        I then thought that maybe I can model this separate redoing part along the lines of ModifiedInputProcessing.py by following the approach I did there and 
        adding some code to its functions, so that I do not have to write a lot of new code, which is what would've happened if I followed 
        my initial idea (my initial idea did not involve getting the entire solution dict as I did in MIP, as getting the dict takes a lot 
        of time, so  I was thinking of working on the solution file directly). My first idea was to modify processModifiedStudentsData() in MIP.py,
        by adding a parameter called 'caller' and if 'caller' was set to "SMIP", then I'd add code to it to create the input data XML file with
        only the new course requests there. But I settled on not having this parameter, but creating an additional sub-dictionary of updatedInputDict
        called studentsNewRequestsDict that contains the data of only the new course requests (the students who have new course requests, and 
        their new course requests), and I'd create its corresponding input data XML file inside SeparateModifiedInputProcessing.py
            - So for this first process, I created a function inside SeparateModifiedInputProcessing.py called generateNewRequestsInputXmlFile()
            that basically does ModifiedInputProcessing.main() - I'm going to treat the generated updated input data XML file as the current solution file
            with the old course requests removed, and the new course requests are already added there (without their allocations) - and I'm going to 
            add code to create the input data XML with only the new course requests (and the capacity values of the lab sections being updated to account 
            for the students already sectioned), which will be named the current input data XML file name with "-newrequests-<modVerNum>" being appended.
            - So for the second process of SeparateModifiedInputProcessing.py, I created a function called generateUpdatedSolutionFile(), that 
            takes the solution file generated by the solver on the input data XML file containing only the new course requests, gets 
            the section allocations and adds them to their respective course requests in (a copy of) the updated input data XML file - which 
            represents the current solution - to obtain the full updated solution file, which is named as the current input data XML file name 
            with "-fullsolution-<modVerNum>" appended, and stored in the problem instance's directory. 
    - I want to ensure that the IFS Solver (from my Main.java's main() method) is run to obtain the solution for the new course requests, 
    before we do the second process of merging the 2 solution files. And since both processes will have to be run by the user, I only want them
    to have to run this script once. So what I intend to do is to make the SeparateModifiedInputProcessing.py script do the first process, run the solver 
    to obtain the solution for the new course requests, and then run the second process (instead of asking the user which process they want to run). 
        - So since my running of the solver is in Java, I needed a way to run Java code from Python. I discovered the py4j package, but it wasn't installing 
        when I tried to install it using the PyCharm Install packages option (my Python version I got installed is Python 3.8). 
        I discovered on their website that it has been tested up till Python 3.7.
            - So I downloaded Python 3.7 and decided to also create a Python 3.7 virtualenv virtual environment for this project - by going Project Structure -> 
            SDKs -> Add ... - which is located at /venv-py37 in this project's directory and named Python 3.7 (ifs-solver) in the Project Structure, 
            and I changed the Python Interpreter for SeparateModifiedInputProcessing.py to this virtual environment [Python 3.7 (ifs-solver)]
            I then had to activate this virtual environment before I could install any packages inside it. Activated it using cmd by 
            going to (changing the directory) this virtual environment's directory (which is located inside this project) and  to its Scripts folder 
            and typing 'activate'. Installing any packages from the Packages tab of this virtual interpreter in Project Structure was giving an error each time, 
            so I went back to the cmd window and installed the packages from there, using the command  "py -m pip install <packageName>", and it worked. 
            I installed all the packages that SeparateModifiedInputProcessing and ModifiedInputProcessing use (beautifulsoup4, pandas, py4j)
                - Since for the Python 3.7 virtual environment, the package's also weren't getting installed from the Install packages option in the Project Structure, 
                and for Python 3.8 the py4j package similarly was giving an error from the install packages option in PyCharm, I decided to create a virtual environment
                for Python 3.8 and install the packages from cmd, and it worked.
                - I then changed the interpreters for the other Python scripts from the default Python 3.8 to the Python 3.8's 
                virtualenv virtual environment [Python 3.8 (ifs-solver)] I created in this project
        - I've now discovered that Python virtual environments are for Python packages (specifically project dependencies involving them)
        instead of for Python interpreter itself - my initial thinking was that if I use a Python virtual environment then I don't have to worry 
        about the user of my system having to have the right version of Python and having to have the packages installed. But this is not the case, 
        and according to StackOverflow it is not recommended to add your virtual environments to version control and Git. 
        - I've also discovered PyInstaller, which lets you create an executable of your project, including its dependencies.
        - I've discovered the jpype package (to access Java from Python) and I'm going to try it out instead of py4j as 
        py4j requires you to have a gateway running.
            - Ran the following 3 commands in cmd in the directory of the Python 3.8 (ifs-solver) virtual environment (/venv-py38/Scripts)
                - git clone https://github.com/originell/jpype.git
                -  cd jpype
                -  python setup.py install
            - jpype not working - giving an error:  "jpype._jvmfinder.JVMNotFoundException: No JVM shared library file (jvm.dll) found. 
            Try setting up the JAVA_HOME environment variable properly." even after setting the JAVA_HOME variable. According to StackOverflow, 
            it could be because my JVM architecture doesn't match my Python one, and my Java is 64-bit whilst my Python is 32-bit. So I've gone 
            and installed a 64-bit version of Python 3.10 (the latest version of Python) and its relevant packages (including jpype)
            and also _**created a JAVA_HOME environment variable and set it to the Java JDK path_**.
                - I also changed the interpreters for all the Python scripts to the Python 3.10 system interpreter 
                - Still getting an error when installing Jpype for Python 3.10 using pip in cmd. It's involving VS Tools.
                I then found the following suggestion: https://github.com/sammchardy/python-binance/issues/148#issuecomment-374853521 and
                followed it. This also appied for installing lxml for Python 3.10 
                - Still getting an error with the Jpype function, so I went to Project Structure -> Modules -> Dependencies and added
                the library Python 3.10 and it now works
                - When running Jpype to access my java class Main.java it is giving an error that it can't find the specified package
                I searched online and found out that I need to create a jar file of my Java class first, so I did that.
                IT's FINALLY WORKING. I GOT MY JAVA CODE RUNNING IN PYTHON.
                    - Remember to rebuild the Jar file everytime I modify the Java code
                - Since I'm using Python 3.10 now, I removed the Python 3.7 and 3.8 and also their virtual environments from Platform Settings -> 
                SDKs (and also deleted their folders), and also removed Python 3.8 from Project Settings -> Modules -> Dependencies

13. Returning to the Minimal Perturbation Experimentation Process
    - Ran Scenario 4 of the 2020-Sem1-CAES-Wvl-no-conflicts problem instance
    - **A realisation I've made now: Since for SMIP.py, I'm generating an updated input data XML file that represents 
    only the new course requests, for modified students only their new course requests will be in this file and their existing 
    course requests (with their current section allocations won't), so when the solution to the new course requests is merged 
    with the initial solution, there _may_ be Time Overlap Conflicts for the modified students as the allocations for the new requests
    weren't checked against the allocations (and their timeslots) for their current requests**
        - So what I need to do is to go back and recode SMIP.py such that for new course requests of existing students (modified Students),
        all the existing course requests (with their section allocations) for that student should be added along with their new course requests, 
        to the new requests input file, so that the solver can check for Time Overlap conflicts and make any changes if necessary
        - Alternatively, we can leave it as is and mention to do this in Future Work/Improvements

14. Processing additional datasets
    - 3 datasets for CAES 2021 Sem 2 (Wvl, Howard, PMB)
        - The original Students Excel files are named "CAES Tutorial Groups 2021_2 <CAMPUS> - 2021-08-20"
        - No courses data has been provided so I have to get my own (can't reuse from 2020-Sem1-CAES-Wvl as that was for Semester 1)
            - UKZN's timetable.ukzn.ac.za site is down
                - UPDATE: use http://timetable.ukzn.ac.za/Homepage.aspx (**TODO**)
            - Sir provided the following direct link to access the timetables for the courses on the Westville (Wvl) campus for Semester 2: 
            https://celcatwp.ukzn.ac.za/2021/WESTVILLE/SCIENCEAGRICSEM2/finder.html
                - If I change 2 to 1 then I can access the timetables for CAES WVL Semester 1. But I can't find the right URL 
                change to access the timetables for Howard College and PMB campuses
            - Since I've got the timetables for each CAES course (and not only for the first year courses) we won't have any CAES
            courses not being processed, only non-CAES courses will not be processed (i.e. Issue #1 will only affect non-CAES courses, 
            as they wouldn't have been specified in the Courses.xlsx input file) - although I can go and find out which non-CAES courses
            the students in the Students.xlsx input file are doing, and get their timetables and add their course offerings to the 
            Courses.xlsx input file
        
    - 2021-Sem2-CAES-Wvl
        - Obtained the course offering details (of their lab sessions) of the CAES courses using the timetable link
        - Some courses had multiple labs (both practicals and tutorials)
        - Cannot specify exact capacities as they are not specified in the timetables on the timetable site
            - For my experimentation, I put a capacity of 500 for each Lab Section. In the paper, mention that due to the 
            proper/exact capacities not having been specified, this problem instance is not ideal (as it won't give availability conflicts
            due to the high capacities specified)
        - Only specified/processed the course offerings in the in Courses.xlsx input file for first year and second year CAES courses
            - The Students input file we're given is for students doing first-year CAES courses (CAES want to do the sectioning for first year labs), 
            and its highly unlikely that a student doing a first year CAES course will also be doing a third-year CAES course. And by searching through the 
            Students input file for each third year CAES course, there are very few students in that file that do them (if any), 
            and the numbers are usually just 1 or 2 students. 


Order of run:\
    1. InputProcessing.py (input data XML file)\
    2. Main.java (initial solution - userAnswer==0)\
    3. ModifiedInputProcessing.py (updated input data XML file)\
    4. Main.java (updated solution - userAnswer==1)\
    5. SectionAllocations.py (allocations data for both initial and updated solution)
    
    
Order of run (updated):\
    1. InputProcessing.py (input data XML file)\
    2. Main.java (initial solution - userAnswer==0)\
    3. SeparateModifiedInputProcessing.py (option 0 - updated input data XML file [current solution] + new requests input data XML file)\
    4. Main.java (solution for new course requests - userAnswer==2)\
    5. SeparateModifiedInputProcessing.py (option 1 - merge solutions to obtain updated solution file, and the updated Section Allocations data)

Order of run (updated 2):\
    1. InputProcessing.py (input data XML file)\
    2. Main.java (initial solution - userAnswer==0)\
    3. SeparateModifiedInputProcessing.py (now does steps 3, 4, and 5 above)

 
 
TODO: MENTION IN PAPER: Since the IFS solver balances the section allocations when doing them, for each course request in the resolving part, 
it most probably will have the option to choose from all the sections for the labs of that course (as in the initial solution the 
allocations were balanced so there should be space in all sections unless num course requests for a course is very close to lab capacity), 
so we DON'T need to remove/unallocate any allocations for the existing/unchanged course requests in the initial/current solution to free up section space (to 
give new course requests an opportunity to be sectioned into other sections)  

 
 If a course have multiple labs and a student who has a course request for this course has a section conflict (either availabilty of time overlap conflict) 
 in being allocated to one of the (sections of one of the) labs of this course, will not be allocated to any (to any sections to any other) of the labs 
 of this course (even though there is ample  available space and no time overlaps in the other labs of this course for this student to be allocated to) 
 - i.e. the course request will remain unallocated (Refer to 2021-Sem2-CAES-Wvl's initial solution)
 
TODO: new updated input data XML file should not replace old one - create separate ones for each modified Students file


TODO: Create a Main.py script where we can set the name of the problem instance in one place, and which lets us choose which of 
the other script's we'd like to run, and can pass in the name of the problem instance to their main methods



TODO: talk about code I changed specifically for the experimentation process
    - also the code in Main.java - to determine which configuration file i should use

TODO: have a text file in the instance folder with the current solution round num - initialise to 0 for initial solution.
    this helps ModifiedIP  to decide which input data Xml file to select, and Main.java to decide which input data xml file to select (if 
    we not overwriting the initial file). Alternative use modVerNum from getModifiedStudentsFilePath() and subtract 1 to get solNum
    
TODO: look at variables in the Solver config files
TODO: WHAT IS AVERAGE DISBALANCE IN THE SOLUTION INFO FILE???

TODO: do experimentation on the original problem instances (that gave incomplete solutions) so that we can show what happened for those cases

TODO: in submission docs, talk about me having to go through the CPSolve code to understand what to do. and not much documentation 
given on how to use the code, and that I had to fix couple bugs

Todo - see Toby for the  chrome tabs I had open    
Todo - update (re processes) the input data XML file for all other problem instances (based on additions made to InputProcessing.py on 22/09/2021

TODO: do experimentation on being able to have multiple updated Students input files and being able to obtain successive updated solutions - speak about
this in the paper
    
[Done] Todo: MAKE CHANGES AND RESOLVE - try out different termination conditions<br>
[Done] Todo: Try out different heuristics. (modify config file)
To see: https://www.unitime.org/api/cpsolver-1.3/org/cpsolver/studentsct/heuristics/StudentSctNeighbourSelection.html <br>
Todo: DO A COMPLETE USER-SYSTEM OF THIS CPSOLVER FIRST<br>

Todo: Change Xmx option (Memory heap size of JVM)
    - See:
        - https://stackoverflow.com/questions/5374455/what-does-java-option-xmx-stand-for
        - https://www.jetbrains.com/help/idea/increasing-memory-heap.html
        - https://www.jetbrains.com/help/idea/tuning-the-ide.html
        - https://intellij-support.jetbrains.com/hc/en-us/articles/206544869-Configuring-JVM-options-and-platform-properties
        
        
## Reference and Acknowledgement Links
https://www.datacamp.com/community/tutorials/python-excel-tutorial
https://openpyxl.readthedocs.io/en/stable/
https://openpyxl.readthedocs.io/en/default/pandas.html
http://docs.pyexcel.org/en/latest/
http://docs.pyexcel.org/en/latest/tutorial_file.html

https://realpython.com/python-dicts/
https://www.geeksforgeeks.org/python-dictionary/
https://docs.python.org/3/tutorial/datastructures.html

https://www.crummy.com/software/BeautifulSoup/bs4/doc/
https://www.crummy.com/software/BeautifulSoup/bs4/doc/#the-keyword-arguments

https://www.geeksforgeeks.org/with-statement-in-python/

https://www.pythontutorial.net/python-string-methods/python-string-index/
https://www.tutorialsteacher.com/python/error-types-in-python
https://docs.python.org/3/library/exceptions.html
https://stackoverflow.com/questions/9572490/find-index-of-last-occurrence-of-a-substring-in-a-string?rq=1

https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop_duplicates.html
https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop.html
https://stackoverflow.com/questions/21800169/python-pandas-get-index-of-rows-which-column-matches-certain-value
https://stackoverflow.com/questions/5844672/delete-an-element-from-a-dictionary

https://www.geeksforgeeks.org/python-get-dictionary-keys-as-a-list/
https://stackoverflow.com/questions/1679384/converting-dictionary-to-list

https://realpython.com/iterate-through-dictionary-python/

https://realpython.com/python-time-module/#python-time-in-seconds-as-a-string-representing-local-time

https://www.geeksforgeeks.org/reading-writing-text-files-python/
https://realpython.com/beautiful-soup-web-scraper-python/#find-elements-by-class-name-and-text-content

https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments
https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/
https://www.py4j.org/index.html - connect Java to Python (run Java code from within Python)
                
https://libzx.so/main/learning/2016/03/13/best-practice-for-virtualenv-and-git-repos.html                
https://stackoverflow.com/questions/6590688/is-it-bad-to-have-my-virtualenv-directory-inside-my-git-repository
https://stackoverflow.com/questions/44827624/why-would-you-create-a-requirements-txt-file-in-a-virtual-environment-in-python?noredirect=1&lq=1
https://stackoverflow.com/questions/67188483/is-it-a-good-practice-to-use-python-virtual-env-as-a-way-of-deploy-python-app?noredirect=1&lq=1
            
https://stackoverflow.com/questions/60390858/jpype-getdefaultjvmpath-fails-when-i-try-accessing-jvm-from-python3
https://stackoverflow.com/questions/13596505/python-not-working-in-command-prompt
https://github.com/sammchardy/python-binance/issues/148#issuecomment-374853521

https://stackoverflow.com/questions/3652554/calling-java-from-python
https://www.tutorialguruji.com/python/jpype-simple-jar-import-and-run-main/
https://www.jetbrains.com/help/idea/compiling-applications.html#package_into_jar
https://stackoverflow.com/questions/23521273/class-not-found-error-on-jpype
https://stackoverflow.com/questions/44033891/jpype-python-importing-folder-of-jars
            
https://jpype.readthedocs.io/en/latest/
https://jpype.readthedocs.io/en/latest/userguide.html
https://jpype.readthedocs.io/en/latest/quickguide.html

https://stackoverflow.com/questions/21356014/how-can-i-insert-a-new-tag-into-a-beautifulsoup-object
https://www.crummy.com/software/BeautifulSoup/bs4/doc/#navigablestring-and-new-tag
https://stackoverflow.com/questions/40529848/how-to-write-the-output-to-html-file-with-python-beautifulsoup
https://stackoverflow.com/questions/42649596/can-i-make-beautiful-soup-keep-the-attributes-ordering-and-lines-indentation
https://gist.github.com/dmattera/ef11cb37c31d732f9e5d2347eea876c2

https://stackoverflow.com/questions/73663/how-to-terminate-a-script

https://www.geeksforgeeks.org/beautifulsoup-modifying-the-tree/
https://stackoverflow.com/questions/9766966/how-to-set-value-in-with-beautiful-soup-in-some-html-element-if-i-know-id-of-tha
https://www.geeksforgeeks.org/python-string-replace/
https://www.geeksforgeeks.org/python-string-strip/