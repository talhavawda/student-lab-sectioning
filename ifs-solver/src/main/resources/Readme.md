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
all the solutions obtained (sibling [independent/parallel] solutions to each other) on the current input data XML file of this 
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

Configuration File for resolving
- I've created a separate solver config file ("SolverConfiguration-resolving.cfg") for the resolving part as I want the 
Termination condition to be MPPTerminationCondition, so that the number of existing course requests that get their allocated 
sections changed is minimised.
    - Initialised it to SolverConfiguration.cfg, changed Termination.Class to MPPTerminationCondition, and added 
    Termination.MinPerturbances attribute and set the value to 0 -> ideally we don't want any changes to be made to existing
    variables (course requests), and the solver will focus on minimising the number of perturbances
- However the solver is still not minimising the number of perturbances
    - See 11. in ../Readme.md - "Trying to fix perturbations problem" - for more details on changes I played around with in the config
    file to try and remove perturbations
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
            - See 10. in this project's main Readme file (../Readme.md) for how I found where the bug occurred and how I fixed it. 
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
        - There's also a time-overlaps-real.csv file (with no info) implying the solver makes a distinction between an actual time conflict, and a time overlap
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
                    - Thus there is no Time overlaps conflicts, as was the case in this problem instance's parent
            - modified Students file:
                - Students-1.xlsx; initialised to a copy of Students.xlsx
                    - Made simple changes (1 for each case) to identify what the resulting modificationsDF in 
                    ModifiedInputProcessing.processModifiedStudentsData() will look like
                    - All modifications were made at the end of the file
                    - Modifications:
                        - Removed student: 220111511. (Had 1 processed course request for MATH134)
                        - Modified student: 220112040. Removed course request for MATH134. Added course request for STAT130. 
                        - Modified student: 220112256. Added course request for STAT130.
                        - Added student: 220120001 with 3 processed course requests.
                                
- 2020-Sem1-CAES-Wvl-no-conflicts
        - This modified problem instance removes the Time Overlap conflicts in its parent instance (2020-Sem1-CAES-Wvl-no-extra-requests)
        allowing us to get a complete initial solution
            - Removed the 8 course requests for MATH196 from those 8 students who also do BIOL196. [Discovered this conflict in solution 210926_225901]
                - Students: 219009466, 219013287, 219018827, 219021664, 219027743, 219030037, 219033547, 218000612
                
    - 211011_011710
        - Initial complete solution that I shall be working with for the Minimal Perturbation Experimentation process
        
    - 2020-Sem1-CAES-Wvl-no-conflicts-no-STAT130
        - This modified problem instance removes the course STAT130 from the courses input file so that (course requests for) 
        it is not processed
            - This is being done for the Minimal Perturbation Experimentation process to see if there are no perturbations
            if STAT130 is removed, as STAT130 results in (most/all depending on modification Scenario) perturbations, even 
            if none of the student modifications involve STAT130
        
        
### Dataset explanations        
        
 
### Modified Students input files

#### 2020-Sem1-CAES-Wvl-no-extra-requests-testing
- Students-1.xlsx
    - Initialised to a copy of Students.xlsx
    - Made simple changes (1 for each case) to identify what the resulting modificationsDF in 
    ModifiedInputProcessing.processModifiedStudentsData() will look like
    - All modifications were made at the end of the file
    - Modifications:
        - Removed student: 220111511. (Had 1 processed course request for MATH134)
        - Modified student: 220112040. Removed course request for MATH134. Added course request for STAT130. 
        - Modified student: 220112256. Added course request for STAT130.
        - Added student: 220120001 with 3 processed course requests.


### Minimal Perturbation Experimentation process
- Simulating students making changes to their registrations
- Each updated/modified Students file (Students-1.xlsx) is initialised to a copy of Students.xlsx file and the modifications 
then made. New students are added at the end of the file.

#### 2020-Sem1-CAES-Wvl-no-conflicts
 - Initial (complete) solution: 211011_011710
    - 6166/6166 [100%] course requests assigned
    - Solver took 0.08m (4.67s)
    - Complete solution found
      
 - Initial num students: 2547
 - Initial num course requests: 6166

##### Scenario 1
- Student modifications:
        - same as for 2020-Sem1-CAES-Wvl-no-extra-requests-testing instance. I want to test the updated solution out.
    - Removed student: 220111511. (Had 1 processed course request for MATH134)
    - Modified student: 220112040. Removed course request for MATH134. Added course request for STAT130. 
    - Modified student: 220112256. Added course request for STAT130.
    - Added student: 220120001 with 3 processed course requests (COMP100, MATH130, STAT130).
    
- Updated num students: 2547
- Updated num course requests: 6169

- Num assigned course requests (pre-resolving): 6164 (99.92%)
    - Get this num from the updated solution's debug.log file. Can also calculate it: Initial num course requests - num removed course requests
- Num students with complete schedule: 2544 (99.88%)

- Updated solution: 211012_223043
    - 6169/6169 [100%] course requests assigned
    - Solver took 0.03m (1.95s)
    - Complete solution found
    - There are a number of section allocation changes to existing course requests
        - Affected courses and sections:
                - Data obtained by comparing the initial solution.xml file to this updated solution.xml file in IntelliJ
                and looking at the differences
            - Course C19 (STAT130)
                - Allocation change from Section S42 to S43 occurred 23 times
                - Allocation change from Section S43 to S42 occurred 3 times
            - Course C7 (CHEM196)
                - Allocation change from Section S17 to S19 occurred 6 times
                - Allocation change from Section S18 to S19 occurred 1 times
                - Allocation change from Section S17 to S18 occurred 5 times
            - Course C1 (BIOL101)
                - Allocation change from Section S1 to S4 occurred 1 times
            - Course C8 (COMP100)
                - Allocation change from Section S21 to S20 occurred 2 times
                - Allocation change from Section S20 to S21 occurred 2 times
            - Course C11 (MATH130)
                - Allocation change from Section S26 to S27 occurred 3 times     
            - Course C17 (PHYS131)
                - Allocation change from Section S39 to S37 occurred 2 times
                    - One of this was for student 220112256, who had 1 added course request, for STAT130
                - Allocation change from Section S38 to S37 occurred 1 times
            - Course C14 (MATH150)
                - Allocation change from Section S33 to S32 occurred 2 times
                
        - Looking at STAT130 since it had the most number of changes:
            - In the Students.xlsx input file, there is 520 course requests for STAT130
            - In the Courses.xlsx input file, there is 2 sections for the STAT130 lab. In the input data XML file they because 
            S42 and S43 with capacities being 491 and 544 respectively.
            - In this intital solution [211011_011710] (from looking at the tableau.csv file), 268 students were allocated to S42 and 
            252 students were allocated to S43
            - In  the updated Student's input, there were 3 added course requests for STAT130, and in the updated solution, 
            S43 was allocated to all of them. Thus with the allocation changes above, for the updated solution: 
            248 students were allocated to S42 and 275 students were allocated to S43 (the tableau.csv file of the updated solution confirms this)
            - So it seems that all these allocation changes made to STAT130 is unnecessary as there was enough available space
            in both sections of the lab to fit in the 3 new course requests.
            
        - Looking at the other courses:
            - CHEM196
                - 148 course requests
                - Sections S16, S17, S18, S19, each with a capacity of 48
                - Initial Solution: students allocated were 37, 48, 33, 30 respectively 
            - BIOL101
                - 600 course requests
                - Sections S1, S2, S3, S4, each with a capacity of 200
                - Initial Solution: students allocated were 151, 150, 150, 149 respectively 
            - COMP100
                - 242 course requests
                - Sections S20, S21, each with a capacity of 250
                - Initial Solution: students allocated were 121 and 121 respectively
                - Updated Student's input: 1 added course request, allocated to S20 in updated Solution
            - MATH130
                - 255 course requests
                - Sections S26, S27, with capacities being 154 and 136 respectively
                - Initial Solution: students allocated were 139 and 116 respectively
                - Updated Student's input: 1 added course request, allocated to S27 in updated Solution
            - PHYS131
                - 609 course requests
                - Sections S37, S38, S39, S40, with capacities being 270, 320, 320, and 320 respectively
                - Initial Solution: students allocated were 133, 159, 159, 158 respectively 
            - MATH150
                - 724 course requests
                - Sections S32, S33, S34, with capacities being 491, 350, and 491 and respectively
                - Initial Solution: students allocated were 256, 202, 266 respectively 
        
        - student 220112256:
            - CR allocations in initial solution: C17 (PHYS131) -> S39 (Wed 09:35); C2 (BIOL103) -> S5 (Fri 14:10); C14 (MATH150) -> S32 (Tues 14:10)
            - In updated solution, C17 allocation changed from S39 (Wed 09:35) to S37 (Mon 14:10), and the new course request for
            course C19 (STAT130) was allocated to S43 (Wed 09:35). 
            **BUT** why didn't the allocation be to the other STAT130 section - S42 (Mon 14:10)? 
            AS this student had no conflict with that timeslot (but had a conflict with this Wed 09:35 timeslot with PHYS131), 
            and then the allocation for PHYS131 wouldn't have needed to change. 
               
        - **So based on the above, there were no actual availability conflicts or time overlap conflicts, so none of these 
        section allocation changes above should have occurred**, based on the 5 new course requests from the updated Students 
        input
                
                                                                          
- Updated solution: 211013_115521
        - Obtained this solution after creating a solver config file for the resolving part and setting Termination.Class 
        to MPPTerminationCondition, and added Termination.MinPerturbances attribute and set the value to 0
    - 6169/6169 [100%] course requests assigned
    - Solver took 0.02m (1.01s)
    - Complete solution found
    - There are still section allocation changes to existing course requests that have occurred, although slightly less than
    that of the previous updated solution above.
        - Affected courses and sections:
                - Data obtained by comparing the initial solution.xml file to this updated solution.xml file in IntelliJ
                and looking at the differences
            - Course C19 (STAT130)
                - Allocation change from Section S42 to S43 occurred 20 times
            - Course C7 (CHEM196)
                - Allocation change from Section S17 to S19 occurred 7 times
                - Allocation change from Section S17 to S18 occurred 5 times
                - Allocation change from Section S18 to S17 occurred 1 times
            - Course C1 (BIOL101)
                - Allocation change from Section S1 to S4 occurred 1 times
            - Course C8 (COMP100)
                - Allocation change from Section S21 to S20 occurred 1 times
            - Course C11 (MATH130)
                - Allocation change from Section S26 to S27 occurred 3 times     
            - Course C17 (PHYS131)
                - Allocation change from Section S39 to S37 occurred 1 times
                    - This was for student 220112256, who had 1 added course request, for STAT130

                
        - Allocations of new student (220120001): COMP100: S20, MATH130: S27, STAT130: S43. The other 2 added course requests (for the students
         who were modified) for STAT130 was also S43

 
##### Scenario 2
- Student modifications:
    - similar to Scenario 1, just removing the added STAT130 course request from the student 220112256

- Updated num students: 2547
- Updated num course requests: 6168

- Num assigned course requests (pre-resolving): 6164 (99.94%)
    - Get this num from the updated solution's debug.log file. Can also calculate it: Initial num course requests - num removed course requests
- Num students with complete schedule: 2545 (99.92%)

- Updated solution: 211014_132146
    - 6168/6168 [100%] course requests assigned
    - Solver took 0.03m (1.55s)
    - Complete solution found
    - There are still section allocation changes to existing course requests that have occurred, although much less than that of
    Scenario 1, and they only affect C19 (STAT130)
        - Affected courses and sections:
                - Data obtained by comparing the initial solution.xml file to this updated solution.xml file in IntelliJ
                and looking at the differences
            - Course C19 (STAT130)
                - Allocation change from Section S42 to S43 occurred 18 times
                
##### Scenario 3
- Student modifications:
        - similar to Scenario 1, removing STAT130 course requests as most perturbations are from STAT130 course requests
    - Removed student: 220111511. (Had 1 processed course request for MATH134)
    - Modified student: 220112040. Removed course request for MATH134. Added course request for COMP100.
    - Added student: 220120001 with 2 processed course requests (COMP100, MATH130).
    
    
- Updated num students: 2547
- Updated num course requests: 6167

- Num assigned course requests (pre-resolving): 6164 (99,95%)
- Num students with complete schedule: 2545 (99.92%)

- Updated solutions (See Exp-S3 folder) 
    - Still getting perturbations
        - There's no STAT130 course requests additions/deletions in the student modifications but all the perturbations are
        for STAT130 course requests
        
        
##### Trying out a new initial solution
- Trying out a new initial solution since the previous one (211011_011710) results in perturbations for the STAT130 course even
though there are no student modifications involving STAT130 (in Scenario 3)

- Testing on Scenario 3

- Updated solutions - See Exp-S3-NIS folder (solutions obtained after also changing some parameter values in the solver config resolving file)
- There's still the same number of perturbations in the updated solutions I've obtained

- Initial (complete) solution: 211018_210933
    - Data from Courses and Students input files:
        - There's 520 course requests for STAT130
        - There's 2 STAT130 Lab Sections: S42 and S43, with capacities being 491 and 544 respectively
            - In this intital solution (from looking at the tableau.csv file), 270 students were allocated to S42 and 
            250 students were allocated to S43
                - So it seems that there is a section allocation disbalance with STAT130: S42 is assigned more students that
                S42, even though S43 has a higher capacity. S42 is 54.99% filled, whilst S43 is 45.96% filled. 
                    - This disbalance also occurs in the first initial solution I obtained above (211011_011710).
                    - **It seems that all the updated solutions (resolving on updated input) are trying to fix this section 
                    allocation disbalance for STAT130.** 
                    
##### Trying out another (third) new initial solution
- In the SolverConfiguration.cfg file (for the initial solution, although this Weights applies to the config file for the updated solution), 
the StudentWeights.Class is set to PriorityStudentWeights. I want to get an initial solution with EqualStudentWeights to see if 
this fixes the section allocation disbalance of STAT130
    - Even though I've set the course request priorities to be the same (priority="0") when generating the initial input data XML file, 
    it seems that the solver is setting its own priorities [in descending order] (first course request of student has priority=1 -> highest priority, 
    and last course request of student has lowest priority) - see request-priorities.csv in a solution folder - as the StudentWeightsClass 
    is set to PriorityStudentWeights.
    
- Initial (complete) solution: 211019_000822
    - still having the STAT130 section allocation disbalance
    
- Updated solution (See Exp-S3-NIS2 folder) still has the STAT130 perturbations


#### 2020-Sem1-CAES-Wvl-no-conflicts-no-STAT130
 - Initial (complete) solution: 211026_023305
    - 5646/5646 [100%] course requests assigned
    - Solver took 0.09m (5.70s)
    - Complete solution found
      
 - Initial num students: 2547
 - Initial num course requests: 5646

##### Scenario 1
- Student modifications:
        - same as Scenario 3 of 2020-Sem1-CAES-Wvl-no-conflicts
    - Removed student: 220111511. (Had 1 processed course request for MATH134)
    - Modified student: 220112040. Removed course request for MATH134. Added course request for COMP100.
    - Added student: 220120001 with 2 processed course requests (COMP100, MATH130).

- Num assigned course requests (pre-resolving): 5644 (99.95%)
- Num students with complete schedule: 2387 (93.72%)

- Updated solution: 211026_144654
    - 5647/5647 [100%] course requests assigned
    - Solver took 0.05m (2.82s)
    - Complete solution found
    - There are NO section allocation changes to existing course requests (i.e. no perturbations)
        - Compared the initial solution.xml file to this updated solution.xml file in IntelliJ and looking at the differences


    
- Created SeparateModifiedInputProcessing.py to solve the perturbations issue (not get any perturbations in the updated solution - no existing 
course requests get their section allocations changed), and testing on 2020-Sem1-CAES-Wvl-no-conflicts problem instance,
on its Scenario 1:

#### 2020-Sem1-CAES-Wvl-no-conflicts [SMIP.py]
 - Initial (complete) solution: 211011_011710
- See 2020-Sem1-CAES-Wvl-no-conflict above for details
 
 ##### Scenario 1
 - See 2020-Sem1-CAES-Wvl-no-conflicts -> Scenario 1 above for student modifications and other details
 
 - Solving using SeparateModifiedInputProcessing.py (to not get any perturbations)
         - 'Updated solution''s solution.xml file is now only the solution for the new course requests
     - Updated solution: 211031_111738 
         - 5/5 [100%] course requests assigned
         - Solver took 0.01m (0.38s)
         - Complete solution found
         
     - Was able to merge the allocations of the new course requests into the current solution and get a full updated solution
     
     - See Scenario 1 - SMIP folder in the Experimentation folder of this problem instance