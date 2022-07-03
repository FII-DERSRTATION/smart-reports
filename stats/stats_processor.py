import json
from pprint import pprint

from disease.bapdbdoc import DISEAES, DISEASES_GERMAN
from disease.statsdoc import StatsDoc
from opensearch.AWSSearchDB import AWSSearchDB
# from utils.bucketutil import BucketUtil
from fuzzywuzzy import fuzz

STATS_KWDS = {
    'Glycemia': {
        'h': ['Diabetes mellitus', 'hyperglycemia in Cushing\'s syndrome', 'pancreatitis', 'craniocerebral trauma', 'general stressful situations'],
        'hh': ['Diabetes',  'Pancreatitis', 'Stress'],
        'l': ['Insulin overdose', 'insulinoma', 'hypoglycemia in congenital metabolic disorders', 'alcoholism'],
        'll': ['Insulinoma', 'Insulin overdose', 'Alcoholism']
    },
    'Cholesterol': {
        'h': ['primary and secondary dyslipidemia'],
        'hh': ['Dyslipidemia', 'Gout'],
        'l': ['Hyperthyroidism', 'anorexia', 'liver cirrhosis', 'severe trauma', 'recent myocardial infarction'],
        'll': ['Hyperthyroidism', 'Liver cirrhosis']
    },
    'Triglycerides': {
        'h': ['familial hypertriglyceridemia', 'diabetes mellitus', 'hyperchylomicronemia', 'secondary hypertriglyceridemia hepatopathie', 'obesity', 'chronic', 'alcoholism'],
        'hh': ['Dyslipidemia', 'Diabetes', 'Alcoholism', 'Hypothyroidism', 'renal Disease'],
        'l': ['not relevant'],
        'll': ['Malnutrition']
    },
    'Creatine': {
        'h': ['renal insufficiency', 'muscle lesions', 'burns', 'old age', 'medication', 'increased reference range for very muscular men'],
        'hh': ['Renal Disfunction'],
        'l': ['early phase of type 1 diabetes', 'pregnancy', 'anorexia'],
        'll': ['Hepatic Disease']
    },
    'Uric Acid': {
        'h': ['hyperuricemia', 'gout', 'tubular dysfunction', 'kidney stone disease', 'secondary hyperuricemia', 'Starvation', 'renal insufficiency', 'diuretics', 'diuretics'],
        'hh': ['Gout', 'Renal'],
        'l': [],
        'll': ['Hepatic Disease']
    },
    'Urea': {
        'h': ['acute renal failure', 'chronic renal failure', 'high protein intake', 'catabolic states '],
        'hh': ['Hepatic Disease'],
        'l': ['severe liver disease', 'lack of protein intake '],
        'll': ['Renal Insufficiency']
    },
    'TGO/AST': {
        'h': ['cell damage with leakage of a multilocular', 'hepatitis', 'fatty liver', 'cholestasis', 'cholangitis', 'Hepatocellular carcinoma'],
        'hh': ['Myocardial', 'Myocardia', 'Hepatic Disease'],
        'l': [],
        'll': []
    },
    'TGP/ALT': {
        'h': ['muscle necrosis', 'AST'],
        'hh': ['Pancreatitis', 'Hepatic Disease'],
        'l': [],
        'll': []
    },
    'Bilirubin Total': {
        'h': ['Hepatitis', 'liver cirrhosis', 'intra- and post-hepatic cholestasis', 'cholangitis', 'cholangitis', ],
        'hh': ['Biliary Disease'],
        'l': [],
        'll': []
    },
    'Bilirubin Id.': {
        'h': ['indirect bilirubin: hemolysis', 'Gilbert-Meulengracht disease'],
        'hh': ['Sepsis', 'Hemolysis'],
        'l': [],
        'll': []
    },
    'VSH (1 hour)': {
        'h': [],
        'hh': ['Infection', 'Inflammation'],
        'l': [],
        'll': ['Allergy', 'Anaphylaxis']
    },
    'VSH (2 hour)': {
        'h': [],
        'hh': ['Infection', 'Inflammation', 'Myeloma'],
        'l': [],
        'll': ['Anaphylaxis']
    },
    'Erythrocytes (RBC)': {
        'h': ['Polycythemia', 'dehydration', 'polycythemia vera'],
        'hh': [],
        'l': ['anemias', 'overhydration'],
        'll': ['Anemia', 'Hemorrhage', 'Internal']
    },
    'Leucocytes (WBC)': {
        'h': ['Infectious diseases', 'various forms of leukemia', 'infarcts', 'Smoking', 'stress', 'steroids'],
        'hh': ['Infection', 'Inflammation', 'Fever'],
        'l': ['Autoimmune diseases', 'tumors', 'bone marrow depression', 'viral infections', 'cytostatics', 'analgesics', 'thyrostatics'],
        'll': ['Fever', 'Bone Marrow Disease', 'Planectomy']
    },
    'Thrombocytes (PLT)': {
        'h': ['primary thrombocytosis', 'essential thrombocythemia', 'myeloproliferative disorders', 'secondary thrombocytosis', 'inflammations', 'infections', 'malignant tumors'],
        'hh': ['Infection'],
        'l': ['primary thrombocytopenia', 'idiopathic thrombocytopenic purpura (ITP)', 'secondary thrombocytopenia', 'collagenases', 'sarcoidosis drug-toxic thrombocytopenia', 'heparin-induced thrombocytopenia', 'diclofenac', 'gold', 'paracetamol', 'cotrimoxazole', 'hypersplenism', 'thrombocytopenia'],
        'll': ['Irradiation', 'Typhoid', 'Fever']
    },
    'Hemoglobin (Hb)': {
        'h': ['Polycythemia', 'dehydration', 'polycythemia vera'],
        'hh': ['Lise in spleen', 'Anaphylaxis'],
        'l': ['anemias', 'overhydration'],
        'll': []
    },
    'Hematocrits (HT)': {
        'h': ['Polycythemia', 'dehydration', 'stay at high altitude', 'blood doping'],
        'hh': [],
        'l': ['anemia', 'pseudo anemia with overhydration'],
        'll': []
    },
    'CRP': {
        'h': ['Acute', 'especially bacterial inflammation', 'necrosis', 'chronic inflammatory processes', 'postoperative', 'heart attack', 'tumors'],
        'hh': ['Infection', 'Tumor', 'postoperative State'],
        'l': [],
        'll': []
    },
    'D-Dimer': {
        'h': ['Leg vein thrombosis and pulmonary embolism', 'embolism', 'disseminated intravascular coagulation', 'monitoring of fibrinolytic therapies'],
        'hh': ['Thrombosis'],
        'l': [],
        'll': []
    },
    'TSH': {
        'hh': [],
        'h': ['primary hypothyroidism', 'iodine deficiency goiter', 'autoimmune thyroiditis with subsequent hypothyroidism'],
        'l': ['hyperthyroidism', 'autonomic adenoma', 'Graves disease', 'secondary hypothyroidism'],
        'll': []
    },
    'Glycated hemoglobin (HbA1, HbA1c)': {
        'h': ['Poorly controlled diabetes mellitus within the last 6–8 weeks'],
        'hh': [],
        'l': ['hemolytic anemia'],
        'll': []
    },
    'INR': {
        'h': ['by penicillin', 'barbiturates', 'anticoagulants'],
        'hh': [],
        'l': ['factor deficiency', 'vitamin K deficiency', 'consumption coagulopathy', 'liver dysfunction', 'anticoagulant therapy'],
        'll': []
    },
    'Lipase': {
        'h': ['acute and chronic pancreatitis', 'with acute upper abdominal pain', 'chronic alcoholism', 'renal failure'],
        'hh': [],
        'l': [],
        'll': []
    },
    'Sodium': {
        'h': ['Water loss without electrolyte loss, mostly extrarenal', 'diabetes insipidus', 'hyperglycemia without ketoacidosis', 'fever', 'Conn Syndrome'],
        'hh': [],
        'l': ['diuretics', 'salt-losing kidney', 'Addison\'s disease', 'syndrome of inappropriate ADH secretion', 'polydipsia', 'vomiting', 'Diarrhea', 'renal tubular acidosis'],
        'll': []
    },
    'Potassium': {
        'h': ['hemolysis at sample collection', 'Renal failure', 'acute tissue breakdown', 'Addison\'s disease', 'acute acidosis', 'ACE inhibitors', 'potassium-sparing diuretics'],
        'hh': [],
        'l': ['Diuretics', 'laxatives', 'vomiting', 'diarrhea', 'renal tubular acidosis', 'acute alkalosis', 'Conn\'s syndrome'],
        'll': []
    }
}


class StatsProcessor:

    def __init__(self, awsdb: AWSSearchDB):
        self.awsdb = awsdb
        self.stat_docs = []
        # self._fetch_stat_docs()

    def _fetch_stat_docs(self):
        raw_stats_doc = self.awsdb.query_stats_index()
        stat_docs_unprocessed = raw_stats_doc['hits']['hits']

        for stat_doc in stat_docs_unprocessed:
            self.stat_docs.append(StatsDoc(stat_doc))

        print("Ana maria")

    def process_stats_local_german(self):
        with open("/Users/danilamarius-cristian/PycharmProjects/pythonProject2/stats/data_german.json", "r") as f:
            stats_memory = json.loads(f.read())

        outliers_map = {}
        a = []

        for disease in DISEASES_GERMAN:
            print(disease)
            outliers_map[disease] = {}
            for stat_entry in stats_memory:
                a.append(stat_entry['diagnosis'])
                if stat_entry['diagnosis'] == disease:
                    for stat, value in stat_entry['stats'].items():
                        if value.lower() == 'l' or value.lower() == 'll':
                            if stat + 'l&ll' not in outliers_map[disease]:
                                outliers_map[disease][stat + 'l&ll'] = 1
                            else:
                                outliers_map[disease][stat + 'l&ll'] += 1
                        elif value.lower() == 'h' or value.lower() == 'hh':
                            if stat + 'h&hh' not in outliers_map[disease]:
                                outliers_map[disease][stat + 'h&hh'] = 1
                            else:
                                outliers_map[disease][stat + 'h&hh'] += 1

        print(outliers_map)
        print(set(a))

        outliers_map_sorted = {}

        for disease in outliers_map:
            outliers_map_sorted[disease] = {k: v for k, v in
                                            sorted(outliers_map[disease].items(), key=lambda item: item[1],
                                                   reverse=True)}

        pprint(outliers_map_sorted)

        return outliers_map_sorted

    def get_top_10_stats_german(self):
        """
            filter the map of stats per disease to only 10 stats  per disease (top 10 stats by occurences)
        """
        processed_stats = self.process_stats_local_german()

        top_10_stats = {}

        for disease in processed_stats:
            if disease not in top_10_stats:
                top_10_stats[disease] = {}

            top_10_vals = sorted(list(processed_stats[disease].values()))[-10:]

            for stat in processed_stats[disease]:
                if processed_stats[disease][stat] in top_10_vals:
                    top_10_stats[disease][stat] = processed_stats[disease][stat]
                    top_10_vals.remove(processed_stats[disease][stat])

                if len(top_10_vals) <= 0:
                    break

        return top_10_stats

    def process_stats(self):
        outliers_map = {}

        for disease, _ in DISEAES.items():

            outliers_map[disease] = {}

            for doc in self.stat_docs:
                if doc.diagnosis == disease:
                    print("disease match")
                    for stat, value in doc.stats.items():
                        print(stat, value)
                        if value.lower() == 'l' or value.lower() == 'll':
                            if stat + 'l&ll' not in outliers_map[disease]:
                                outliers_map[disease][stat + 'l&ll'] = 1
                            else:
                                outliers_map[disease][stat + 'l&ll'] += 1
                        elif value.lower() == 'h' or value.lower() == 'hh':
                            if stat + 'h&hh' not in outliers_map[disease]:
                                outliers_map[disease][stat + 'h&hh'] = 1
                            else:
                                outliers_map[disease][stat + 'h&hh'] += 1

        pprint(outliers_map)

    def preprocess_input_stats(self, input_stats):
        """
            select only relevant stats from the input (ie those that have have values in {l, ll, h, hh})
            and convert those stats to the format <stat-name1>l&ll or <stat-namek>h&hh. This is all done to
            ease the process of matching the relevant disease based on stats
        """

        processed_stats_list = []

        for stat in input_stats:
            if (input_stats[stat].lower() == 'l' or
                    input_stats[stat].lower() == 'll'):
                processed_stats_list.append(stat + 'l&ll')

            if (input_stats[stat].lower() == 'h' or
                    input_stats[stat].lower() == 'hh'):
                processed_stats_list.append(stat + 'h&hh')

        return processed_stats_list


    def predict_diseases_based_on_stats(self, input_stats):
        """
            given a set of lab results we need to predict the disease based on number of matching analysis maximum
            per disease.
        """
        top_10_stats_per_disease = self.get_top_10_stats_german()
        processed_input_stats = self.preprocess_input_stats(input_stats)

        disease_score = {}

        for disease in top_10_stats_per_disease:
            if disease not in disease_score:
                disease_score[disease] = 0

            for stat in top_10_stats_per_disease[disease]:
                if stat in processed_input_stats:
                    disease_score[disease] += 1

        max_score = sorted(disease_score.values())[-1]

        for d_score_key in disease_score:
            if disease_score[d_score_key] == max_score:
                return d_score_key

        # default returned disease
        return 'nstemr'

    def get_keywords(self, diagnostic, input_stats):


        kwds = []

        for stat in input_stats:
            if (input_stats[stat].lower() != 'l' and input_stats[stat].lower() != 'll'
                    and input_stats[stat].lower() != 'h' and input_stats[stat].lower() != 'hh'):
                continue

            from utils.bucketutil import BucketUtil
            matching_stat = BucketUtil.find_appropriate_stat(stat)

            if input_stats[stat].lower() == 'l':
                if len(STATS_KWDS[matching_stat]['l']) > 0:
                    kwds += STATS_KWDS[matching_stat]['l']
                else:
                    kwds += STATS_KWDS[matching_stat]['ll']

            if input_stats[stat].lower() == 'll':
                if len(STATS_KWDS[matching_stat]['ll']) > 0:
                    kwds += STATS_KWDS[matching_stat]['ll']
                else:
                    kwds += STATS_KWDS[matching_stat]['l']

            if input_stats[stat].lower() == 'h':
                if len(STATS_KWDS[matching_stat]['h']) > 0:
                    kwds += STATS_KWDS[matching_stat]['h']
                else:
                    kwds += STATS_KWDS[matching_stat]['hh']

            if input_stats[stat].lower() == 'hh':
                if len(STATS_KWDS[matching_stat]['hh']) > 0:
                    kwds += STATS_KWDS[matching_stat]['hh']
                else:
                    kwds += STATS_KWDS[matching_stat]['h']

        return kwds


    def find_appropriate_befunde_labor(self, db, input_stats, kwds):
        cursor = db.cursor()
        cursor.execute(
            "select befundeLabor, content from kis_reports.report_nf, kis_reports.report_lab where kis_reports.report_nf.befundeLabor != '' and kis_reports.report_nf.id_lab = kis_reports.report_lab.id_lab limit 5000")

        records = cursor.fetchall()

        stats_score = 0
        fuzzy_search_score = 0
        target_befunde_labor = ''

        for record in records:

            doc_stats = {}
            try:

                content_tuple = record[1].decode("UTF-8")

                content_raw = json.loads(content_tuple)

                for stat in content_raw.items():
                    try:
                        doc_stats[stat[1]['NAM']] = stat[1]['FLAG']
                    except Exception as e2:
                        print("Inner exception")
            except Exception as e:
                continue
                print(e)


            stat_count = 0
            for i_stat in input_stats:

                if i_stat in doc_stats:
                    stat_count += 1

            local_stat_score = stat_count / len(input_stats)
            local_fuzzy_score = fuzz.ratio(' '.join(kwds), record[0].decode("UTF-8"))

            if local_stat_score > stats_score and local_fuzzy_score > fuzzy_search_score:
                target_befunde_labor = record[0].decode("UTF-8")

        return target_befunde_labor


if __name__ == "__main__":

    """
                filter the map of stats per disease to only 10 stats  per disease (top 10 stats by occurences)
    """


    stats_processor = StatsProcessor(None)
    processed_stats = stats_processor.process_stats_local_german()

    top_10_stats = {}

    for disease in processed_stats:
        if disease not in top_10_stats:
            top_10_stats[disease] = 0

        top_10_vals = sorted(list(processed_stats[disease].values()))[-10:]

        for stat in processed_stats[disease]:
            if processed_stats[disease][stat] in top_10_vals:
                top_10_stats[disease] += processed_stats[disease][stat]
                top_10_vals.remove(processed_stats[disease][stat])

            if len(top_10_vals) <= 0:
                break

    print(top_10_stats)