# -*- coding: utf-8 -*-

import util
from nar import NetworkAssociationRules
import os

def parse_association_rule(row, index):
    row = association_rules[index]
    semester_hour = nar.convert_index_to_semeter_hour(index)
    return [semester_hour[0], semester_hour[1], row[0], row[1], row[2]]

def parse_accuracy(row, index):
    row = accuracy[index]
    rule = association_rules[index]
    semester_hour = nar.convert_index_to_semeter_hour(index)

    result = "T" if row >= rule[1] else "F"
    return [semester_hour[0], semester_hour[1], rule[0], rule[1], row,result]

#util.generate_random_data('data.csv', 80000)
base_path, filename = os.path.split(__file__)
if base_path == '':
    base_path = '.'
trainning_data = util.get_data_from_file(base_path + '/../data_base/trainning_data.csv')
print("Generating association rules...")
nar = NetworkAssociationRules(trainning_data)
association_rules = nar.calculate_association_rules()

# saving association_rules
print("Saving association rules into file...")
util.create_csv(base_path + "/../results/association_rules.csv", association_rules, ["Semester", "Hour", "level", "Conf", "Sup"], parse_association_rule)


#util.generate_random_data('test_data.csv', 20000)
test_data = util.get_data_from_file(base_path + '/../data_base/testing_data.csv')
print("Testing....")
accuracy = nar.validate_association_rules(test_data)

# saving accuracy
print("Saving test results...")
util.create_csv(base_path + "/../results/accuracy.csv", accuracy, ["Semester", "Hour", "level", "Conf[rule]", "Conf[test]", "Result"], parse_accuracy)

