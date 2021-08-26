# IFS Solver

This project is for testing UniTime's CPSolver (that makes use of the Iterative Forward Search (IFS) algorithm) 
to solve my Student Sectioning problem.

This project is being developed using Java (as the CPSolver is available in Java only) in IntelliJ IDEA.

## What I've done (Steps)
1. Created this project (ifs-solver) in IntelliJ inside my local copy of the student-lab-sectioning repository
    - This automatically adds the project to Git and I can access Git features inside IntelliJ
2. I created a 'lib' folder (Right Click -> New -> Directory) and added the CPSolver javadoc files to the lib folder.
3. I right-clicked the 'lib' folder and selected 'Add as library'
4. Created sub-directories in the src folder
    - 'main' and 'test' sub-directories
        - In the 'main' sub-directory, I created 'java' and 'resources' sub-directories and marked them as Sources 
        and Resources respectively in the Project Structure
        - In the 'test' sub-directory, I created a 'java' sub-directory and marked it
        as Tests in the Project Structure
5. Studying the Data Format of the UniTime Student Sectioning solver
6. Creating my Excel template input files
7. [Incomplete] Creating input files for CAES-2020-Sem1-Wvl according to my templates
8. [Incomplete] Creating a Python program script to read in and process input files, and produce an XML file (input data file)
 for the UniTime Student Sectioning solver according to their data format structure/template
    - How to run Python in IntelliJ:
        - Links
            - https://www.jetbrains.com/help/idea/configuring-local-python-interpreters.html
            - https://www.jetbrains.com/help/idea/configuring-python-sdk.html
            - https://www.jetbrains.com/help/idea/run-debug-configuration-python.html#1
        - Then go to Project Settings -> Moudules -> Dependencies -> Add Python interpreter
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