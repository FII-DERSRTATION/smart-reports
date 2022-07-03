import ast
import json

from opensearch.AWSSearchDB import AWSSearchDB
from utils.bucketutil import BucketUtil


class StatsFetcher:

    def __init__(self, db, awsdb: AWSSearchDB):
        self.db_con = db
        # self._restart_es_con()

    def _restart_es_con(self):
        self.awsdb = AWSSearchDB()


    def fetch_stats_german(self):
        cursor = self.db_con.cursor()
        cursor.execute("select distinct kis_reports.report_lab.id_lab, kis_reports.report_lab.content, kis_reports.report_nf.diagnosen from kis_reports.report_lab, kis_reports.report_nf where kis_reports.report_lab.id_lab = kis_reports.report_nf.id_lab and kis_reports.report_nf.diagnosen != '' and kis_reports.report_lab.content like '%FLAG%'")
        records = cursor.fetchall()

        self.resp_list_german = []

        j = 0
        for record in records:
            try:
                diag = self._collect_diagnostics(record[2])

                content_tuple = record[1].decode("UTF-8")

                content_raw = json.loads(content_tuple)
                doc_stats = {}

                for stat in content_raw.items():
                    try:
                        doc_stats[stat[1]['NAM']] = stat[1]['FLAG']
                    except Exception as e2:
                        print("Inner exception")


                # print(BucketUtil.find_appropriate_disease(i['_source']['dignostic'][0]))

                resp = {
                    "diagnosis": BucketUtil.find_appropriate_disease_german(diag),
                    "stats": doc_stats
                }

                print(">>>>>>>>>>>> exported entry <<<<<<<<<<<<<<<<<<")
                print(resp)
                print(">>>>>>>>>>>> exported entry <<<<<<<<<<<<<<<<<<")
                self.resp_list_german.append(resp)

            except Exception as e:
                continue
                print("================ this is an error ==================")
                print(e)
                print("================ this is an error ==================")

            print(j)
            j += 1

        with open("/Users/danilamarius-cristian/PycharmProjects/pythonProject2/stats/data_german.json", "w") as f:
            json.dump(self.resp_list_german, f)


    def _collect_diagnostics(self, diagnostic_json):
        a = json.loads(diagnostic_json)

        diagnostic = []

        for e in a['Diagnosen']['Diagnosen']['List']:
            title = e['Titel']

            if "Inhalt" in e.keys():
                content = e['Inhalt']
                diagnostic.append(title)
            else:
                diagnostic.append(title)

        return diagnostic


    def fetch_stats(self):
        cursor = self.db_con.cursor()
        cursor.execute("select distinct id_lab, content, date from  kis_reports.report_lab where content like '%FLAG%' order by date desc")
        records = cursor.fetchall()

        f = open('/Users/danilamarius-cristian/PycharmProjects/pythonProject2/stats/raw_index.json')


        self.memmory_json = ast.literal_eval(f.read())
        f.close()

        self.resp_list = []

        j = 0
        for record in records:
            print(j)
            self._process_entry_local(record)
            j += 1


        print(self.resp_list)

        with open("/Users/danilamarius-cristian/PycharmProjects/pythonProject2/stats/data.json", "w") as f:
            json.dump(self.resp_list, f)


    def _process_entry_local(self, data):
        id_lab = data[0]
        content_tuple = data[1].decode("UTF-8")

        doc_stats = {}




        for i in self.memmory_json['hits']['hits']:
            if i['_source']['id_lab'] == id_lab:
                try:
                    content_raw = json.loads(content_tuple)

                    for stat in content_raw.items():
                        try:
                            doc_stats[stat[1]['NAM']] = stat[1]['FLAG']
                        except Exception as e2:
                            continue

                    # print(
                    #     BucketUtil.find_appropriate_disease(i['_source']['dignostic'][0]))

                    resp = {
                        "diagnosis": BucketUtil.find_appropriate_disease(i['_source']['dignostic'][0]),
                        "stats": doc_stats
                    }

                    print(">>>>>>>>>>>> exported entry <<<<<<<<<<<<<<<<<<")
                    print(resp)
                    print(">>>>>>>>>>>> exported entry <<<<<<<<<<<<<<<<<<")
                    self.resp_list.append(resp)

                except Exception as e:
                    print("================ this is an error ==================")
                    print(e)
                    print("================ this is an error ==================")







    def _process_entry(self, data):
        id_lab = data[0]
        content_tuple = data[1].decode("UTF-8")
        disease_doc = self.awsdb.find_disease_doc_by_id_lab(id_lab)

        doc_stats = {}

        # BucketUtil.find_appropriate_disease(disease_doc['hits']['hits'])
        if len(disease_doc['hits']['hits']) != 0:
            try:
                content_raw = json.loads(content_tuple)

                for stat in content_raw.items():
                    doc_stats[stat[1]['NAM']] = stat[1]['STAT']

                print(BucketUtil.find_appropriate_disease(disease_doc['hits']['hits'][0]['_source']['dignostic'][0]))

                resp = {
                    "diagnosis": BucketUtil.find_appropriate_disease(disease_doc['hits']['hits'][0]['_source']['dignostic'][0]),
                    "stats": doc_stats
                }

                print(">>>>>>>>>>>> exported entry <<<<<<<<<<<<<<<<<<")
                self.awsdb.add_stat(resp)

            except Exception as e:
                print(e)


