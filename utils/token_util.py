from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class TokenUtil:

    @staticmethod
    def remove_words(data):
        """
        :param data: sentence to bve filtered
        :return: list with words in data without stopwords
        """
        stop_words = set(stopwords.words('english'))

        word_tokens = word_tokenize(data)

        filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]

        filtered_sentence = []

        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)

        return filtered_sentence