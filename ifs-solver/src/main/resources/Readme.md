Each problem instance must be in its own folder (named appropriately: year-term-initiative) within the 'input' folder
and must contain the following files named as is: "Courses.xlsx", "Students.xlsx", and "Specification.xml"

If the user cannot modify a copy of the SpecificationInputTemplate.xml file in the resources folder, they may use a
copy of the DefaultSpecification.xml file from the resources folder by renaming the copy to "Specification.xml",
and placing it inside the problem instance's folder

When the input files of this problem instance are processed, an input data XML file of the same name as the problem instance
will be generated and stored in this problem instance's folder. And each time the solver is run (on the current input data XML file) 
to obtain a (new/first/initial) solution, a folder will be created for that solution (with its name being the date and time that the solver was run for that solution)
and will be placed inside this problem instance's folder.

Each time the solver is run (on the current problem instance), the name of the solution (its probable folder name) is 
appended to a new line of the Solutions.txt file in the problem instance's folder.
Furthermore, each time the input data XML file is generated (either for the first time or being updated, in either 
InputProcessing.py or ModifiedInputProcessing.py), a blank/empty CurrentSolutions.txt file is created and placed in the 
problem instance's folder, and each time the solver is run on the current input data XML file, the name of the solution 
(its probable folder name) is appended to a new line of this text file. 
So Solutions.txt represents all the solutions obtained for this problem instance, and CurrentSolutions.txt represents 
all the solutions obtained (sibling [independent] solutions to each other) on the current input data XML file of this 
problem instance. 

**_Modified input and resolving_**:
I would like to keep the initial Students.xlsx input file as is (it should not be re-written), so that I can obtain a new solution
to the initial input of the problem instance from scratch if I want to. So a modified Students file will be initialised
to a copy of the current Students input file (whether the initial Students.xlsx or a modified Students input file) and will
be renamed similarly to Students.xlsx but with a dash and a number (modification version number) appended/suffixed to it, 
the modification version number starting from 1, indicating the first modified Students input file. 
E.g. "Students-1.xlsx" for the first modified version of the Students.xlsx input file which was used to  obtain the 
initial solution of this problem instance, "Students-2.xlsx" for the modified version of Students-1.xlsx input file, 
which was used to obtain the first updated solution of this problem instance etc. <br>
All the modified Students input files will be stored in the folder of this problem instance. <br>
ModifiedInputProcessing will ask for the number of the modified input file. <br>
NB. A modified Students file MUST contain the dash, and the mod. ver. number, with no whitespace in between 'Students', 
the dash, and the mod. ver. number <br>
NB. The first modified Students file must have the mod. ver. number to be 1 (and not 2. Assume the initial Students file 
to implicitly have the mod. ver. number of 0). <br>
NB. Each new modified Students input file must increment the mod. ver. number by exactly 1. i.e. no integers may be skipped.
<br>
<br>

### CoursesInputTemplate.xlsx:
The course offerings - the courses, their labs, sections, and capacities, and the allocated/scheduled dates and times 
for their lab sessions (the timeslot allocations for the lab sections).


The venueCapacity field in my CoursesInputTemplate.xlsx doc matches with the
'limit' field of the 'section' tag/element in the CPSolver (See SSDataFormatTemplate.xml)

The sessionLength field in my CourseInputTemplate.xlsx doc matches with the
'length' field/attribute of the 'time' tag/element (which is a sub-tag/element of the 'section' tag/element)
 in the CPSolver (See SSDataFormatTemplate.xml). 
 - [OLD] This represents the number
 of timeslots a session takes up. The default value is 1, and it should only
 be changed when the problem instance contains lab sessions of differing time durations.
    - The number of timeslots per day for the problem instances would've been modified accordingly
    such that 1 represents the shortest duration of a session.
    - The UKZN CAES problem has all lab sessions being of the same duration so it should
    not be affected by this (i.e. all sessionLength values will remain the default 1) 
 - This number represents the length of the lab session in the hh:mm format. It no longer matches with the 'length' attribute
 of the 'time' element. In the code when processing the course offerings in InputProcessing.py, I had to convert from the
  sessionLength time to the number of timeslots. See https://github.com/talhavawda/student-lab-sectioning/issues/10 
 for details about the change from the initial value above
    
<br>
<br>

### StudentsInputTemplate.xlsx:
I am working with the global/universal terms 'Faculty' and 'School' for the academic structure.
 UKZN refers to a 'Faculty' as a 'College'.
 What I refer to as a 'course', UKZN refers to as a 'module'
 
 qualification = degree
 
 I am specifying that the max number of courses a student can be doing in a single semester/term
 is 10, so I shall have 10 columns.
 
 numCourses = number of courses registered for the current semester/term.
 User must ensure that the course specified for each student matches the numCourses value as the
 numCourses value will be used to iterate through the columns and extract the courses of that student from the succeeding columns 
 (I am not going to go through all 10 columns and check for courses (if the field is non-empty) as
  this will be more time intensive)
  
 The 'faculty' field matches with the 'classification' element (sub-element of the 'student' element)
 in the CPSolver
 
 The 'qualification' field matches with the 'major' element (sub-element of the 'student' element) 
 in the CPSolver
 
 TODO - see if I should add the school field as an element or attribute
  
 The user using the program must ensure that all data in the input files are valid - all characters must
 be valid Unicode characters (specifically limit them to letters, numbers, whitespace and keyboard symbols) otherwise an error will result
 
 <br>
 <br>
 
### Configuration File (for CPSolver)
The default file given on the UniTime's website is the 'configFileDefault.cfg' file
I made a copy of it and named it "SolverConfiguration.cfg".
My com.talhavawda.ifssolver.Main.main() accesses it from this resource folder, so don't move it 

Changes made:
- Use student distance conflicts (StudentSct.StudentDist)
    - changed it to false
- Maximal solver time (Termination.TimeOut)
    - changed it to 60 from 28800
    - changed it to 300 from 60
- Stop when a complete solution if found (Termination.StopWhenComplete)
    - changed it to true
- Anonymize XML file (no names) (Xml.ShowNames)
    - changed it to true (to make it non-anonymised)
        - all this does (to the solution) is add the time of the session (as actual text in between the tags)
        to the time sub-element of the section element in the offerings part, and the to the allocated
        section element in the students part 

<br>

### Solutions explanations
#### 2020-Sem1-CAES-Wvl-OLD
- 210828_003504
    - First run. Didn't stop running (due to the high TimeOut value) so I terminated it. 
    
- 210902_105758
    - Configuration File change: changed Maximal solver time (Termination.TimeOut)  to 60 from 28800
    - Solver took 1m
    - Complete solution found.
    
- 210903_204021
    - Configuration File change: changed Stop when a complete solution if found (Termination.StopWhenComplete) to true,
    and Termination.TimeOut to 300 (from 60)
    - Solver took 0.21m (12.64s) [including trying to get a better solution on the initial complete solution]
    - Complete solution found.
    
- 210903_223248
    - Configuration File change: changed Anonymize XML file (no names) (Xml.ShowNames) to true
    - Solver took 0.24m (14.66s)
    - Complete solution found.
    
- 210907_091307
    - Wanted to test the quality of the solution after the initial complete solution is obtained (whether the solution quality increases
    or decreases) since we solving the Optimization Problem of Student Sectioning (we want an optimized solution, not just the initial complete one)
        - Wanted to test it on this OLD problem instance where we managed to obtain a complete solution (100% initial allocation). Cannot obtain a complete
        solution in the current problem instance (2020-Sem1-CAES-Wvl) due to availability conflicts in the BIOL103 and BIOL195 courses
    - Configuration File change (for this solution attempt only): changed Termination.StopWhenComplete to false and Termination.TimeOut to 900
    (so that the solver will continue running after an  initial complete solution is found and will generate many new solutions)
    - See this output folder for results
        - BEST solution value increased very little from initial solution value (maybe because we have already assigned all course request successfully)
        and later solutions seemed to decrease a little (dipping below 100% allocations) but came up again to 100%, and this cycle continued.  
<br>

#### 2020-Sem1-CAES-Wvl
- 210905_212507
    - Running IFS-Solver on updated 2020-Sem1-CAES-Wvl problem instance
    - According to Debug.log file, the program continued running as the initial solution and subsequent solutions
    were not complete solutions, and the solver continued till it reached the TimeOut termination condition (300s),
    and when ShutdownHook was printing info about the solution (before writing to the solution.xml file) in the studentsct.Test class,
    there was a java.lang.NullPointerException with an error message "Test failed.". Thus, there was no output student.xml
    file given.

- 210906_114246
    - Running solver after fixing previous NullPointerException error (added "itype" attribute to each subpart element in the XML input fike).
    - No complete solution found - best solution had 56 course requests unassigned (6118/6174 [99.09%] assigned). 
        - Solution file has "Students missing 1 course: 100,00% (56)"
        - Unassigned course requests in the solution.xml file will not have a <best> sub-element added to it.
            - In the tableau.csv file in the solution folder, the request's Enrolled attribute value will be 'No',
            and the Section value will be empty. In the request-priorities.csv file, the Enrolled value will be 0.
        
- 210906_143728
    - Changed Termination.TimeOut to 900 (changed it back to 300 after this run)
    - No complete solution found. The same 56 unassigned course requests as the previous solution.
        - Upon further digging, it seems that 2 courses are filled to capacity and have more course requests than their capacity:
        The availability-conflicts-real.csv (and conflicts-real.csv, and section-conflicts-real.csv) says that Course C2 (BIOL103) has 18 availability conflicts for its (only) Section S5
        and that Course C3 (BIOL195) has 38 availability conflicts for its (only) Section S6 [both these sections have a capacity of 200]
        If we count the number of Course Requests for BIOL103 and BIOL195, it is indeed 218 and 238 respectively.
            - If we look in the solution.xml file, for those students who were not assigned to a section due to the availability conflicts,
            there is no 'best' element added as a sub-element of their course request ('course') element 
        
- 2020-Sem1-CAES-Wvl-fixing-timeslots (Solutions can be ignored)
    - 210921_213541
        - Decreased timeslot values by 1 in the Courses.xlsx  data file and processed the input, and ran the solver on the 
        updated input data xml file. 
            - This didn't fix the Timeslots issue.
        - Changed Termination.TimeOut to 60 (changed it back to 300 after this run)
    - 210921_222536
        - Running solver after changing the Courses file to adhere to the default timeslot values.
            - See https://github.com/talhavawda/student-lab-sectioning/issues/10 for details.
        - Changed Termination.TimeOut to 60 (changed it back to 300 after this run)
    - 210922_021529
        - Running solver on the modified input where the field names in the Courses.xlsx input file were updated (to sessionDay and sessionStartTime)
        - Changed Termination.TimeOut to 60 (changed it back to 300 after this run)
        
- 2020-Sem1-CAES-Wvl-no-extra-requests
        - This modified problem instance fixes the exceeded course capacity 'error' (availability conflict) in its parent instance (2020-Sem1-CAES-Wvl)
        by increasing the capacities of the 2 courses (BIOL103 and BIOL195) in the Courses.xlsx input file to match the number of requests for those courses, 
        allowing us to get a complete solution
    - 210922_125809
        - Solver took 0.12m (7.13s)
        - Complete solution found.
    - 210922_212224
        - Solver took 0.07m (4.40s)
        - Complete solution found.
    - 210922_212403
        - Solver took 0.15m (8.92s)
        - Complete solution found.
    - 210924_010657
        - Changed the students' id attribute in the input data XML file to be their actual student number's/id's according to their institute,
        instead of starting from 1 for the first student and incrementing by 1 for each student.
        See Issue #13 (https://github.com/talhavawda/student-lab-sectioning/issues/13)
    - 210926_202819
        - When working on ModifiedInputProcessing.py to prepare to add the solutions (assigned sections) to the studentsDict,
        I wanted to test what will reflect in the solution.xml file if there is a time  conflict and thus the student 
        will not be assigned a section for that course request. So I took a student (218047643) and added a course request 
        for them in the Students.xlsx input file for a course that they were already doing that contained only 1 section for its lab (BIOL196).
        So now this student had two course requests for BIOL196. When I generated the updated input data XML file, and 
        ran the solver on it, to my surprise a complete solution was found, and  I saw that the (same) section of BIOL196 
        was assigned to both course requests (thus a time overlap conflict)
        - Solver took 0.35m (20.82s)
        - Complete solution found.
    - 210926_204519
        - After the above solution's (210926_202819) results, I thought that maybe the solver detects if two course requests are for the 
        same course and doesn't consider time conflicts for it. So for the second BIOL196 course request for this student, I replaced BIOL196 with another course,
        BIOL222, a course that doesn't (currently) exist, and went to Courses.xlsx and added BIOL222 with only 1 section, whose timeslot 
        is the exact same as that of BIOL196 and set the capacity to 1, so that I can test time overlap conflict for two different courses.
        Yet, still a complete solution was found, and both course requests were assigned to the respective sections (both of which occur at the same time) 
        - Solver took 0.25m (15.18s)
        - Complete solution found.
    - 210926_225901
        - Running the solver after fixing the Time overlaps conflicts bug that I discovered above
            - See 10.2 in this project's main Readme file (../Readme.md) for how I found where the bug occurred and how I fixed it. 
            - All previously obtained solutions above probably have Time overlap conflicts within them, and that they went unchecked, 
            and that the time taken are quite shorter than what they should have been. 
        - Solver took 5m (300s - the Maximal solver time (Termination.TimeOut's value); with the message that 'Timeout reached')
        - NO complete solution found (as expected) 
            - Best solution had 9 course requests unassigned (6166/6175 [99,85%] assigned) (8 more than I was expecting). 
            - From looking at the debug.log file, the initial solution (6166 requests assigned) is the best solution obtained (in terms of number of requests assigned).
            No other solution obtained more assigned requests (though many other solutions did also get 6166 assigned requests)
        - What the csv files say:
            - conflicts-real:
                - Course C16 (the unassigned course) has 8 students conflicting with C4 with the following reason: P16 W 9:35a - 12:35p  vs P4 W 9:35a - 12:35p
                    - 'P' stands for Subpart (i.e. a lab). It's used in the name of the subpart - 'name' attribute for a subpart 
                    is added in the solution.xml file. Since each course only has 1 lab in this problem instance, the subpart number
                    should match up with the course number
                    - Course C4 is BIOL196 and Course C16 is MATH196
                - Course C5 has 1 student conflicting with C4 for the same reason as C16. Course C5 is the BIOL222 course I added for testing.
            - time-conflicts-real
                - contains the class (lab section) of the unassigned course that is causing the conflict, as well as the meeting time
            - section-conflicts-real
                - contains more info than conflicts-real, including the course and class (lab section) enrolments (student course requests successfully assigned)
                and class limit for courses C16 and C5. 
            - tableau
                - Course requests of students with their assigned sections in a tabular format
                - Each row is a course request
                - If a course request was unassigned in the solution, its value for the "Enrolled" field will be "No",
                and the "Sections" field will be empty
        - There's also a time-overlaps-real.csv file (with no info) implying the solver makes a distinction between an actual time conflict and a time overlap
    - 210927_010236
        - Running the solver after undoing the changes that I made to the Courses.xlsx and Students.xlsx file to test the time 
        overlap conflict (i.e. removed the BIOL222 course and its course request for the student 218047643)
        - Solver took 5m (300s - the Maximal solver time (Termination.TimeOut's value); with the message that 'Timeout reached')
        - NO complete solution found (as expected) 
            - 8 unassigned course requests  (6166/6174 [99,87%] assigned)
            - Basically same as previous solution - 8 students of MATH196 (now course C15) conflicting with course C4
            
    - 2020-Sem1-CAES-Wvl-no-extra-requests-testing
            - Created this problem instance so that in ModifiedInputProcessing.py, I can test processModifiedStudentsData() 
            without having to wait for processCurrentSolution() to process the entire Students input (which takes long) 
                - I only kept the last 100 students from the initial Students.xlsx and removed the rest above. 

### Modified Students input files

#### 2020-Sem1-CAES-Wvl-no-extra-requests-testing
- Students-1.xlsx
    - Initialised to a copy of Students.xlsx
    - Made simple changes (1 for each case) to identify what the resulting modificationsDF in 
    ModifiedInputProcessing.processModifiedStudentsData() will look like
    - All modifications were made at the end of the file
    - Modifications:
        - Added student: 220120001 with 3 course requests.
        - Removed student: 220111511.
        - Modified student: 220112040. Removed course request for MGNT102.
        - Modified student: 220112256. Added course request for STAT130.
