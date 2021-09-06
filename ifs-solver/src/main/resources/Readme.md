Each problem instance must be in its own folder (named appropriately: year-term-initiative) within the 'input' folder
and must contain the following files named as is: "Courses.xlsx", "Students.xlsx", and "Specification.xml"
<br>
<br>

###### CoursesInputTemplate.xlsx:
The venueCapacity field in my CoursesInputTemplate.xlsx doc matches with the
'limit' field of the 'section' tag/element in the CPSolver (See SSDataFormatTemplate.xml)

The sessionLength field in my CourseInputTemplate.xlsx doc matches with the
'length' field/attribute of the 'time' tag/element (which is a sub-tag/element of the 'section' tag/element)
 in the CPSolver (See SSDataFormatTemplate.xml). 
 - This represents the number
 of timeslots a session takes up. The default value is 1, and it should only
 be changed when the problem instance contains lab sessions of differing time durations.
    - The number of timeslots per day for the problem instances would've been modified accordingly
    such that 1 represents the shortest duration of a session.
    - The UKZN CAES problem has all lab sessions being of the same duration so it should
    not be affected by this (i.e. all sessionLength values will remain the default 1) 
    
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
        - all thus does (to the solution) is add the time of the session (as actual text in between the tags)
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
    - solver took 0.21m (12.64s)
    - Complete solution found.
- 210903_223248
    - Configuration File change: changed Anonymize XML file (no names) (Xml.ShowNames) to true
    - solver took 0.24m (14.66s)
    - Complete solution found.
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
    - Running solver after fixing previous NullPointerException error.
    - No complete solution found. 