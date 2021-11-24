# student-lab-sectioning
## Student Lab Sectioning with Minimal Perturbation

### Execution instructions (COMP700 Project marking)

The datasets are placed inside this project. Their problem instances are located in the ifs-solver/src/main/resources/input directory. Note that downloading a local copy of this repository may take a while due to the large cummulative file size of the generated experimentation results.

The JAR file (ifs-solver.jar) for the Java sub-system of this project could not be commited to (and is thus not present in) this remote cloud-hosted repositiory as its size is above GitHub's 100MB file size limit.
Download the JAR file (ifs-solver.jar) from [this link](https://drive.google.com/drive/folders/1AWqlMftnSjfEWUG8ZbypLO7Ou7nbc0Yo?usp=sharing) and place it inside the following sub-directory of the ifs-solver project: /out/artifacts/ifs_solver_jar/.


#### Dependencies
Ensure that you're running 64-bit versions of Java and Python.
Specifically, Java SDK 13.0.1 and Python 3.10 (both 64-bit) have been used in the current version of this project.

The following libraries need to be installed: pandas, beautifulsoup4, mindom, openpyxl, lxml, and JPype. All but JPype can be installed normally using pip or through an IDE (IntelliJ/PyCharm).
JPype needs to be installed by running the following 3 commands in cmd:
- git clone https://github.com/originell/jpype.git
-  cd jpype
-  python setup.py install

If there's an error installing JPype which involves VS Code, follow the instructions in [this comment](https://github.com/sammchardy/python-binance/issues/148#issuecomment-374853521) to download and install the whl package for you python version, and then re-attempt to install JPype. This also applies if you're using Python 3.10 and getting an error installing lxml using pip.


#### Execution
First download the ifs-solver project. This can be done by downloading a ZIP folder of this repository and extracting the ifs-solver project. 

To run the projec: In Command Prompt, change your current directory to the directory (on your local machine) of the Main.py script in the ifs-solver project 
and run Main.py using the following command: 'python Main.py'


Obtaining solutions with Main.py:

1. Run InputProcessing.py which obtains the initial input data XML file and runs the CPSolver to obtain the initial solution
2. Run ModifiedInputProcessing.py to process a modified Students input data Excel file and runs the CPSolver to obtain the updated solution. 
Note that for ModifiedInputProcessing.py, there may be perturbations for students with unchanged course registrations in the updated solution. 
If you want an updated solution for which perturbations for students with unchanged course registrations do not occur, run SeparateModifiedInputProcessing.py, 
which shall obtain the allocations of the Students with new course requests separately and merge it with the initial solution to obtain the full updated solution.

For the second step above, Main.py will have to be re-executed.


Note that although the option is given in Main.py to run Main.java, the three Python processes above run the Main.java file within them and also specify the solution type 
they want to obtain, so their is no need for the user to run the Main.java file directly. 
 

If want to run the project in an IDE, open it in IntelliJ, add a Python interpreter to the project (if one is not already specified) and create a build configuration for the Main.py file. 
- How to run Python in IntelliJ (adding a Python interpreter):
    - Links
        - https://www.jetbrains.com/help/idea/configuring-local-python-interpreters.html
        - https://www.jetbrains.com/help/idea/configuring-python-sdk.html
        - https://www.jetbrains.com/help/idea/run-debug-configuration-python.html#1
    - Then go to Project Settings -> Modules -> Dependencies -> Add Python interpreter


Refer to the paper for more details on the pipeline and architecture of the project.

