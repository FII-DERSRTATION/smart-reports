import json
import uuid
from typing import Dict

import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth

DISEASE_INDEX: Dict[str, str] = {
    'anaphylaxis': 'bapdb-anaphylaxis-keywords',
    'appendicitis': 'bapdb-appendicitis-keywords',
    'asthma-attack': 'bapdb-asthma-attack-keywords',
    'copd-attack': 'bapdb-copd-attack-keywords',
    'diverticulosis-attack': 'bapdb-diverticulosis-attack-keywords',
    'urinary-retention-attack': 'bapdb-urinary-retention-attack-keywords',
    'urinary-tract-infection-attack': 'bapdb-urinary-tract-infection-attack-keywords',
    'hypertensive-crisis-attack': 'bapdb-hypertensive-crisis-attack-keywords',
    'lumbago': 'bapdb-lumbago-keywords',
    'nstemi': 'bapdb-nstemi-keywords',
    'ankle-sprains': 'bapdb-ankle-sprains-keywords',
    'urolithiasis': 'bapdb-urolithiasis-keywords'
}


class AWSSearchDB:

    def __init__(self):
        host = 'search-tengine2-5nn4xi272rmoglndi7swodwzpy.us-east-1.es.amazonaws.com'
        port = 443
        # auth = ('tengine', '^T3ngine')
        credentials = boto3.Session(
            aws_access_key_id='AKIAUCYMDOCRXMRNIOPV',
            aws_secret_access_key='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',
        ).get_credentials()
        auth = AWSV4SignerAuth(credentials, 'us-east-1')

        self.client = OpenSearch(
            hosts=[{'host': host, 'port': port}],
            http_auth=auth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection,
            request_timeout=1000000
        )

    def create_disease_index(self, prefix):
        index_name = 'bapdb-anaphylaxis-keywords'
        index_body = {
            'settings': {
                'index': {
                    'number_of_shards': 4
                }
            }
        }

        response = self.client.indices.create(index_name, body=index_body)
        print('\nCreating index:')
        print(response)

        index_name = 'bapdb-appendicitis-keywords'
        index_body = {
            'settings': {
                'index': {
                    'number_of_shards': 4
                }
            }
        }

        response = self.client.indices.create(index_name, body=index_body)
        print('\nCreating index:')
        print(response)

        index_name = 'bapdb-asthma-attack-keywords'
        index_body = {
            'settings': {
                'index': {
                    'number_of_shards': 4
                }
            }
        }

        response = self.client.indices.create(index_name, body=index_body)
        print('\nCreating index:')
        print(response)

        index_name = 'bapdb-copd-attack-keywords'
        index_body = {
            'settings': {
                'index': {
                    'number_of_shards': 4
                }
            }
        }

        response = self.client.indices.create(index_name, body=index_body)
        print('\nCreating index:')
        print(response)

        index_name = 'bapdb-diverticulosis-attack-keywords'
        index_body = {
            'settings': {
                'index': {
                    'number_of_shards': 4
                }
            }
        }

        response = self.client.indices.create(index_name, body=index_body)
        print('\nCreating index:')
        print(response)

        index_name = 'bapdb-urinary-retention-attack-keywords'
        index_body = {
            'settings': {
                'index': {
                    'number_of_shards': 4
                }
            }
        }

        response = self.client.indices.create(index_name, body=index_body)
        print('\nCreating index:')
        print(response)

        index_name = 'bapdb-urinary-tract-infection-attack-keywords'
        index_body = {
            'settings': {
                'index': {
                    'number_of_shards': 4
                }
            }
        }

        response = self.client.indices.create(index_name, body=index_body)
        print('\nCreating index:')
        print(response)

        index_name = 'bapdb-hypertensive-crisis-attack-keywords'
        index_body = {
            'settings': {
                'index': {
                    'number_of_shards': 4
                }
            }
        }

        response = self.client.indices.create(index_name, body=index_body)
        print('\nCreating index:')
        print(response)

        index_name = 'bapdb-lumbago-keywords'
        index_body = {
            'settings': {
                'index': {
                    'number_of_shards': 4
                }
            }
        }

        response = self.client.indices.create(index_name, body=index_body)
        print('\nCreating index:')
        print(response)

        index_name = 'bapdb-nstemi-keywords'
        index_body = {
            'settings': {
                'index': {
                    'number_of_shards': 4
                }
            }
        }

        response = self.client.indices.create(index_name, body=index_body)
        print('\nCreating index:')
        print(response)

        index_name = 'bapdb-ankle-sprains-keywords'
        index_body = {
            'settings': {
                'index': {
                    'number_of_shards': 4
                }
            }
        }

        response = self.client.indices.create(index_name, body=index_body)
        print('\nCreating index:')
        print(response)

        index_name = 'bapdb-urolithiasis-keywords'
        index_body = {
            'settings': {
                'index': {
                    'number_of_shards': 4
                }
            }
        }

        response = self.client.indices.create(index_name, body=index_body)
        print('\nCreating index:')
        print(response)

        print("done creating diseases indexes")

    def query_bapdb_index(self):
        # Search for the document.
        query = {
            'size': 100
        }

        response = self.client.search(
            body=query,
            index='bapdb-reports-prod-4'
        )
        # print('\nSearch results:')
        # print(response)
        return response

    def query_disease_data(self, disease):
        # Search for the document.
        query = {
            'size': 100
        }

        response = self.client.search(
            body=query,
            index=DISEASE_INDEX[disease]
        )
        # print('\nSearch results:')
        # print(response)
        return response

    def update_disease_doc(self, index: str, text: str):
        # Add a document to the index.
        id = str(uuid.uuid4())

        response = self.client.index(
            index=index,
            body='{"text": "%s"}' % text,
            id=id,
            refresh=True
        )

        print('\nAdding document:')
        print(response)


    def find_disease_doc_by_id_lab(self, id_lab):
        # Search for the document.
        q = 'miller'
        query = {
          "size": 1000,
          "query": {
            "term": {
              "id_lab": {
                "value": id_lab,
                "boost": 1.0
              }
            }
          }
        }

        response = self.client.search(
            body=query,
            index='bapdb-reports-prod-6'
        )
        # print('\nSearch results:')
        # print(response)
        return response


    def add_stat(self, stat):
        # Add a document to the index.
        id = str(uuid.uuid4())

        response = self.client.index(
            index='bapdb-stats-5',
            body=stat,
            id=id,
            refresh=True
        )

        print('\nAdding document:')
        print(response)

    def query_stats_index(self):
        # Search for the document.
        query = {
            'size': 1000
        }

        response = self.client.search(
            body=query,
            index='bapdb-stats-5'
        )
        # print('\nSearch results:')
        # print(response)
        return response