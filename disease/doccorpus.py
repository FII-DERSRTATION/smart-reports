from typing import List


class DocCorpus:

    def __init__(self, text: str, diagnostic: List[str]):
        self.text = text
        self.diagnostic = diagnostic

    def get_difference(self, docc2) -> str:
        tokens = self.text.split()

        difference = []

        for token in tokens:
            if token not in docc2.text:
                difference.append(token)

        return ' '.join(difference)

