Each problem instance must be in its own folder (named appropriately: year-term-initiative) within the 'input' folder
and must contain the following files named as is: "Courses.xlsx", "Students.xlsx", and "Specification.xml"
<br>
<br>

###### CoursesInputTemplate.xlsx:
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

###### StudentsInputTemplate.xlsx:
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
 
###### Configuration File (for CPSolver)
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

###### Solutions explanations
##### 2020-Sem1-CAES-Wvl-OLD
- 210828_003504
    - First run. Didn't stop running (due to the high TimeOut value) so I terminated it. 
    
- 210902_105758
    - Configuration File change: changed Maximal solver time (Termination.TimeOut)  to 60 from 28800
    - solver took 1m
    - Complete solution found.
    
- 210903_204021
    - Configuration File change: changed Stop when a complete solution if found (Termination.StopWhenComplete) to true,
    and Termination.TimeOut to 300 (from 60)
    - solver took 0.21m (12.64s) [including trying to get a better solution on the initial complete solution]
    - Complete solution found.
    
- 210903_223248
    - Configuration File change: changed Anonymize XML file (no names) (Xml.ShowNames) to true
    - solver took 0.24m (14.66s)
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

##### 2020-Sem1-CAES-Wvl
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
        - solver took 0.12m (7.13s)
        - Complete solution found.
    - 210922_212224
        - solver took 0.07m (4.40s)
        - Complete solution found.
    - 210922_212403
        - solver took 0.15m (8.92s)
        - Complete solution found.