
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
        self.bigramsSaw = set()
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

                self.bigramsSaw.add((previousLabel, label))

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

            #del self.words[label]['total']

            for word in self.words[label]:
                self.words[label][word] /= totalForPrevious



    def classify(self, sentence, numberOfArranges : int):

        # initial = 'EMPTY'
        #
        # possibles = [['EMPTY']] * numberOfArranges
        #
        # for index in range(0, numberOfArranges-1):
        #
        #
        #     nexts = list(self.bigrams['EMPTY'].keys())
        #
        #     for possible in possibles:
        #         possible.append()
        #
        #
        #     #
        #     # for value in nexts:
        #     #     np.append(possibles, value)
        #
        # print( ' possible' + str(possibles))





        print(self.bigrams)
        print('Started Classification')

        splittedSentence = sentence.replace('.', ' .').replace(',', ' ,').split(' ')
        possibleArranges = self.possibleArranges(len(splittedSentence))
        probabilityOfArrange = []

        viterbyDict = dict()
        timesSaved = 0
        totalTimes = 0
        for index,arrange in enumerate(possibleArranges):
            produtOfProbabilites = 1
            # print(str(index ) + '/' + str(len(possibleArranges)))
            for index, word in enumerate(splittedSentence):
                currentLabel = arrange[index].value[0]
                previousLabel = 'EMPTY' if index == 0 else arrange[index-1].value[0]


                # Verify dictionary for previous occurrencies
                tupleForCurrentiteration = (previousLabel,currentLabel,word)
                if tupleForCurrentiteration in viterbyDict:
                    timesSaved += 1
                    produtOfProbabilites *= viterbyDict[tupleForCurrentiteration]
                    continue
                totalTimes+=1


                if word not in self.words[currentLabel]:
                    probabilityOfWord = 0.001
                else:
                    probabilityOfWord = self.words[currentLabel][word]

                if previousLabel not in self.bigrams or currentLabel not in self.bigrams['EMPTY' if index == 0 else arrange[index-1].value[0]]:
                    probabilityOfBigram = 0.000000000000001
                    break
                else:
                    probabilityOfBigram = self.bigrams['EMPTY' if index == 0 else previousLabel][currentLabel]

                viterbyDict[(previousLabel, currentLabel, word)] = probabilityOfWord * probabilityOfBigram

                produtOfProbabilites *= probabilityOfWord * probabilityOfBigram

            probabilityOfArrange.append(produtOfProbabilites)


        max = 0
        maxIndexes = []

        print('Entered ' + str(timesSaved) + ' times in viterbidict')
        print('Calculeted ' + str(totalTimes) + ' times the probability')

        maxProbability = np.argmax(probabilityOfArrange)
        return possibleArranges[maxProbability]

        # for index,probability in enumerate(probabilityOfArrange):
        #     if probability != 1:
        #         #print(probability)
        #         if probabilityOfArrange[index] > max:
        #             max = probabilityOfArrange[index]
        #             maxIndexes = [index]
        #         elif probabilityOfArrange[index] == max:
        #             maxIndexes.append(index)
        #
        # return np.array(possibleArranges)[maxIndexes]

    def possibleArranges(self, count: int):
        # Gets all combinations of labels with repetition
        allPossible = list([p for p in itertools.product(self.possibleLabels, repeat=count)])
        return allPossible


    def generatePossibleLabels(self):
        self.possibleLabels = list(set(map(Label, Label)))


























