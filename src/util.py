import csv
import random

CSV_DELIMITER=";"

# funcion to generate random data into file
def generate_random_data(filename, size):
    data = []

    for i in range(0,size):
        semester = random.randint(1,4)
        hour = random.randint(0,23)
        level = random.randint(1,5)
        data.append([semester, hour, level])
    create_csv(filename, data)



def get_data_from_file(filename):
    with open(filename, 'r') as csv_file:
        data = list(csv.reader(csv_file, delimiter=CSV_DELIMITER))
    return data


def create_csv(filename, data, header=None, parser=None):
    with open(filename, 'w') as csvFile:
        writer = csv.writer(csvFile, delimiter=CSV_DELIMITER)
        if parser != None:
            if header != None:
                writer.writerow(header)
            for index in range(len(data)):
                writer.writerow(parser(data[index], index))
        else:
            if header != None:
                data.prepend(header)
            writer.writerows(data)
