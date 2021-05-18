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
    QuestionStatsPrivate = dict()
    QuestionStatsState = dict()
    AgeCt = dict()

    def __init__(self):
        self.data = create_dict(read_csv_file())
        self._create_nominaldata_keywords()
        self._show_nominal_datas()
        self._calculate_all_questions_stats()
        self._katilimci_yas_araligi_ve_sayisi()

        print("A produced Data dict:")
        print(self.data[0])
        print("-" * 40)

    def _create_nominaldata_keywords(self):
        for i in self.data:  #
            for key, value in zip(i.keys(), i.values()):
                if type(value) is str:
                    if not self.data_set_dict.get(key):
                        self.data_set_dict.update({key: set()})
                    self.data_set_dict[key].add(value)

    def _show_nominal_datas(self):
        print("-" * 40)
        print("String veri ayıraçları:")
        for i in self.data_set_dict:
            print("\t", i, "types:", self.data_set_dict[i])
        print("-" * 40)

    def _calculate_statistics(self, qusetion, schooltype="all"):
        datas = list()
        for i in self.data:
            if schooltype == "all":
                datas.append(i.get(qusetion.upper()))
            else:
                if i.get("School Type") == schooltype:
                    datas.append(i.get(qusetion.upper()))
                else:
                    pass

        return {"schooltype": schooltype,
                "mean": statistics.mean(datas),
                "mode": statistics.mode(datas),
                "stddev": statistics.stdev(datas),
                "variance": statistics.variance(datas),
                "median": statistics.median(datas),
                "harmonicmean": statistics.harmonic_mean(datas),
                "quantiles": statistics.quantiles(datas, n=4, method="inclusive")}

    def _katilimci_yas_araligi_ve_sayisi(self):
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

    def _calculate_all_questions_stats(self):
        for i in self.questions:
            self.QuestionStats.update({i: self._calculate_statistics(qusetion=i)})
            self.QuestionStatsPrivate.update({i: self._calculate_statistics(qusetion=i, schooltype="Private")})
            self.QuestionStatsState.update({i: self._calculate_statistics(qusetion=i, schooltype="State")})

    def print_calulated_datas(self):
        print("All statistics")
        for key, value in zip(self.QuestionStats.keys(), self.QuestionStats.values()):
            print(key, ": ", value)
        print("-" * 40)
        print("Statistics By school type")
        for i in analiseobj.QuestionStatsState:
            print(i, ": ", self.QuestionStatsState.get(i))
            print(i, ": ", self.QuestionStatsPrivate.get(i))
            print("*" * 10)
        print("-" * 40)
        print("Survey yaş aralığı dağılımı")
        print(self.AgeCt)
        print("-" * 40)


class Graping:
    StatistcsObj = AnalyseSurvey

    def __init__(self, Statistics):
        self.StatistcsObj = Statistics

    def drawagect(self):
        pyplot.bar(list(self.StatistcsObj.AgeCt.keys()), list(self.StatistcsObj.AgeCt.values()))
        pyplot.ylabel("Count")
        pyplot.xlabel("Age")
        pyplot.margins(y=0.1)
        pyplot.savefig("KatilimciYasSayisi.png")
        pyplot.close()

    def draw_questions_by_school_type(self):
        for i in self.StatistcsObj.QuestionStats:
            mean = [self.StatistcsObj.QuestionStatsPrivate[i]["mean"], self.StatistcsObj.QuestionStatsState[i]["mean"]]
            stddev = [self.StatistcsObj.QuestionStatsPrivate[i]["stddev"], self.StatistcsObj.QuestionStatsState[i]["stddev"]]
            pyplot.bar(["Private", "State"], mean)
            pyplot.ylabel("mean")
            pyplot.xlabel("SchoolType")
            pyplot.title(i)
            pyplot.margins(y=0.1)
            pyplot.savefig("mean"+i+"_devlet-vs-ozel.png")
            pyplot.close()
            pyplot.bar(["Private", "State"], stddev)
            pyplot.ylabel("StdDev")
            pyplot.xlabel("SchoolType")
            pyplot.title(i)
            pyplot.margins(y=0.1)
            pyplot.savefig("StdDev" + i + "_devlet-vs-ozel.png")
            pyplot.close()


if __name__ == "__main__":
    analiseobj = AnalyseSurvey()
    analiseobj.print_calulated_datas()
    graphobj = Graping(analiseobj)
    graphobj.drawagect()
    graphobj.draw_questions_by_school_type()


