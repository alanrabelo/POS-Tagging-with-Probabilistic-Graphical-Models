from Enums import Label
import itertools
import numpy as np
from optparse import OptionParser
import inspect

class FeatureFunction(object):


    def __init__(self, previous_label, label):
        self.previous_label = previous_label
        self.label = label
        self.numberOfUses = 0


    def apply(self, previous_label, label):
        return 1 if self.previous_label == previous_label and self.label == label else 0

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

    labels = list(map(Label, Label))
    def wordToFeatures(self, sentence : str, corpusFeatures, numberOfArranges : int = 5):

        arrangesOfLabels = self.possibleArranges(sentence)
        splittedSentence = sentence.split(' ')
        features = self.features()

        probabilityOfArrange = []

        print('Entrou no word2features ' + str(len(corpusFeatures)))

        for arrange in arrangesOfLabels:
            sumOfFeatures = 0

            for feature in corpusFeatures[0:100]:
                for position in range(1, len(splittedSentence)):
                    sumOfFeatures += feature.apply(arrange[position-1].value, arrange[position].value)

            probabilityOfArrange.append(sumOfFeatures)


        # for arrange in arrangesOfLabels:
        #     sumOfFeatures = 0
        #
        #     for feature in features:
        #         for position in range(1, len(splittedSentence)):
        #             sumOfFeatures += feature(splittedSentence[position], splittedSentence[position-1], position, arrange[position], arrange[position-1])
        #     probabilityOfArrange.append(sumOfFeatures)


        bestIndices = np.argpartition(probabilityOfArrange, -numberOfArranges)[-numberOfArranges:]
        print(np.array(arrangesOfLabels)[bestIndices])
        print(np.array(probabilityOfArrange)[bestIndices])


        return(np.array(arrangesOfLabels)[bestIndices])

    def create_feature_functions(self, sentences):

        features_functions = set()
        print(sentences[0])
        for labels in sentences:
            for i in range(1, len(labels)):

                feature = FeatureFunction(labels[i - 1], labels[i])

                if features_functions.__contains__(feature):
                    removedFeature = features_functions.remove(feature)
                    feature.numberOfUses = removedFeature + 1
                    features_functions.add(feature)
                else:
                    features_functions.add(feature)

        print(features_functions)
        return list(features_functions)


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

    def possibleArranges(self, sentence : str):
        # Gets all combinations of labels
        sentenceSplitted = sentence.split(' ')
        return list(itertools.permutations(self.labels, len(sentenceSplitted)))

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

