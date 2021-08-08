CP Solver v1.3 build 232 change log (since the last release, build 219 on 23 Sep 2020 00:30)

Revision 45aa96e by tomas-muller <muller@unitime.org> (27-Nov-2020 12:38 PM)
  Student Scheduling: Critical Course Requests / Priority Students
    - added ability to boost the weight of critical course requests (StudentWeights.CriticalBoost)
      and priority students (StudentWeights.PriortyBoost)
    - base weight is multipled by the boost parameter
    - both parameters default to 1.0, no bost
    - this is to make sure priority students and/or critical courses are more important when
      comparing two solutions

Revision 4c8e38a by tomas-muller <muller@unitime.org> (25-Nov-2020 7:19 PM)
  Student Scheduling: Student Swap
    - take students in the order by their priority, only students with the same priority
    - when failed, put the student back to the queue after the students with the same priority

Revision 7f3b213 by tomas-muller <muller@unitime.org> (25-Nov-2020 7:18 PM)
  Student Scheduling: Enrollment Swap
    - take the unassigned requests in the order by their priority, only shuffle requests with the
      same priority
    - critical requests or priority student first (based on solver config)
    - request priority (higher priority first, substitute request last)
    - when failed, put the request at back to the queue after the requests with the same priority

Revision 57d1903 by tomas-muller <muller@unitime.org> (25-Nov-2020 7:12 PM)
  Student Scheduling: Backtracking
    - take the unassigned requests in the order by their priority, only shuffle requests with the
      same priority
    - critical requests or priority student first (based on solver config)
    - request priority (higher priority first, substitute request last)
    - when failed, put the request at back to the queue after the requests with the same priority

Revision e97bdd5 by tomas-muller <muller@unitime.org> (24-Nov-2020 6:40 PM)
  Student Scheduling: IFS
    - added ability to prohibit unassignment of a request of higher priority (than the request
      that is being assigned)
    when Neighbour.StandardCanHigherPriorityConflict is set to false (defaults to true)

Revision c2eef88 by tomas-muller <muller@unitime.org> (24-Nov-2020 6:39 PM)
  Student Scheduling: IFS
    - variable selection: skip unassigned free times when selecting variables

Revision aef7b66 by tomas-muller <muller@unitime.org> (22-Nov-2020 5:00 PM)
  Student Scheduling: Enrollment Swap
    - listen for failed neibhours, put the failed request back into the queue

Revision 961a4ae by tomas-muller <muller@unitime.org> (22-Nov-2020 4:59 PM)
  Student Scheduling: Student Swap
    - avoid cycling where the same student swap keeps on repeatedly failing (very rare, but not
      impossible)

Revision 42c0875 by tomas-muller <muller@unitime.org> (22-Nov-2020 4:59 PM)
  Student Scheduling: IFS
    - improved handing of concurrent modification errors

Revision 77a46cc by tomas-muller <muller@unitime.org> (20-Nov-2020 4:30 PM)
  Student Scheduling: IFS
    - added an ability to completely disable conflicting placements (no unassignments are allowed)
    - added an ability to disable conflicting placements at some point during the search (e.g.,
      two hours before solver's timeout)
    - added an ability to disable this neighbourhood at some point during the search (e.g., no IFS
      if less than an hour before solver's timeout)
    -> this is to allow the solver some time at the end of the search to optimize the solution
    without making steps that are hard to undo or resolve

Revision 061b087 by tomas-muller <muller@unitime.org> (20-Nov-2020 4:28 PM)
  Student Scheduling: Restore Best
    - added a simple step that checks whether the best solution has improved since the last check
    - if there is no improvement, restore the best solution (reset the search to start from the
      best solution again)
    - the checking is done in the seletion's initialization phase, no neighbors are actually
      computed

Revision a5df083 by tomas-muller <muller@unitime.org> (19-Nov-2020 8:57 PM)
  Student Scheduling: MPP
    - CourseRequest.isMPP() -- do not return true when the request has no initial assignment, but
      only some preferences (selected choices)
    - this is to avoid problems when initial assignments must be kept (e.g., branch&bound does not
      allow MPP request to be left unassigned)

Revision 62bfaa7 by tomas-muller <muller@unitime.org> (17-Nov-2020 9:02 AM)
  Student Scheduling: Required Sections / Configs
    - CourseRequest.isRequired(Section) -- corrected the config checking when there is a section
      required

Revision 12657a9 by tomas-muller <muller@unitime.org> (15-Nov-2020 1:16 PM)
  Student Scheduling: Concurrent Modification
    - improved handing of concurrent modification errors during backtracking (caused by a model
      change during the search)
    - retry computation of the neighbour selection up to five times rather than skipping to the
      next student/request

Revision 55c3eab by tomas-muller <muller@unitime.org> (15-Nov-2020 1:12 PM)
  Student Scheduling: Branch & Bound Selection
    - value ordering: always prefer enrollments that do not have a time conflict with a lower
      priority course which has only a few possible enrollments (five or less)
    - partial comparison of enrollments that are otherwise very close to each other was breking
      comparator transitivity in some cases
    - set OnlineStudentSectioning.TimesToAvoidHeuristics to false to swith of the time conflict
      checking

Revision 7290163 by tomas-muller <muller@unitime.org> (15-Nov-2020 1:09 PM)
  Student Scheduling: Critical IFS
    - can unassing: check student priority (do not allow unassignment of higher priority student)
    - can unassign: added ability to allow/disallow unassigment of a course request of the same or
      higher request priority (more critical)
    - by setting Neighbour.AllowCriticalUnassignment to true (defaults to false)

Revision c8d9df9 by tomas-muller <muller@unitime.org> (15-Nov-2020 1:04 PM)
  Student Scheduling: Request Bound
    - added ability to switched off the request bound adjustments implemented by commit 5d0b726
    - by setting StudentWeights.ImprovedBound to false (defaults to true)

Revision f555fa7 by tomas-muller <muller@unitime.org> (15-Nov-2020 12:59 PM)
  Student Scheduling: Failed Neighbour Assignment
    - backtrack and student swap now also listen for failed neibhours, putting the failed
      student/request back into the queue
    - improving success of each phase, especially when there are higher number of solver threads
    - also students are put at the beginning of the queue, ensuring that priority students are
      processed first

Revision 1639c6f by tomas-muller <muller@unitime.org> (13-Nov-2020 5:16 PM)
  Student Scheduling: XML Save/Load
    - include course id in the current/best/initial enrollment
    - this is to fix the case where a student is requesting multiple courses of a cross-listed
      course as alternatives to each other

Revision 4b8c09d by tomas-muller <muller@unitime.org> (13-Nov-2020 2:06 PM)
  Student Scheduling: Branch & Bound
    - when a neigbour (class schedule of a student) fails to be assigned, e.g., because the last
      spot in a class got taken:
    - put the student back at the beginning of the queue (instead of the end)
    - this is to ensure that student priority is beter considered (priority student does not get
      bumped at the end of the list)

Revision 5d0b726 by tomas-muller <muller@unitime.org> (12-Nov-2020 9:04 PM)
  Student Scheduling: Request Bound
    - improved computation of course request bound in an attempt to improve the branching
    - include penalization for arrange hours, online, selection and intitial placement if it
      cannot be avoided
    (e.g., when all enrollments are online)

Revision 0e491d2 by tomas-muller <muller@unitime.org> (11-Nov-2020 6:04 PM)
  Course Timetabling: Same Dates Group Constraint
    - added a new group constraint SAME_DATES
    - given classes must be taught on the same dates
    - if one of the classes meets more often, the class meeting less often can only meet on the
      dates when the other class is meeting
    - when prohibited or (strongly) discouraged: given classes cannot be taught on the same days
      (there cannot be a date when both classes are meeting)
    - note: unlike with the same days/weeks constraint, this constraint consider individual
      meeting dates of both classes

Revision 835f055 by tomas-muller <muller@unitime.org> (11-Nov-2020 5:34 PM)
  Student Scheduling: Branch & Bound Selection
    - value ordering: among enrollments that are otherwise very close to each other (in terms of
      their value), prefer those that do not have a time conflict with a lower priority course
      which has only a few possible enrollments (five or less)

Revision 6891ac1 by tomas-muller <muller@unitime.org> (6-Oct-2020 3:40 PM)
  Student Scheduling: Priority Students
    - student priority changed from being a boolean (priority yes/no) to have five layers of
      priority students
    - named Priority > Senior > Junior > Sophomore > Freshmen > Normal (no priority)
    - students of higher priority are assigned before students of lower priority
    - combined with course request priority depending on
      Sectioning.PriorityStudentsFirstSelection.AllIn
    - when true, student priority takes precedence Critical Priority > Non-Critical Priority >
      Critical Senior ...
    - when false, request priority takes precedence Critical Priority > Critical Senior > ... >
      Non-Critical Priority ...
