from Enums import Label
from Sentence import Sentence

import itertools
import numpy as np
from optparse import OptionParser
import inspect

class FeatureFunction():

    previous_label = Label['V']
    label = Label['V']
    numberOfUses = 1

    def __init__(self, previous_label : Label, label : Label):
        self.previous_label = previous_label
        self.label = label
        self.numberOfUses = 1

    def __hash__(self):
        return hash(self.previous_label) ^ hash(self.label)

    def __eq__(self, other):
        if (self.previous_label, self.label) == (other.previous_label, other.label):
            self.numberOfUses += 1
            return True
        else:
            return False

    def __lt__(self, other):
        return self.numberOfUses < other.numberOfUses

class Features:


    @classmethod

    def verify(cls, feature : FeatureFunction, current : Label, previous : Label):

        if feature.previous_label == previous:
            if feature.label == current:
                return 1
            else:
                return 0
        else:
            return 0

    @classmethod
    def featuresFromSentences(self, sentences : [Sentence]):

        print('entrou')
        features = set()

        for sentence in sentences:

            for i in range(1, len(sentence.labels)):

                label = Label[sentence.labels[i]]
                previousLabel = Label[sentence.labels[i-1]]

                feature = FeatureFunction(previousLabel, label)
                features.add(feature)

        sortedList = sorted(list(features), key=lambda numberOfUses: numberOfUses, reverse=True)

        filteredList = [FeatureFunction]

        for feat in sortedList:
            if feat.numberOfUses > 1000:
                filteredList.append(feat)
        print('We have infiltered ' + str(len(list(filteredList))))

        return filteredList

    def features(self):
        return [
            self.featureAdverb,
            self.featureAdverbWithPrevious,
            self.featureVerbAr,
            self.featureVerbEr,
            self.featureVerbIr,
            self.featureVerbOr,
            self.featureNounAfterArticle,
            self.featureVerbAfterPronoum,
            self.featureVerbAfterPronoumFirst
        ]



    def featureAdverb(self, currentWord : str, previousWord : str, positionInSentence : int, currentLabel, previousLabel):
        return 1 if currentWord.endswith('mente') and currentLabel == Label.ADV else 0

    def featureAdverbWithPrevious(self, currentWord : str, previousWord : str, positionInSentence : int, currentLabel, previousLabel):
        return 1 if currentWord.endswith('mente') and currentLabel == Label.ADV and previousLabel == Label.V else 0

    def featureVerbAfterPronoum(self, currentWord : str, previousWord : str, positionInSentence : int, currentLabel, previousLabel):
        return 1 if currentLabel == Label.V and previousLabel == Label.PROPESS else 0

    def featureVerbAfterPronoumFirst(self, currentWord : str, previousWord : str, positionInSentence : int, currentLabel, previousLabel):
        return 1 if previousLabel == Label.PROPESS and positionInSentence == 1 else 0

    def featureVerbAr(self, currentWord: str, previousWord: str, positionInSentence: int, currentLabel,
                          previousLabel):
        return 1 if currentWord.endswith('ar') and currentLabel == Label.V else 0

    def featureVerbEr(self, currentWord: str, previousWord: str, positionInSentence: int, currentLabel,
                          previousLabel):
        return 1 if currentWord.endswith('er') and currentLabel == Label.V else 0

    def featureVerbIr(self, currentWord: str, previousWord: str, positionInSentence: int, currentLabel,
                          previousLabel):
        return 1 if currentWord.endswith('ir') and currentLabel == Label.V else 0

    def featureVerbOr(self, currentWord: str, previousWord: str, positionInSentence: int, currentLabel,
                          previousLabel):
        return 1 if currentWord.endswith('or') and currentLabel == Label.V else 0

    def featureNounAfterArticle(self, currentWord: str, previousWord: str, positionInSentence: int, currentLabel : Label,
                          previousLabel : Label):
        return 1 if (currentLabel == Label.N or currentLabel == Label.NPROP) and previousLabel == Label.ART else 0

