# IFS Solver

This project is for testing UniTime's CPSolver (that makes use of the Iterative Forward Search (IFS) algorithm) 
to solve my Student Sectioning problem.

This project is being developed using Java (as the CPSolver is available in Java only) in IntelliJ IDEA.

UniTime Student Sectioning Solver (UniTime site Links):
 - Constraint Solver Examples: Constraint Solver Examples: https://www.cpsolver.org/cpsolver_examples.php
 - Student Sectioning Problem Description: https://www.unitime.org/sct_description.php
 - Student Sectioning Data Format: https://www.unitime.org/sct_dataformat.php
 - Student Sectioning Benchmark Datasets: https://www.unitime.org/sct_datasets.php
 - Student Sectioning Solver Execution: https://www.unitime.org/sct_execution.php
 - CPSolver API Documentation: https://www.unitime.org/api/cpsolver-1.3/index.html
 
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
                - Todo: Consider changing this 'dates' value to something more meaningful
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
    
    - Creating multiple parallel (first) modified/updated Students.xlsx input files (i.e. Students-1.xlsx) representing different 
    scenarios (% of additions and modifications, % of individual capacities filled etc.) for this problem instance.
        - The modified Students.xlsx files are the entire Students' input data for the problem instance, not just containing
        the course requests that need to be added/removed. 
        - The current scenario's Students-1.xlsx file will be placed in the folder of this problem instance so that
        the updated input data XML file and updated solution folder can be obtained. Thereafter a folder inside this problem instance's 
        folder will be created for this current scenario and these 3 items will be placed inside it, so that the next scenario's updated 
        Students file can be placed in the problem instances folder so that the next scenario can be run, and so on.


TODO: WHAT IS AVERAGE DISBALANCE IN THE SOLUTION INFO FILE???

Todo - see Toby for the  chrome tabs I had open    
Todo - update (re processes) the input data XML file for all other problem instances (based on additions made to InputProcessing.py on 22/09/2021

    
Todo: MAKE CHANGES AND RESOLVE - try out different termination conditions<br>
Todo: Try out different heuristics. (modify config file)<br>
Todo: DO A COMPLETE USER-SYSTEM OF THIS CPSOLVER FIRST<br>

Todo: Change Xmx option (Memory heap size of JVM)
    - See:
        - https://stackoverflow.com/questions/5374455/what-does-java-option-xmx-stand-for
        - https://www.jetbrains.com/help/idea/increasing-memory-heap.html
        - https://www.jetbrains.com/help/idea/tuning-the-ide.html
        - https://intellij-support.jetbrains.com/hc/en-us/articles/206544869-Configuring-JVM-options-and-platform-properties
        
        
## Reference and Acknowledgement Links

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

                
            
            
            
