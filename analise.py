import csv
from matplotlib import pyplot


def read_csv_file(filename="surveyresultspy.csv"):
    clean_data = list()
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            clean_data.append(row)
            if line_count == 0:
                line_count += 1
            else:
                del row[-3:]
                line_count += 1
        print(f'Processed {line_count} lines.')
        return clean_data


def create_dict(surveydata):
    anslist = list()
    temp = dict()
    for i in range(len(surveydata)):
        for j in range(len(surveydata[0])):
            try:
                temp.update({surveydata[0][j]: int(surveydata[i][j])})
            except ValueError:
                temp.update({surveydata[0][j]: surveydata[i][j]})

        anslist.insert(i, temp)
        temp = {}
    del anslist[0]
    return anslist


class AnalyseSurvey:
    data_set_dict = dict()

    def __init__(self):
        self.data = create_dict(read_csv_file())
        self.create_nominaldata_keywords()
        self.show_nominal_datas()
        print(self.data)

    def create_nominaldata_keywords(self):
        for i in self.data:  #
            for key, value in zip(i.keys(), i.values()):
                if type(value) is str:
                    if not self.data_set_dict.get(key):
                        self.data_set_dict.update({key: set()})
                    self.data_set_dict[key].add(value)

    def show_nominal_datas(self):
        print("-" * 40)
        print("String veri ayıraçları:")
        for i in self.data_set_dict:
            print("\t", i, "types:", self.data_set_dict[i])
        print("-" * 40)

    def calculate_mean(self, qusetion, gender="", schooltype="", educationlevel=""):
        sum = 0
        for i in self.data:
            sum += i.get(qusetion.upper())

        return sum / len(self.data)

    def katilimci_yas_araligi_ve_sayisi(self):
        # dict döndürür {yaş: bu yaştaki katılımcı sayısı}
        age_all = list()
        age_set = set()
        age_ct_dict = dict()
        for i in self.data:  # create age set
            age_set.add(i.get("Age"))
            age_all.append(i.get("Age"))
        for i in age_set:  # create age dict
            age_ct_dict.update({str(i): 0})
        for i in age_all:
            age_ct_dict[str(i)] += 1
        pyplot.bar(list(age_ct_dict.keys()), list(age_ct_dict.values()))
        pyplot.ylabel("Count")
        pyplot.xlabel("Age")
        pyplot.margins(y=0.1)
        pyplot.show()
        return age_ct_dict


if __name__ == "__main__":
    analiseobj = AnalyseSurvey()
    analiseobj.calculate_mean(qusetion="Q1")
    analiseobj.katilimci_yas_araligi_ve_sayisi()
