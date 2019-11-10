import csv
from datetime import datetime

def convert_timestamp_to_semester_hour(timestamp):
    date = datetime.fromtimestamp(float(timestamp))
    month = date.month
    hour = date.hour
    semester = 4
    if month >= 6 and month <= 9:
        semester=1
    elif month >= 10 or month <= 1:
        semester = 2
    elif month >= 3 and month <= 5:
        semester = 3

    return (semester, hour)

def convert_tshark_date_to_timestamp(date):
    date = date.split('.')[0]
    return datetime.strptime(date,'%b %d, %Y %H:%M:%S').timestamp()

results = []

#filename = '../data_base/combined.cap'
#delimiter = ' '

filename = '../data_base/TCP 80 University Napoli/data.csv'
delimiter = ';'

with open(filename, 'r') as cap_file:
    data = list(csv.reader(cap_file, delimiter=delimiter))

    sumarized_data = {}

    for row in data:
        date = datetime.fromtimestamp(convert_tshark_date_to_timestamp(row[0]))
        index = date.strftime('%Y-%m-%d %H')
        if not index in sumarized_data:
            sumarized_data[index] = []
        sumarized_data[index].append(row)

    new_data = []

    for i in sumarized_data:
        day_hour = sumarized_data[i]
        total = 0
        for row in day_hour:
            total += float(row[2])
        new_row = day_hour[0]
        new_row.append(0)
        new_row[3] = total / len(day_hour)

        new_data.append(new_row)

    max_load = 0
    min_load = 9999999999
    for row in new_data:
        load = row[3]
        if load > max_load:
            max_load = load
        if load < min_load:
            min_load = load

    step = (max_load - min_load)/4

    for row in new_data:
        sh = convert_timestamp_to_semester_hour(convert_tshark_date_to_timestamp(row[0]))
        load = float(row[3])
        load = load-min_load
        level = int(load / step)
        results.append([sh[0], sh[1],level+1])

data_size = len(results)
trainning = int(0.6 * data_size)


with open('../data_base/trainning_data.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter=";")
    for i in range(trainning):
        writer.writerow(results[i])

with open('../data_base/testing_data.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter=";")
    for i in range(trainning, data_size):
        writer.writerow(results[i])

