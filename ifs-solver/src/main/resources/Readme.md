The venueCapacity field in my CourseInputTemplate.xlsx doc matches with the
'limit' field of the 'section' tag in the CPSolver (See SSDataFormatTemplate.xml)

The sessionLength field in my CourseInputTemplate.xlsx doc matches with the
'length' field of the 'time' tag (which is a subtag of the 'section' tag)
 in the CPSolver (See SSDataFormatTemplate.xml). 
 - This represents the number
 of timeslots a session takes up. The default value is 1, and it should only
 be changed when the problem instance contains lab sessions of differing time durations.
    - The number of timeslots per day for the problem instances would've been modified accordingly
    such that 1 represents the shortest duration of a session.
    - The UKZN CAES problem has all lab sessions being of the same duration so it should
    not be affected by this (i.e. all sessionLength values will remain the default 1) 
