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
    MaleFemaleCt = {"Male": 0, "Female": 0, "Other": 0}
    QuestionStatsMale = dict()
    QuestionStatsFemale = dict()
    QuestionStatsOther = dict()

    def __init__(self):
        self.data = create_dict(read_csv_file())
        self._create_nominaldata_keywords()
        self._show_nominal_datas()
        self._calculate_all_questions_stats()
        self._katilimci_yas_araligi_ve_sayisi()
        self._calculate_gender_ct()

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

    def _calculate_gender_ct(self):
        for i in self.data:
            if i["Gender"] == "Male":
                self.MaleFemaleCt["Male"] += 1
            elif i["Gender"] == "Female":
                self.MaleFemaleCt["Female"] += 1
            else:
                self.MaleFemaleCt["Other"] += 1

    def _calculate_statistics(self, qusetion, schooltype="all", gender="all", age="all"):
        datas = list()
        for i in self.data:
            if schooltype == "all" and gender == "all" and gender == "all":
                datas.append(i.get(qusetion.upper()))
            elif schooltype != "all":
                if i.get("School Type") == schooltype:
                    datas.append(i.get(qusetion.upper()))
                else:
                    pass
            elif gender != "all":
                if i["Gender"] == gender:
                    datas.append(i.get(qusetion.upper()))
                else:
                    pass
            else:
                continue

        return {"schooltype": schooltype,
                "gender": gender,
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
            self.QuestionStatsMale.update({i: self._calculate_statistics(qusetion=i, gender="Male")})
            self.QuestionStatsFemale.update({i: self._calculate_statistics(qusetion=i, gender="Female")})
            self.QuestionStatsOther.update(
                {i: self._calculate_statistics(qusetion=i, gender="I do not want to indicate")})

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
        print("Katılımcı Cinsiyet Profili")
        print(self.MaleFemaleCt)
        print("-" * 40)
        print("Statistics By Gender")
        for i in self.QuestionStats:
            print(i + "\n\t MALE:", self.QuestionStatsMale[i], "\n\t FAMALE:", self.QuestionStatsFemale[i],
                  "\n\t OTHER", self.QuestionStatsOther[i])
            print("*" * 10)


class Graping:
    StatistcsObj = AnalyseSurvey

    def __init__(self, Statistics):
        self.StatistcsObj = Statistics

    def drawagect(self):
        self.savedrawplot(x=list(self.StatistcsObj.AgeCt.keys()), y=list(self.StatistcsObj.AgeCt.values()),
                          xtitle="Age", ytitle="DataCount", gtitle="Count by Age",
                          fname="KatilimciYasSayisi.png")

    def savedrawplot(self, x, y, xtitle, ytitle, gtitle, fname): #barplt
        pyplot.bar(x, y)
        pyplot.ylabel(ytitle)
        pyplot.xlabel(xtitle)
        pyplot.title(gtitle)
        pyplot.margins(y=0.1)
        pyplot.savefig(fname)
        pyplot.close()
    def savehistogram(self,x,xtitle, gtitle, fname):
        pyplot.xticks(range(min(x),max(x)+1))
        pyplot.xlabel(xtitle)
        pyplot.ylabel("People Count")
        pyplot.title(gtitle)
        pyplot.hist(x,color="green")
        pyplot.savefig(fname)
        pyplot.close()

    def draw_questions_by_school_type(self):
        for i in self.StatistcsObj.QuestionStats:
            mean = [self.StatistcsObj.QuestionStatsPrivate[i]["mean"], self.StatistcsObj.QuestionStatsState[i]["mean"]]
            stddev = [self.StatistcsObj.QuestionStatsPrivate[i]["stddev"],
                      self.StatistcsObj.QuestionStatsState[i]["stddev"]]
            self.savedrawplot(x=["Private", "State"], y=mean,
                              xtitle="School Type", ytitle="mean", gtitle="mean-state-vs-private-schools->" + i,
                              fname="mean" + i + "_devlet-vs-ozel.png")
            self.savedrawplot(x=["Private", "State"], y=stddev,
                              xtitle="School Type", ytitle="StdDev", gtitle="StdDev-state-vs-private-schools->" + i,
                              fname="StdDev" + i + "_devlet-vs-ozel.png")

    def draw_gender_profiles_ct(self):
        self.savedrawplot(x=list(self.StatistcsObj.MaleFemaleCt.keys()),
                          y=list(self.StatistcsObj.MaleFemaleCt.values()),
                          xtitle="Gender", ytitle="DataCount", gtitle="GenderCount",
                          fname="KatilimciCinsisyetsayisi.png")

    def draw_questions_by_gender(self):
        for i in self.StatistcsObj.QuestionStats:
            mean = [self.StatistcsObj.QuestionStatsMale[i]["mean"],
                    self.StatistcsObj.QuestionStatsFemale[i]["mean"],
                    self.StatistcsObj.QuestionStatsOther[i]["mean"]]
            stddev = [self.StatistcsObj.QuestionStatsMale[i]["stddev"],
                      self.StatistcsObj.QuestionStatsFemale[i]["stddev"],
                      self.StatistcsObj.QuestionStatsOther[i]["stddev"]]
            self.savedrawplot(x=["Male", "Female", "Other"], y=mean,
                              xtitle="Gender", ytitle="mean", gtitle="mean_by_gender->" + i,
                              fname="mean" + i + "_by_gender.png")
            self.savedrawplot(x=["Male", "Female", "Other"], y=stddev,
                              xtitle="Gender", ytitle="stddev", gtitle="mean_by_gender->" + i,
                              fname="stdDev" + i + "_by_gender.png")
    def draw_qestions_histogram(self):
        questiondatas=list()
        for question in self.StatistcsObj.questions:
            for j in self.StatistcsObj.data:
                questiondatas.append(j[question])
            self.savehistogram(x=questiondatas,xtitle="Student Selection", gtitle=question+" Histogram", fname=question+"-histogram.png")
            questiondatas = []



if __name__ == "__main__":
    analiseobj = AnalyseSurvey()
    analiseobj.print_calulated_datas()
    graphobj = Graping(analiseobj)
    graphobj.drawagect()
    graphobj.draw_questions_by_school_type()
    graphobj.draw_gender_profiles_ct()
    graphobj.draw_questions_by_gender()
    graphobj.draw_qestions_histogram()