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
        - In the 'test' sub-directory, I created java' and 'resources' sub-directories and marked the 'java' subdirectory
        as Tests in the Project Structure