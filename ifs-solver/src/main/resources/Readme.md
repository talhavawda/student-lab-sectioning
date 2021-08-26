Each problem instance must be in its own folder (named appropriately: year-term-initiative) within the 'input' folder
and must contained the following files named as is: "Courses.xlsx", "Students.xlsx", and "Specification.xml"
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
 
