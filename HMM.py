
import operator
from Enums import Label
import itertools
import numpy as np


class HMM:

    def __init__(self):
        self.labels = set()
        self.tags = []
        self.sentences = []
        self.words = dict()
        self.bigrams = dict()
        self.bigramsProbabilities = dict()

    def loadTrainningData(self, filename):

        self.generatePossibleLabels()
        fh = open(filename, 'r')
        for line in fh.readlines():
            sentenceSplitted = line.replace('\n', '').split(' ')
            for index, wordFromSentence in enumerate(sentenceSplitted):
                word, label = wordFromSentence.split('_')


                if index == 0:
                    previousLabel = 'EMPTY'
                else:
                    previousLabel = sentenceSplitted[index-1].split('_')[1]

                if label.startswith('PREP'):
                    label = 'PREP'
                if label.startswith('PRO') or label.startswith('PDEN'):
                    label = 'PRO'
                if label.startswith('K'):
                    label = 'K'
                if label.startswith('N'):
                    label = 'N'
                if label.startswith('ADV'):
                    label = 'ADV'

                if previousLabel.startswith('PREP'):
                    previousLabel = 'PREP'
                if previousLabel.startswith('PRO') or previousLabel.startswith('PDEN'):
                    previousLabel = 'PRO'
                if previousLabel.startswith('K'):
                    previousLabel = 'K'
                if previousLabel.startswith('N'):
                    previousLabel = 'N'
                if previousLabel.startswith('ADV'):
                    previousLabel = 'ADV'


                self.labels.add(str(label))
                if word in self.words:
                    probabilitiesDict = self.words[word]
                    if label in probabilitiesDict:
                        probabilitiesDict[label] += 1
                    else:
                        probabilitiesDict[label] = 1
                    self.words[word]['total'] += 1
                else:
                    self.words[word] = {label : 1, 'total' : 1}

                if previousLabel in self.bigrams :
                    if label in self.bigrams[previousLabel]:
                        self.bigrams[previousLabel][label] += 1
                    else:
                        self.bigrams[previousLabel][label] = 1
                    self.bigrams[previousLabel]['total'] += 1
                else:
                    self.bigrams[previousLabel] = { label : 1, 'total' : 1 }


        fh.close()

        for previous in self.bigrams.keys():

            totalForPrevious = self.bigrams[previous]['total']

            del self.bigrams[previous]['total']

            for current in self.bigrams[previous]:
                self.bigrams[previous][current] /= totalForPrevious

        for word in self.words.keys():

            totalForPrevious = self.words[word]['total']

            del self.words[word]['total']

            for label in self.words[word]:
                self.words[word][label] /= totalForPrevious

        print(self.words)



    def classify(self, sentence, numberOfArranges : int):

        splittedSentence = sentence.split(' ')
        possibleArranges = self.possibleArranges(len(splittedSentence))
        probabilityOfArrange = []

        for index,arrange in enumerate(possibleArranges):
            if index / len(possibleArranges) % 0.01 == 0:
                print(index / len(possibleArranges))
            produtOfProbabilites = 1
            for index, word in enumerate(splittedSentence):
                if word not in self.words or arrange[index].value[0] not in self.words[word]:
                    probabilityOfWord = 0.00000000001
                else:
                    probabilityOfWord = self.words[word][arrange[index].value[0]]

                if arrange[index-1].value[0] not in self.bigrams or arrange[index].value[0] not in self.bigrams['EMPTY' if index == 0 else arrange[index-1].value[0]]:
                    probabilityOfBigram = 0.00000000001
                else:
                    probabilityOfBigram = self.bigrams['EMPTY' if index == 0 else arrange[index - 1].value[0]][
                        arrange[index].value[0]]

                produtOfProbabilites *= probabilityOfWord * probabilityOfBigram

                # if index == 0:
                #     if word in self.words and arrange[index] in self.words[word] and 'EMPTY' in self.bigrams and arrange[index] in self.bigrams['EMPTY']:
                #         produtOfProbabilites *= probabilityOfWord * probabilityOfBigram
                # else:
                #     if word in self.words and arrange[index] in self.words[word] and arrange[index-1] in self.bigrams and arrange[index] in self.bigrams[arrange[index-1]]:
                #         produtOfProbabilites *= self.words[arrange[index]] *
            #print(arrange)
            #print(produtOfProbabilites)
            probabilityOfArrange.append(produtOfProbabilites)


        max = 0
        maxIndexes = []

        for index,probability in enumerate(probabilityOfArrange):
            if probability != 1:
                if probabilityOfArrange[index] > max:
                    max = probabilityOfArrange[index]
                    maxIndexes = [index]
                elif probabilityOfArrange[index] == max:
                    print(probabilityOfArrange[index])
                    maxIndexes.append(index)

        return np.array(possibleArranges)[maxIndexes]

    def possibleArranges(self, count: int):
        # Gets all combinations of labels
        return list(itertools.permutations(self.possibleLabels, count))

    def generatePossibleLabels(self):
        self.possibleLabels = list(set(map(Label, Label)))


























