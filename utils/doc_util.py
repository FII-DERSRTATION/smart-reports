from functools import reduce

from disease.bapdbdoc import BapdbDoc
from disease.doccorpus import DocCorpus
from opensearch.AWSSearchDB import AWSSearchDB, DISEASE_INDEX


class DocUtil:

    @staticmethod
    def build_update_doc_str(doc: DocCorpus, db: AWSSearchDB, probabilist_diag: str) -> str:
        disease_doc_raw = db.query_disease_data(probabilist_diag)
        disease_doc = disease_doc_raw['hits']['hits']

        dif_text = doc.text

        if len(disease_doc) > 0:
            for entry in disease_doc:
                dif_text = doc.get_difference(DocCorpus(entry['_source']['text'], DocUtil.find_key(entry['_index'], DISEASE_INDEX)))
                doc.text = dif_text

        return dif_text



    @staticmethod
    def build_update_json_based_doc_str(doc: DocCorpus, json, probabilist_diag: str) -> str:
        disease_kwds_text = ' '.join(json[probabilist_diag])


        dif_text = doc.text

        if len(disease_kwds_text) > 0:
            # for entry in disease_doc:
            #     dif_text = doc.get_difference(DocCorpus(entry['_source']['text'], DocUtil.find_key(entry['_index'], DISEASE_INDEX)))
            #     doc.text = dif_text

            dif_text = doc.get_difference(DocCorpus(disease_kwds_text, [probabilist_diag]))

        return dif_text


    # needs refactor
    @staticmethod
    def find_key(value, dictionary):
        return reduce(lambda x, y: x if x is not None else y,
                      map(lambda x: x[0] if x[1] == value else None,
                          dictionary.items()))
