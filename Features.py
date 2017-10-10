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
        # features = set()
        #
        # for sentence in sentences:
        #
        #     for i in range(1, len(sentence.labels)):
        #
        #         label = Label[sentence.labels[i]]
        #         previousLabel = Label[sentence.labels[i-1]]
        #
        #         feature = FeatureFunction(previousLabel, label)
        #         features.add(feature)
        #
        # sortedList = sorted(list(features), key=lambda numberOfUses: numberOfUses, reverse=True)
        #
        # filteredList = [FeatureFunction]
        #
        # for feat in sortedList:
        #     if feat.numberOfUses > 1000:
        #         filteredList.append(feat)
        # print('We have infiltered ' + str(len(list(filteredList))))
        #
        # return filteredList


    def features(self):
        return [
            self.featureAdverb,
            self.featureAdverbWithPrevious,
            self.featureNounAfterArticle,
            self.featureNounAfterPossessives,
            self.pronounPESSReto,
            self.pronounPESSOblique,
            self.featureVerbAfterPronoum,
            self.featureVerbAfterPronoumFirst,
            self.featureVerbAr,
            self.featureVerbEr,
            self.featureVerbIr,
            self.featureVerbOr,
            self.featureNotConjunction
        ]


    # Features for Adverbs
    def featureAdverb(self, currentWord : str, previousWord : str, positionInSentence : int, currentLabel : Label, previousLabel : Label):
        return 1 if currentWord.endswith('mente') and currentLabel == Label.ADV else 0

    def featureAdverbWithPrevious(self, currentWord : str, previousWord : str, positionInSentence : int, currentLabel : Label, previousLabel : Label):
        return 1 if currentWord.endswith('mente') and currentLabel == Label.ADV and previousLabel == Label.V else 0

    #features for Nouns
    def featureNounAfterArticle(self, currentWord: str, previousWord: str, positionInSentence: int, currentLabel : Label,
                          previousLabel : Label):
        return 1 if (currentLabel == Label.N) and previousLabel == Label.ART else 0

    def featureNounAfterPossessives(self, currentWord: str, previousWord: str, positionInSentence: int, currentLabel : Label,
                          previousLabel : Label):
        return 1 if (currentLabel == Label.N) and (previousLabel == Label.PRO) and (previousWord == 'meu' or 'minha' or 'meus' or 'minhas' or 'teu' or 'tua' or 'teus' or 'tuas' or 'seu' or 'sua' or 'seus' or 'suas' or 'nosso' or 'nossa' or 'nossos' or 'nossas' or 'vosso' or 'vossa' or 'vossos' or 'vossas' or 'seu' or 'sua' or 'seus' or 'suas') else 0

    #features for Pronouns
    def pronounPESSReto(self, currentWord: str, previousWord: str, positionInSentence: int, currentLabel : Label,
                        previousLabel : Label):
        return 1 if (currentWord.lower() == ('eu' or 'tu' or 'você' or 'ele' or 'ela' or 'nós' or 'vocês' or 'vós' or 'eles')) and currentLabel == Label.PRO else 0

    def pronounPESSOblique(self, currentWord: str, previousWord: str, positionInSentence: int, currentLabel : Label,
                        previousLabel : Label):
        return 1 if (currentWord.lower() == ('me' or 'te' or 'lhe' or 'se' or 'nos' or 'vos' or 'lhes')) and (currentLabel == (Label.PRO)) else 0

    # Features for Verbs
    def featureVerbAfterPronoumFirst(self, currentWord : str, previousWord : str, positionInSentence : int, currentLabel, previousLabel):
        return 1 if previousLabel == Label.PRO and currentLabel == Label.V and positionInSentence == 1 else 0

    def featureVerbAfterPronoum(self, currentWord: str, previousWord: str, positionInSentence: int, currentLabel : Label,
                          previousLabel : Label):
        return 1 if (currentLabel == Label.V) and previousLabel == (Label.PRO) else 0

    def featureVerbAr(self, currentWord: str, previousWord: str, positionInSentence: int, currentLabel : Label,
                          previousLabel : Label):
        return 1 if currentWord.endswith('ar') and currentLabel == Label.V else 0

    def featureVerbEr(self, currentWord: str, previousWord: str, positionInSentence: int, currentLabel : Label,
                          previousLabel : Label):
        if currentWord.endswith('er') and currentLabel == Label.V:
            "its a verb"
        return 0

        # return 1 if currentWord.endswith('er') and currentLabel == Label.V else 0

    def featureVerbIr(self, currentWord: str, previousWord: str, positionInSentence: int, currentLabel : Label,
                          previousLabel : Label):
        return 1 if currentWord.endswith('ir') and currentLabel == Label.V else 0

    def featureVerbOr(self, currentWord: str, previousWord: str, positionInSentence: int, currentLabel : Label,
                          previousLabel : Label):
        return 1 if currentWord.endswith('or') and currentLabel == Label.V else 0

    def featureNotConjunction(self, currentWord: str, previousWord: str, positionInSentence: int, currentLabel: Label,
                      previousLabel: Label):
        return 0 if currentLabel == Label.K and positionInSentence == -1 else 1

