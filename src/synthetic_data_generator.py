from datetime import datetime, timedelta
import random
import csv
import os


def convert_datetime_to_semester_hour(date):
    month = date.month
    day = date.day
    hour = date.hour
    semester = 4
    if (month == 2 and day >= 25) or (month >= 3 and month <= 6) or (month == 7 and day <= 20):
        semester=1
    elif (month==7 and day > 20) or (month == 8 and day <= 5):
        semester = 3
    elif (month==8 and day > 5) or (month > 8 and month <= 11) or (month == 12 and day <= 20):
        semester = 2

    return (semester, hour)

def is_class_day(date):
    # @TODO add academic calendar
    return True

def get_factor_by_date(date):
    factor = 1.0
    month = date.month

    if month < 3: # initial months of year has only a few stutends
        factor = 0.2
    elif month == 3:
        if date.day <= 10: # in first days of semester students not all students become
            factor = 0.75
        else: # after a few days it has the maximum of stundents
            factor = 1.0
    elif month < 6: # the middle of semester students missing class
        factor = 0.8
    elif month == 6: # the final of semester students start to back
        factor = 0.85
    elif month == 7:
        if date.day <= 15: # the final days of semester the students has tests and increase the number of students
            factor = 0.9
        else: # the time between semesters decrease the amoung of students
            factor = 0.6
    elif month == 8:
        if date.day <= 10: # the time between semesters decrease the amoung of students
            factor = 0.6
        else:
            factor = 0.7 # the inital of second semester has no many students
    elif month <= 11: # the middle of second semester has less students than first semester
        factor = 0.75
    else:
        if date.day <= 15: # the final of second semester has tests so increase the number of students
            factor = 0.85
        else:
            factor = 0.2 # vacations
    return factor


def generate_data(filename, date, end_date):
    with open(filename, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=";")

        while(date <= end_date):
            students_min = 0.02
            students_max = 0.1
            if is_class_day(date):
                if date.weekday() < 5: # monday to friday
                    # in the mornings it has at least 25% of students
                    if date.hour >= 7 and date.hour < 9: # few students become before class
                        students_min = 0.05
                        students_max = 0.2
                    elif date.hour <= 11: # maximum of mornings
                        students_min = 0.1
                        students_max = 0.25
                    elif date.hour < 14: # lunch time, few students stay at university
                        students_min = 0.05
                        students_max = 0.15
                    # in the afternoons it has at least 25% of students
                    elif date.hour < 18:
                        students_min = 0.1
                        students_max = 0.25
                    # in the night the most part of students become
                    elif date.hour < 19: # few students become before night class
                        students_min = 0.3
                        students_max = 0.6
                    elif date.hour < 23: # the maximum number of students
                        students_min = 0.6
                        students_max = 1.0
                    else: # after class few students stay at university
                        students_min = 0.2
                        students_max = 0.5
                elif date.weekday() == 5: #saturday class is only mornings and has some extensions class
                    if date.hour >= 7 and date.hour < 9:
                        students_min = 0.1
                        students_max = 0.25
                    elif date.hour <= 11:
                        students_min = 0.2
                        students_max = 0.35

            students = random.uniform(students_min, students_max)
            factor = get_factor_by_date(date)
            level = int(students * factor * 5)+1
            sh = convert_datetime_to_semester_hour(date)
            date += timedelta(hours=1)
            writer.writerow([sh[0], sh[1], level])

base_path, filename = os.path.split(__file__)
generate_data(base_path + '/../data_base/trainning_data.csv', datetime(2013, 1, 1),datetime(2017, 12, 31, 23))
generate_data(base_path + '/../data_base/testing_data.csv', datetime(2018, 1, 1),datetime(2018, 12, 31, 23))
