from django.core.management.base import BaseCommand,CommandParser
from prompt_toolkit import prompt
from django.contrib.auth import authenticate
import sys
from pathlib import Path
base_dir=Path(__file__).resolve().parent.parent.parent
sys.path.insert(0,base_dir)
from userprofile.models import Assignments, Course, CourseUserRelation, Solutionfeedback, Solutions
from userprofile.aggregates import ToDoListStudent, ToDoListTeacher
import shutil
import os

class Command(BaseCommand):
    help = 'Lets Try This Out'

    def handle(self, *args, **options):
        user=None
        while user is None:
            username=prompt('>Username:')
            password=prompt('>Password:',is_password=True)
            user=authenticate(username=username,password=password)
            if not user:
                print("Incorrect UserName or Password.Try Again")
        while True:
            user_input=prompt('>Enter Command: ')
            if(user_input.capitalize()=="Quit"):
                break
            else:
                split=user_input.split(" ")
                if(split[0].capitalize()=="Deadlines"):
                    toDoList=ToDoListStudent(user)
                    for course in toDoList:
                        print(f"{course[0].name}: ")
                        for assignment in course[1]:
                            print(f"Name:{assignment.assignment_name}")
                            print(f"Deadline:{assignment.deadline}\n")
                        print("------------------")
                elif(split[0].capitalize()=="Marks"):
                    if len(split)==1:
                        courses=Course.objects.filter(user=user)
                        print("Select Courses:")
                        learner_courses=[]
                        for course in courses:
                            if CourseUserRelation.objects.filter(course=course).get(user=user).is_student:
                                print(f"{course.name}")
                                learner_courses.append(course)
                        print("------------")
                        course_name=prompt('>Enter Course Name: ')
                        try:
                            selected_course=Course.objects.filter(name=course_name).get(user=user)
                            if selected_course in learner_courses:
                                assignments=Assignments.objects.filter(course=selected_course)
                                for assignment in assignments:
                                    try:
                                        solution=Solutions.objects.filter(assignment=assignment).get(student=user)
                                        try:
                                            marks=Solutionfeedback.objects.get(solution=solution).marks_obtained
                                            print(f"{assignment.assignment_name}:{marks}/{assignment.max_marks}----Course Weightage:{assignment.course_weightage}")
                                        except Solutionfeedback.DoesNotExist:
                                            print(f"{assignment.assignment_name}:Not yet graded")
                                    except Solutions.DoesNotExist:
                                        print(f"{assignment.assignment_name}:Not Submitted Yet")
                            else:
                                print("Incorrect Course,Try Again")
                        except Course.DoesNotExist:
                            print("Incorrect Course,Try Again")
                    # else:
                    #     selected_course=split[1]
                    #     try:
                    #         courses=Course.objects.filter(user=user)
                    #         learner_courses=[]
                    #         for course in courses:
                    #             if CourseUserRelation.objects.filter(course=course).get(user=user).is_student:
                    #                 learner_courses.append(course)
                    #         if selected_course in learner_courses:
                    #             assignments=Assignments.objects.filter(course=selected_course)
                    #             for assignment in assignments:
                    #                 try:
                    #                     solution=Solutions.objects.filter(assignment=assignment).get(student=user)
                    #                     try:
                    #                         marks=Solutionfeedback.objects.get(solution=solution).marks_obtained
                    #                         print(f"{assignment.assignment_name}:{marks}/{assignment.max_marks}----Course Weightage:{assignment.course_weightage}")
                    #                         break
                    #                     except Solutionfeedback.DoesNotExist:
                    #                         print(f"{assignment.assignment_name}:Not yet graded")
                    #                 except Solutions.DoesNotExist:
                    #                     print(f"{assignment.assignment_name}:Not Submitted Yet")
                    #         else:
                    #             print("Incorrect Course Selected")
                    #             continue
                    #     except Course.DoesNotExist:
                    #         print("Incorrect Course Name")
                    #         continue
                elif(split[0].capitalize()=="Download"):
                    selected_course=None
                    courses=Course.objects.filter(user=user)
                    print("Select Course: ")
                    for course in courses:
                        print(f"{course.name}")
                    print("----------")
                    selected_course=prompt(">Enter Course Name: ")
                    try:
                        course=Course.objects.filter(name=selected_course).get(user=user)
                        assignments=Assignments.objects.filter(course=course)
                        for assignment in assignments:
                            print(f'{assignment.pk}:{assignment.assignment_name}')
                        print("-----------")
                        selected_assignment=prompt(">Enter Assignment Number: ")
                        try:
                            assignment=Assignments.objects.filter(course=course).get(pk=selected_assignment)
                            location=prompt(">Enter Download Path: ")
                            location=str(location)
                            download_location=os.path.join(location,f'{assignment.assignment_name}.pdf')
                            file_location=str(assignment.problemfile)
                            assignment_location=os.path.join(base_dir.parent,file_location)
                            try:
                                shutil.copy(assignment_location,download_location)
                                print("File Downloaded")
                            except shutil.SameFileError:
                                print("Source and Destination")
                            except PermissionError:
                                print("Permission Denied")
                            except:
                                print("Error occured while downloading file")
                        except Assignments.DoesNotExist:
                            print("No Such Assignment exists")
                    except Course.DoesNotExist:
                        print("No such course exists")
                elif(split[0].capitalize()=="Grading" and split[1].capitalize()=="Left"):
                    List=ToDoListTeacher(user)
                    if List[0]:
                        for courses in List[1]:
                            print(f"Course Name: {courses[0].name}")
                            for assignment in courses[1]:
                                print(f"Assignment Name: {assignment.assignment_name}")
                        print("-----------")
                    else:
                        print("Not a Teacher or a Grading TA")