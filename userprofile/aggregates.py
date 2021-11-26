import numpy as np
from django.contrib.auth.models import User
from userprofile.models import Assignments, Course, CourseUserRelation, CsvFeedback, Lecture, LectureNotes, Solutions, Solutionfeedback,LectureCompleted
import matplotlib
import matplotlib.pyplot as plt
from pathlib import Path
import os
from matplotlib import colors


def CalculatePercentageCourseCompleted(student_courses,user):
    percentages_list=[]
    for course in student_courses:
        course_lectures=Lecture.objects.filter(course=course)
        total_lectures=len(course_lectures)
        completed_lectures_count=0
        for lecture in course_lectures:
            try:
                if LectureCompleted.objects.filter(lecture=lecture).get(user=user).lecture_completed:
                    completed_lectures_count+=1
            except LectureCompleted.DoesNotExist:
                continue
        course_assignments=Assignments.objects.filter(course=course)
        total_assignments=len(course_assignments)
        percentage_assignments_completed=0
        for assignment in course_assignments:
            try:
                solution=Solutions.objects.filter(assignment=assignment).get(student=user)
                percentage_assignments_completed+=1
            except Solutions.DoesNotExist:
                continue
        if total_lectures+total_assignments!=0:
            percentage_course_completed=(completed_lectures_count+percentage_assignments_completed)*100/(total_lectures+total_assignments)
        else:
            percentage_assignments_completed=0
        percentages_list.append([course,round(percentage_course_completed,2)])
    return percentages_list


def CalculateCourseMarksStudent(learner_course,user):
    course_assignments=Assignments.objects.filter(course=learner_course)
    student_assignmentwise_stats=[]
    total_marks=0
    percentage_score=0
    for assignment in course_assignments:
        try:
            solution=Solutions.objects.filter(assignment=assignment).get(student=user)
            try:
                marks=Solutionfeedback.objects.filter(solution=solution).marks_obtained
                student_assignmentwise_stats.append([assignment,marks,assignment.course_weightage*marks/assignment.max_marks])
                total_marks+=marks
                percentage_score+=assignment.course_weightage*marks/assignment.max_marks
            except Solutionfeedback.DoesNotExist:
                student_assignmentwise_stats.append([assignment,0.0,0.0])
        except Solutions.DoesNotExist:
            student_assignmentwise_stats.append([assignment,0.0,0.0])
    return student_assignmentwise_stats,total_marks,percentage_score


def GenerateTeacherStatsAssignment(course,assignment):
    assignment_marks=[]
    students=GetCourseLearners(course)
    for user in students:
        try:
            solution=Solutions.objects.filter(assignment=assignment).get(student=user)
            try:
                marks=Solutionfeedback.objects.filter(solution=solution).marks_obtained
                assignment_marks.append(marks)
            except Solutionfeedback.DoesNotExist:
                assignment_marks.append(0.0)
        except Solutions.DoesNotExist:
                assignment_marks.append(0.0)
    marks_array=np.array(assignment_marks)
    mean=marks_array.mean()
    variance=np.var(marks_array)
    base_dir=Path(__file__).resolve().parent.parent
    scatter_url=os.path.join(base_dir,f'/teacher_stats/scatterplots/{assignment.assignment_name}.png')
    hist_url=os.path.join(base_dir,f'/teacher_stats/histograms/{assignment.assignment_name}.png')
    plt.scatter(range(1,len(assignment_marks)+1),assignment_marks,c = "blue")
    plt.savefig(scatter_url)
    GenerateHistogram(marks_array,"Marks","Students",hist_url,None,assignment)
    return mean,variance,scatter_url,hist_url


def GenerateHistogram(array,x_label,y_label,url,course,assignment):
    fig,axs=plt.subplot(1,1,figsize=(10,7),tight_layout=True)
    for s in ['top','bottom','left','right']:
        axs.spines[s].set_visible(False)
    
    axs.xaxis.set_ticks_position('none')
    axs.yaxis.set_ticks_position('none')

    axs.xaxis.set_tick_params(pad=5)
    axs.yaxis.set_tick_params(pad=10)

    axs.grid(b=True,color='grey',linestyle="-.",linewidth=0.5,alpha=0.6)

    N,bins,patches=axs.hist(array,bins=20)

    fracs = ((N**(1/5))/N.max())
    norm = colors.Normalize(fracs.min(),fracs.max())

    for thisfrac,thispatch in zip(fracs,patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)
    
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    if assignment!=None:
        plt.title(f'Histogram for {assignment.assignment_name} Assignment')
    else:
        plt.title(f'Histogram for {course.title} Course')
    plt.savefig(url)


def GenerateTeacherStatsCourse(teacher_course):
    all_students=GetCourseLearners(teacher_course)
    total_score_list=[]
    percent_score_list=[]
    for student in all_students:
        assignment_stat,total_marks,percent_score=CalculateCourseMarksStudent(teacher_course,student)
        total_score_list.append(total_marks)
        percent_score_list.append(percent_score)
    base_dir=Path(__file__).resolve().parent.parent
    score_histogram_url=os.path.join(base_dir,f'/teacher_stats/histograms/{teacher_course.title}_score.png')
    percent_histogram_url=os.path.join(base_dir,f'/teacher_stats/histograms/{teacher_course.title}_percentage.png')
    GenerateHistogram(np.array(total_score_list),"Marks","Students",score_histogram_url,teacher_course,None)
    GenerateHistogram(np.array(percent_score_list),"Weighted Score","Students",percent_histogram_url,teacher_course,None)
    return all_students,total_score_list,percent_score_list,score_histogram_url,percent_histogram_url


def GetCourseLearners(teacher_course):
    all_registered_users=CourseUserRelation.objects.filter(course=teacher_course)
    student_users=[]
    for registered_user in all_registered_users:
        if registered_user.is_student:
            student_users.append(User.objects.get(pk=registered_user.user_id))
    return student_users

# def ToDoList(user):
