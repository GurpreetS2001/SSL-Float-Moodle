# SSL-Float-Moodle
## Course Project for CS251 Software Systems Lab 
Built by Dhvanit Beniwal (200050035), Gurpreet Singh Wadhwa (200050046), Molina Dhembla (200050076) and Yashvardhan (200050162).


This is an online learning management system built using Django's web framework based in Python with HTML/CSS, Bootstrap components and javascript used for the frontend. Includes application of Python libraries like matplotlib and numpy for generating graphs representing course statistics and prompt_toolkit for creating the command line interface.


To build the project, you must have all packages listed in requirements.txt installed in a python environment.
Command for the same:
> $ pip install -r requirements.txt

Once inside the python virtual environment, run the site like a typical Django project:
> $ source "path-to-v_env"/bin/activate 
  
> $ python3 manage.py runserver
  
*make sure you change the database credentials in moodle/settings.py to match your local pgadmin4-postgres setup*
  

### Some features we have implemented include:
* Basic signup and login, user authentication, option to reset password incase of 'forgot password'
  - the reset passowrd functionality **emails the user with a unique password update link**
  - the options to '**edit profile**' and '**change password'** once registered
* Creation of courses with separate **registration codes** for TAs and students
* Course creation notice with the registration code can be optionally sent to all users **via emails**
* **One user can view another's profile and the list of courses they take/teach**
* Instructor, teaching assistant and student roles in courses
* **Power of teaching assistants being set by the instructor**
    - Instructor can assign one or more of grading, assignment creation and lecture upload powers to TAs
* Course-specific **discussion forums** where users can post queries, reply to existing threads
* Instructors/TAs with the privilege can set a **deadline for assignments** created after which the submission link can't be accessed
* **New assignment created and successful submission are notified via email to concerned user**
* **Custom course weightage** can be set for assignments set by instructor
* **Direct messages** are supported among users, with an email notification for replies
* **Instructor having the power to disable discussion forums and direct messages for course members in event of an exam**
* **To-do lists** for all users (pending assignments/grading)
* Teachers/TAs with the required privilege can **download submissions** separately for each student or **all at once**
* **Feedbacks, marks upload** for submissions via **.csv files** and/or directly on the webpage
  - .csv format: (username,feedback,marks)  
  - the first row should be "userame,feedback,marks" and each subsequent row should contain data in the same format 
  - order of rows is irrelevant and non-existent usernames are ignored
  - the feedback can contain commas
* **Class performance statistics** (overall, assignment-wise and student-wise) for the teacher 
    - mean & variance in total marks displayed with illustrative graphs
    - represent variation in marks obtained and in terms of percent-weightage in course 
* **Grades and feedback** page accessible to students for assignment submissions in all registered courses
* Tracking and displaying **student progress** in terms of lectures 'marked as done' and assignments submitted
* Displaying **recently logged-in users** list on dashboard
* Elegant and suitable **error handling** to a reasonable extent via message-boxes and alerts
* Decent, responsive user interface implemented via HTML/CSS and bootstrap components
* **Built a command line interface 'moodle_cli'** 
  - can handle password-based login; assignment download; viewing marks, upcoming deadlines & course weightage for assignments; list of grading tasks left and a quit command
  - command to run the CLI: 
    > $ python3 manage.py moodle_cli



