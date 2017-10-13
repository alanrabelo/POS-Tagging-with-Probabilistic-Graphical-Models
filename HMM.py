
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
        self.total = 0

    def loadTrainningData(self, filename):

        self.generatePossibleLabels()
        fh = open(filename, 'r')
        for line in fh.readlines():
            sentenceSplitted = line.replace('\n', '').split(' ')
            for index, wordFromSentence in enumerate(sentenceSplitted):
                word, label = wordFromSentence.split('_')

                word = str(word).lower()

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
                if label.startswith('NUM'):
                    label = 'NUM'
                elif label.startswith('N'):
                    label = 'N'
                if label.startswith('ADV'):
                    label = 'ADV'

                if previousLabel.startswith('PREP'):
                    previousLabel = 'PREP'
                if previousLabel.startswith('PRO') or previousLabel.startswith('PDEN'):
                    previousLabel = 'PRO'
                if previousLabel.startswith('K'):
                    previousLabel = 'K'
                if previousLabel.startswith('NUM'):
                    previousLabel = 'NUM'
                elif previousLabel.startswith('N'):
                    previousLabel = 'N'
                if previousLabel.startswith('ADV'):
                    previousLabel = 'ADV'


                self.labels.add(str(label))
                if label in self.words:
                    probabilitiesDict = self.words[label]
                    if word in probabilitiesDict:
                        probabilitiesDict[word] += 1
                    else:
                        probabilitiesDict[word] = 1
                    self.words[label]['TOTALABEL'] += 1
                else:
                    self.words[label] = {word : 1, 'TOTALABEL' : 1}

                # if word in self.words:
                #     probabilitiesDict = self.words[word]
                #     if label in probabilitiesDict:
                #         probabilitiesDict[label] += 1
                #     else:
                #         probabilitiesDict[label] = 1
                #     self.words[word]['total'] += 1
                # else:
                #     self.words[word] = {label : 1, 'total' : 1}

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

        for label in self.words.keys():
            totalForPrevious = self.words[label]['TOTALABEL']

            print(self.words[label]['TOTALABEL'])

            #del self.words[label]['total']

            for word in self.words[label]:
                self.words[label][word] /= totalForPrevious



    def classify(self, sentence, numberOfArranges : int):

        sentence = str(sentence).lower()
        splittedSentence = sentence.replace('.', ' .').replace(',', ' ,').split(' ')

        possibleArranges = self.possibleArranges(len(splittedSentence))
        probabilityOfArrange = []

        for index,arrange in enumerate(possibleArranges):
            if index / len(possibleArranges) % 0.01 == 0:
                print(index / len(possibleArranges))
            produtOfProbabilites = 1
            #arrange[0].value[0] == 'ART' and arrange[1].value[0] == 'N' and arrange[2].value[0] == 'V'
            for index, word in enumerate(splittedSentence):
                if word not in self.words[arrange[index].value[0]]:
                    probabilityOfWord = 0.000000000000001
                else:
                    probabilityOfWord = self.words[arrange[index].value[0]][word]

                if arrange[index-1].value[0] not in self.bigrams or arrange[index].value[0] not in self.bigrams['EMPTY' if index == 0 else arrange[index-1].value[0]]:
                    probabilityOfBigram = 0.000000000000001
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
                #print(probability)
                if probabilityOfArrange[index] > max:
                    max = probabilityOfArrange[index]
                    maxIndexes = [index]
                elif probabilityOfArrange[index] == max:
                    #print(probabilityOfArrange[index])
                    maxIndexes.append(index)

        #print(max)
        return np.array(possibleArranges)[maxIndexes]

    def possibleArranges(self, count: int):
        # Gets all combinations of labels with repetition
        return list([p for p in itertools.product(self.possibleLabels, repeat=count)])

    def generatePossibleLabels(self):
        self.possibleLabels = list(set(map(Label, Label)))
