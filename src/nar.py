import numpy as np

class NetworkAssociationRules:

    # 4 semester * 24 hours
    MATRIZ_ROWS = 96

    LEVELS_SIZE = 5

    def __init__(self, data):
        s = (self.MATRIZ_ROWS, self.LEVELS_SIZE)
        self.matrix = np.zeros(s)
        self.control = np.zeros(s)
        self.data = data
        self.result = np.zeros((self.MATRIZ_ROWS, 3))

    def convert_semester_hour_to_index(self, semester, hour):
        return (semester-1)*24 + (hour)

    def convert_index_to_semeter_hour(self, index):
        semester = int(index/24)+1
        hour = int(index%24)
        return (semester, hour)

    def sumarize_data(self):
        for row in self.data:
            semester = int(row[0])
            hour = int(row[1])
            level = int(row[2])
            pos = self.convert_semester_hour_to_index(semester, hour)

            self.matrix[pos][level-1] += 1
            for i in range(self.LEVELS_SIZE):
                if self.control[pos][i] == 0 or self.control[pos][i] == level:
                    self.control[pos][i] = level
                    break

    def add_result(self, pos, level, confidence, support):
        self.result[pos] = [level+1, confidence, support]


    def calculate_association_rules(self):
        count_all = len(self.data)
        self.sumarize_data()


        for item in range(0,self.MATRIZ_ROWS):
            count_sh = 0
            #count occurence of semester and hour pair
            for l in range(self.LEVELS_SIZE):
                count_sh += self.matrix[item][l]

            #has any occurence?
            if count_sh > 0:
                # iterate into each level position
                for l in range(self.LEVELS_SIZE):
                    # calculate confidence
                    conf = self.matrix[item][l] / count_sh
                    # calculate support
                    sup = self.matrix[item][l] / count_all

                    # verifi
                    if conf > self.result[item][1]:
                        self.add_result(item, l, conf, sup)
                    elif conf == self.result[item][1]:
                        if sup > self.result[item][2]:
                            self.add_result(item, l, conf, sup)
                        elif sup == self.result[item][2]:
                            for c_item in self.control[item]:
                                if c_item == l+1:
                                    self.add_result(item, l, conf, sup)
                                    break
                                elif c_item == self.result[item][0]:
                                    break
        return self.result

    def validate_association_rules(self, testData):
        errors = np.zeros(self.MATRIZ_ROWS)
        success = np.zeros(self.MATRIZ_ROWS)
        for row in testData:
            pos = self.convert_semester_hour_to_index(int(row[0]), int(row[1]))

            level = self.result[pos][0]
            #print("Proposition: LHS", row[0],",", row[1], " -> ", row[2], "Rule: ", level)
            if level == int(row[2]):
                #print("T")
                success[pos] +=1
            else:
                #print("F")
                errors[pos] +=1

        accuracy = np.zeros(self.MATRIZ_ROWS)

        for i in range(self.MATRIZ_ROWS):
            total = success[i]+errors[i]
            if total > 0:
                accuracy[i] = success[i] / total

        return accuracy
