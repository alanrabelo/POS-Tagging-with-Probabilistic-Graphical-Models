
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

        sentence = str(sentence).lower()

        print('Started Classification Task')


        splittedSentence = sentence.replace('.', ' .').replace(',', ' ,').lower().split(' ')


        possibleLabelsBest = []

        for word in splittedSentence:

            labelsForWord = []

            for label in self.possibleLabels:
                if word in self.words[label.value[0]]:
                    if self.words[label.value[0]][word] > 0:
                        labelsForWord.append(label.value[0])

            if len(labelsForWord) == 0:
                possibleLabelsBest.append(self.generatePossibleLabelsAsString())
            else:
                possibleLabelsBest.append(labelsForWord)
        print(possibleLabelsBest)



        possibleArranges = self.possibleArrangesForArray(possibleLabelsBest)

        probabilityOfArrange = []

        viterbyDict = dict()

        for index,arrange in enumerate(possibleArranges):
            produtOfProbabilites = 1
            for index, word in enumerate(splittedSentence):
                if index >= len(arrange):
                    continue
                currentLabel = arrange[index]
                previousLabel = 'EMPTY' if index == 0 else arrange[index-1]

                # Verify dictionary for previous occurrencies
                tupleForCurrentiteration = (previousLabel,currentLabel,word)
                if tupleForCurrentiteration in viterbyDict:
                    produtOfProbabilites *= viterbyDict[tupleForCurrentiteration]
                    continue

                if word not in self.words[currentLabel]:
                    probabilityOfWord = 0.00000000000001
                else:
                    probabilityOfWord = self.words[currentLabel][word]

                if previousLabel not in self.bigrams or currentLabel not in self.bigrams['EMPTY' if index == 0 else arrange[index-1]]:
                    probabilityOfBigram = 0.000000000000001
                else:
                    probabilityOfBigram = self.bigrams['EMPTY' if index == 0 else previousLabel][currentLabel]

                viterbyDict[(previousLabel, currentLabel, word)] = probabilityOfWord * probabilityOfBigram

                produtOfProbabilites *= probabilityOfWord * probabilityOfBigram

            probabilityOfArrange.append(produtOfProbabilites)

        maxProbability = np.argmax(probabilityOfArrange)

        return possibleArranges[maxProbability]

    def possibleArranges(self, count: int):
        # Gets all combinations of labels with repetition
        allPossible = list([p for p in itertools.product(self.possibleLabels, repeat=count)])
        return allPossible

    def possibleArrangesForArray(self,array : [str]):
        # Gets all combinations of labels with repetition
        allPossible = list(itertools.product(*array))
        print('We must search in ' + str(len(allPossible)) + ' combinations')

        return allPossible


    def generatePossibleLabels(self):
        self.possibleLabels = list(set(map(Label, Label)))

    def generatePossibleLabelsAsString(self):

        labels = []
        for label in list(set(map(Label, Label))):
            labels.append(label.value[0])
        return labels


