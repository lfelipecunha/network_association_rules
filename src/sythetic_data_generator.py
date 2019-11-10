from datetime import datetime, timedelta
import random
import csv


def convert_datetime_to_semester_hour(date):
    month = date.month
    day = date.day
    hour = date.hour
    semester = 4
    if (month == 2 and day >= 25) or (month >= 3 and month <= 6) or (month == 7 and day <= 20):
        semester=1
    elif (month==7 and day > 20) or (month == 8 and day <= 5):
        semester = 2
    elif (month==8 and day > 5) or (month > 8 and month <= 11) or (month == 12 and day <= 20):
        semester = 3

    return (semester, hour)

def is_class_day(date):
    # @TODO add academic calendar
    return True

def get_factor_by_date(date):
    factor = 1.0
    month = date.month

    if month < 3:
        factor = 0.2
    elif month == 3:
        if date.day <= 10:
            factor = 0.75
        else:
            factor = 1.0
    elif month < 6:
        factor = 0.8
    elif month == 6:
        factor = 0.85
    elif month == 7:
        if date.day <= 15:
            factor = 0.9
        else:
            factor = 0.6
    elif month == 8:
        if date.day <= 10:
            factor = 0.65
        else:
            factor = 0.95
    elif month <= 11:
        factor = 0.75
    else:
        if date.day <= 15:
            factor = 0.85
        else:
            factor = 0.2
    return factor


def generate_data(filename, date, end_date):
    with open(filename, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        while(date <= end_date):
            students_min = 0.02
            students_max = 0.1
            if is_class_day(date):
                if date.weekday() < 5:
                    if date.hour >= 7 and date.hour < 9:
                        students_min = 0.05
                        students_max = 0.2
                    elif date.hour <= 11:
                        students_min = 0.1
                        students_max = 0.25
                    elif date.hour < 14:
                        students_min = 0.05
                        students_max = 0.2
                    elif date.hour < 18:
                        students_min = 0.1
                        students_max = 0.25
                    elif date.hour < 19:
                        students_min = 0.3
                        students_max = 0.6
                    elif date.hour < 23:
                        students_min = 0.5
                        students_max = 0.9
                    else:
                        students_min = 0.2
                        students_max = 0.5
                elif date.weekday() == 5:
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

generate_data('../data_base/trainning_data.csv', datetime(2012, 1, 1),datetime(2017, 12, 31, 23))
generate_data('../data_base/testing_data.csv', datetime(2011, 1, 1),datetime(2018, 12, 31, 23))
