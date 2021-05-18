import csv
import statistics
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
    questions = ("Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10", "Q11")
    data_set_dict = dict()
    QuestionStats = dict()
    AgeCt = dict()

    def __init__(self):
        self.data = create_dict(read_csv_file())
        self.create_nominaldata_keywords()
        self.show_nominal_datas()
        self.calculate_all_questions_stats()

        print("A produced Data dict:")
        print(self.data[0])
        print("-" * 40)

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

    def calculate_statistics(self, qusetion):
        datas = list()
        for i in self.data:
            datas.append(i.get(qusetion.upper()))
        return {"mean": statistics.mean(datas),
                "mode": statistics.mode(datas),
                "stddev": statistics.stdev(datas),
                "variance": statistics.variance(datas),
                "median": statistics.median(datas),
                "harmonicmean": statistics.harmonic_mean(datas),
                "quantiles": statistics.quantiles(datas, n=4, method="inclusive")}

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
        self.AgeCt = age_ct_dict
        pyplot.bar(list(age_ct_dict.keys()), list(age_ct_dict.values()))
        pyplot.ylabel("Count")
        pyplot.xlabel("Age")
        pyplot.margins(y=0.1)
        pyplot.show()

    def calculate_all_questions_stats(self):
        for i in self.questions:
            self.QuestionStats.update({i: self.calculate_statistics(qusetion=i)})


if __name__ == "__main__":
    analiseobj = AnalyseSurvey()
    for key, value in zip(analiseobj.QuestionStats.keys(), analiseobj.QuestionStats.values()):
        print(key, ": ", value)
    print("-"*40)
    analiseobj.katilimci_yas_araligi_ve_sayisi()
    print(analiseobj.AgeCt)