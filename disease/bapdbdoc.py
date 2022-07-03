import re
from typing import Dict, List

from disease.doccorpus import DocCorpus
from utils.token_util import TokenUtil


DISEAES: Dict[str, str] = {
    'anaphylaxis': 'anaphylaxis',
    'appendicitis': 'appendicitis',
    'asthma-attack': 'asthma attack',
    'copd-attack': 'COPD - Chronic Obstructive Pulmonary Disease Exacerbation',
    'diverticulosis-attack': 'diverticulosis attack',
    'urinary-retention-attack': 'urinary retention attack',
    'urinary-tract-infection-attack': 'urinary tract infection attack',
    'hypertensive-crisis-attack': 'hypertensive crisis attack',
    'lumbago': 'lumbago pain in the muscle and joints of the lower back',
    'nstemi': 'NSTEMI - Non-ST segment elevation myocardial infarction',
    'ankle-sprains': 'ankle sprains',
    'urolithiasis': 'urolithiasis calculi in the urinary tract'
}

DISEASES_GERMAN: List[str] =[
    'anaphylaxie',
    'appendizitis',
    'asthmaanfall',
    'copd exazerbation',
    'divertikulitis',
    'harnverhalt',
    'hwi',
    'hypertensive entleisung',
    'lumbago',
    'nstemr',
    'osg distorsion',
    'urolithiasis'
]

class BapdbDoc:

    def __init__(self, data):
        self.doc_data = data['_source']
        self.complete_doc_corpus = ''

        self.diag = []

        if self.doc_data['diagnostic']:
            for diag in self.doc_data['diagnostic']:
                self.complete_doc_corpus += diag[1]
                self.diag.append(diag[0])

        self.complete_doc_corpus += self.doc_data['anamnesis']
        self.complete_doc_corpus += self.doc_data['berteleug']
        self.complete_doc_corpus += self.doc_data['anamnesis']
        self.complete_doc_corpus += self.doc_data['procedure']

        # clear the final output of unwanted chars
        self.complete_doc_corpus = re.sub(r"[\n\t]*", "", self.complete_doc_corpus)

        # remove stepwords
        self.complete_doc_corpus = ' '.join(TokenUtil.remove_words(self.complete_doc_corpus))

        self.doc_corpus = DocCorpus(self.complete_doc_corpus, self.diag)

    def get_doc_corpus(self) -> DocCorpus:
        return self.doc_corpus
