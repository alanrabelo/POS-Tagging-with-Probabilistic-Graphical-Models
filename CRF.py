import numpy.random as random
import numpy as np
from Features import Features, FeatureFunction
from Enums import Label
from Sentence import Sentence
from Data import Data
import itertools

class CRF:

    weigths = [float]
    alpha = 0.1
    numberOfFeatures = 6
    featuresFunctions = [FeatureFunction]
    sentences = [Sentence]
    featuresFunctionsHandMade = []
    possibleLabels = set(Label)


    def loadData(self, filename):
        data = Data()
        self.sentences = data.sentencesFromFile(filename)
        print('Found ' + str(len(self.sentences)) + ' sentences in data')
        self.generatePossibleLabels()
        self.generateFeatures()
        self.train()

    def generatePossibleLabels(self):
        self.possibleLabels = list(set(map(Label, Label)))

    def generateFeatures(self):

        featureGenerator = Features()
        self.featuresFunctionsHandMade = featureGenerator.features()
        self.featuresFunctions = Features.featuresFromSentences(self.sentences)
        self.weigths = np.random.uniform(low=0.0, high=1.0, size=(len(self.featuresFunctionsHandMade)))

    def train(self):

        self.weigths = []
        for _ in range(len(self.featuresFunctionsHandMade)):
            self.weigths.append((random.randint(0, 1000)) / 1000)

        print('started trainning')

        for sentence in self.sentences:

            sumOfModel = 0
            for featureIndex,feature in enumerate(self.featuresFunctionsHandMade):
                for index in range(1, len(sentence.words)):

                    current = sentence.words[index]
                    currentLabel = sentence.labels[index]
                    previous = sentence.words[index-1]
                    previousLabel = sentence.labels[index-1]

                    if index == len(sentence.words) - 1:
                        result = feature(current, previous, -1, currentLabel, previousLabel)
                    else:
                        result = feature(current, previous, index, currentLabel, previousLabel)
                    sumOfModel += result

            print(sumOfModel)

            sumOfModelPossibles = 0

            for possibleArrangeIndex,sequence in enumerate(self.possibleArranges(len(sentence.words))):
                for featureIndex, feature in enumerate(self.featuresFunctionsHandMade):
                    for index in range(1, len(sentence.words)):

                        current = sentence.words[index]
                        currentLabel = sentence.labels[index]
                        previous = sentence.words[index - 1]
                        previousLabel = sentence.labels[index - 1]

                        if index == len(sentence.words) - 1:
                            result = feature(current, previous, -1, currentLabel, previousLabel)
                        else:
                            result = feature(current, previous, index, currentLabel, previousLabel)
                        sumOfModelPossibles += result

            ratioModelSum = sumOfModelPossibles/len(self.possibleArranges(len(sentence.words)))
            print('The hope value is ' + str(sumOfModel) + ' but the returned Value is ' + str(ratioModelSum))

            for index in range(0, len(self.weigths)):
                self.weigths[index] += self.alpha * (sumOfModel - ratioModelSum)

        print("Finished Trainnning of features")


    def predict(self, sentence : str):

        best = self.verifySentence(sentence, numberOfArranges=1)
        print('best combination based on features ' + str(best))
        return 'In Construction'


    def resultOfFeaturesInWeigths(self, sentence):

        arranges = list(itertools.permutations(self.possibleLabels, len(sentence.words) + 1))

        probabilityOfArrange = []

        for (indexTop,arrange) in enumerate(arranges):
            sumOfFeatures = 0

            for (index, feature) in enumerate(self.featuresFunctions):
                for position in range(0, len(sentence.labels)):
                    current = arrange[position]
                    previous = arrange[position-1]
                    response = Features.verify(feature, current, previous)
                    sumOfFeatures += self.weigths[index] * response
            probabilityOfArrange.append(sumOfFeatures)
        bestIndices = np.argpartition(probabilityOfArrange, -1)[-1:]

        return bestIndices[0]

    def verifySentence(self, sentence : str, numberOfArranges : int = 1):


        arrangesOfLabels = self.possibleArranges(len(sentence))
        splittedSentence = sentence.split(' ')

        probabilityOfArrange = []

        # print('Entrou no word2features with ' + str(len(self.featuresFunctions)))

        for arrange in arrangesOfLabels:
            sumOfFeatures = 0

            for (index, feature) in enumerate(self.featuresFunctionsHandMade):
                for position in range(0, len(splittedSentence)):
                    currentLabel = arrange[position]
                    previousLabel = arrange[position-1]
                    currentWord = splittedSentence[position]
                    previousWord = splittedSentence[position-1]

                    response = self.weigths[index] * feature(currentWord, previousWord, position, currentLabel, previousLabel)
                    sumOfFeatures += response
            probabilityOfArrange.append(sumOfFeatures)

        bestIndices = np.argpartition(probabilityOfArrange, -numberOfArranges)[-numberOfArranges:]
        return(np.array(arrangesOfLabels)[bestIndices])


    def possibleArranges(self, sentence : str):
        # Gets all combinations of labels
        sentenceSplitted = sentence.split(' ')
        return list(itertools.permutations(self.possibleLabels, len(sentenceSplitted)))

    def possibleArranges(self, count : int):
        # Gets all combinations of labels
        return list(itertools.permutations(self.possibleLabels, count))