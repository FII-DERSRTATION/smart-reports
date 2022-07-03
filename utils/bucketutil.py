from typing import List
from disease.bapdbdoc import DISEAES, DISEASES_GERMAN
from fuzzywuzzy import fuzz

from stats.stats_processor import STATS_KWDS


class BucketUtil:


    @staticmethod
    def find_appropriate_disease(diagnostic: List[str]):

        ratio_disease_distribution = {}

        for disease_key in DISEAES:
            max_ratio = 0
            iteration_disease = 'NOT-SPECIFIED'
            for diag in diagnostic:
                ratio = fuzz.ratio(DISEAES[disease_key].lower(), diag.lower())

                if ratio > max_ratio:
                    max_ratio = ratio
                    iteration_disease = disease_key

            ratio_disease_distribution[iteration_disease] = max_ratio

        # now select the disease with the biggest ratio

        key, value = max(ratio_disease_distribution.items(), key=lambda x: x[1])

        return key


    @staticmethod
    def find_appropriate_disease_german(diagnostic: List[str]):

        ratio_disease_distribution = {}

        for disease_key in DISEASES_GERMAN:
            max_ratio = 0
            iteration_disease = 'NOT-SPECIFIED'
            for diag in diagnostic:
                # nu facce pe descriere, ci pe keye, pentru ca nu exista descriere
                ratio = fuzz.ratio(disease_key, diag.lower())

                if ratio > max_ratio:
                    max_ratio = ratio
                    iteration_disease = disease_key

            ratio_disease_distribution[iteration_disease] = max_ratio

        # now select the disease with the biggest ratio

        key, value = max(ratio_disease_distribution.items(), key=lambda x: x[1])

        return key


    @staticmethod
    def find_appropriate_stat( canditate_stat):


        final_stat = ''
        for stat_key in STATS_KWDS:
            max_ration = 0
            ratio = fuzz.ratio(stat_key, canditate_stat)
            if ratio > max_ration:
                max_ration = ratio
                final_stat = stat_key

        return final_stat

