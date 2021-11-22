# student-lab-sectioning
## Student Lab Sectioning with Minimal Perturbation


Download the JAR file (ifs-solver.jar) from this link (https://drive.google.com/file/d/1mjL3uRGLy4oHhna0Td66pcuFo515L6sA/view?usp=sharing) and place it inside the following sub-directory of the ifs-solver project: /out/artifacts/ifs_solver_jar/. The JAR file could not be commited to this remote repositiory as its size is above GitHub's 100MB file size limit. 

Ensure that you're running 64-bit versions of Java and Python.

The following libraries need to be installed: pandas, beautifulsoup4, mindom, openpyxl, lxml, and JPype. All by JPype can be installed normally using pip or through an IDE (IntelliJ/PyCharm).
JPype needs to be installed by running the following 3 commands in cmd:
- git clone https://github.com/originell/jpype.git
-  cd jpype
-  python setup.py install

If there's an error installing JPype which involves VS Code, follow the instructions in this comment: https://github.com/sammchardy/python-binance/issues/148#issuecomment-374853521 to download and install the whl package for you python version, and then re-attempt to install JPype. This also applies if you're using Python 3.10 and getting an error installing lxml using pip.


Running the project: In Command Prompt, change to the directory of the Main.py script and run Main.py using the following command: 'python Main.py'


If want to run the project in an IDE, open it in IntelliJ, and create a build configuration for the Main.py file and set the working directory to the ifs-solver root folder (instead of the sub-folder containing Main.py)

