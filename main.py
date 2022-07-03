import ast
import json
from pprint import pprint

from db.connector import connect_to_kis_db, connect_to_kis_db_no_config_file
from disease.bapdbdoc import BapdbDoc
from opensearch.AWSSearchDB import AWSSearchDB, DISEASE_INDEX
from stats.stats_fetch import StatsFetcher
from stats.stats_processor import StatsProcessor
from utils.bucketutil import BucketUtil
from utils.doc_util import DocUtil



def process_core():
    # db = AWSSearchDB()
    #
    # # db.create_disease_index('')
    #
    # docs = db.query_bapdb_index()


    f = open('/Users/danilamarius-cristian/PycharmProjects/pythonProject2/raw_index.json.bkp')

    # returns JSON object as
    # a dictionary
    data = ast.literal_eval(f.read())
    f.close()


    pprint(data['hits']['hits'])

    managed_docs =[]
    for doc in data['hits']['hits']:
        bapdb_doc = BapdbDoc(doc)
        # managed_docs.append(BapdbDoc(doc))
        # print(100 * "=")
        # print(managed_docs.complete_doc_corpus)
        # print(100 * "=")
        probabilistic_disease = BucketUtil.find_appropriate_disease(bapdb_doc.get_doc_corpus().diagnostic)

        print(20 * "=")
        print(bapdb_doc.get_doc_corpus().diagnostic)
        print(probabilistic_disease)
        print(20 * "=")

        # if probabilistic_disease != 'NOT-SPECIFIED':
        #     disease_doc_str = DocUtil.build_update_doc_str(bapdb_doc.get_doc_corpus(), db, probabilistic_disease)
        #     db.update_disease_doc(DISEASE_INDEX[probabilistic_disease], disease_doc_str)


    # for md in managed_docs:
    #     print(100 * '+')
    #     key = BucketUtil.find_appropriate_disease(md.get_doc_corpus().diagnostic)
    #     if key == '':
    #         print("<<actually empty key>>")
    #     else:
    #         print(key)
    #     print(100 * '+')

def fetch_stats():
    # awsdb = AWSSearchDB()
    db = connect_to_kis_db_no_config_file()

    stats_fetcher = StatsFetcher(db, None)
    stats_fetcher.fetch_stats_german()


def process_stats():
    stats_processor = StatsProcessor(None)
    # stats_processor.process_stats_local_german()
    pprint(stats_processor.get_top_10_stats_german())



def process_keywords_json():
    f = open('/Users/danilamarius-cristian/PycharmProjects/pythonProject2/raw_index.json.bkp')

    # returns JSON object as
    # a dictionary
    data = ast.literal_eval(f.read())
    f.close()

    f = open('/Users/danilamarius-cristian/PycharmProjects/pythonProject2/kwds.json')
    kwds_json = ast.literal_eval(f.read())
    f.close()



    pprint(data['hits']['hits'])

    managed_docs =[]
    for doc in data['hits']['hits']:
        bapdb_doc = BapdbDoc(doc)
        # managed_docs.append(BapdbDoc(doc))
        # print(100 * "=")
        # print(managed_docs.complete_doc_corpus)
        # print(100 * "=")
        probabilistic_disease = BucketUtil.find_appropriate_disease(bapdb_doc.get_doc_corpus().diagnostic)

        if probabilistic_disease != 'NOT-SPECIFIED':
            disease_doc_str = DocUtil.build_update_json_based_doc_str(bapdb_doc.get_doc_corpus(), kwds_json, probabilistic_disease)
            # db.update_disease_doc(DISEASE_INDEX[probabilistic_disease], disease_doc_str)
            kwds_json[probabilistic_disease].append(disease_doc_str)

    with open("/Users/danilamarius-cristian/PycharmProjects/pythonProject2/kwds.json", "w") as outfile:
        json.dump(kwds_json, outfile)


if __name__ == '__main__':
    # fetch_stats()
    # process_stats()
    # process_keywords_json()
    process_core()