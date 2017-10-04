import numpy.random as random
import numpy as np
from Features import Features, FeatureFunction
from Enums import Label
from Sentence import Sentence
from Data import Data
import itertools

class CRF:

    weigths = []
    alpha = 0.1
    numberOfFeatures = 6
    featuresFunctions = [FeatureFunction]
    sentences = [Sentence]

    possibleLabels = set(Label)


    def loadData(self, filename):
        data = Data()
        self.sentences = data.sentencesFromFile(filename)
        print('Found ' + str(len(self.sentences)) + ' sentences in data')
        self.generatePossibleLabels()
        self.generateFeatures()

    def generatePossibleLabels(self):
        self.possibleLabels = list(set(map(Label, Label)))

    def generateFeatures(self):
        self.featuresFunctions = Features.featuresFromSentences(self.sentences)

    def train(self):
        print('not trainning yet, we have random weigths')


    def predict(self, sentence : str):

        best = self.wordToFeatures(sentence, numberOfArranges=1)
        print('best combination based on features ' + str(best))
        self.weigths = [(random.randint(0, 1000)) / 1000 for _ in range(6)]
        return 'In Construction'

    def wordToFeatures(self, sentence : str, numberOfArranges : int = 5):


        arrangesOfLabels = self.possibleArranges(sentence)
        splittedSentence = sentence.split(' ')

        probabilityOfArrange = []

        print('Entrou no word2features with ' + str(len(self.featuresFunctions)))

        for arrange in arrangesOfLabels:
            sumOfFeatures = 0

            for feature in self.featuresFunctions:
                for position in range(1, len(splittedSentence)):
                    current = arrange[position]
                    previous = arrange[position-1]
                    sumOfFeatures += Features.verify(feature, current, previous)

            probabilityOfArrange.append(sumOfFeatures)

        bestIndices = np.argpartition(probabilityOfArrange, -numberOfArranges)[-numberOfArranges:]
        print(np.array(arrangesOfLabels)[bestIndices])
        print(np.array(probabilityOfArrange)[bestIndices])


        return(np.array(arrangesOfLabels)[bestIndices])


    def possibleArranges(self, sentence : str):
        # Gets all combinations of labels
        sentenceSplitted = sentence.split(' ')
        return list(itertools.permutations(self.possibleLabels, len(sentenceSplitted)))
