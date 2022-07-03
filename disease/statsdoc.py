class StatsDoc:

    def __init__(self, doc):
        self.diagnosis, self.stats = self._parse_opensearch_entry(doc)

    def _parse_opensearch_entry(self, doc):
        raw_doc = doc['_source']

        diagnostic = raw_doc['diagnosis']
        stats = raw_doc['stats']

        return diagnostic, stats