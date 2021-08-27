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
7. Creating input files for CAES-2020-Sem1-Wvl according to my templates
8. Creating a Python program script (InputProcessing.py) inside this ifs-solver project to read in and process input files, and produce an XML file (input data file)
 for the UniTime Student Sectioning solver according to their data format structure/template
    - Current input files I'm using are the CAES-2020-Sem1-Wvl problem instance
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
 9. Running the UniTime's Student Sectioning CPSolver
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
        - Created a org.talhavawda.ifssolver package inside the src/main/java directory and added a Main file with a main() method. 
        Then I added code to my Main.main() method to set up the string parameter variables, and then called org.cpsolver.studentsect.Test.main() with its arg param being the array of my string parameter variables.
        - Was getting a NullPointerException error during the XML Loading process - I didn't specify a 'dates' attribute for the 'time' element of the 'section' element in my XML input file generation
            - I fixed this by setting a 'dates' attribute with the value being an empty string
                - Todo: Consider changing this 'dates' value to something more meaningful
        - Then I was getting an error cos I didn't put priority attribute for course requests (NumberFormatException). Fixed that also.
        - It's working now 
        - I modified the default configuration file given by UniTime to tune it to my specific Student Sectioning Problem
            - SEE src/main/resources/Readme.md for info about the configuration file I'm using for the solver
        