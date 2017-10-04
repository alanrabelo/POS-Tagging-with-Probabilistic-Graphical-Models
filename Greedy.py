
import operator

class Greedy:

    def __init__(self):
        self.labels = set()
        self.tags = []
        self.sentences = []
        self.words = dict()


    def loadTrainningData(self, filename):
        fh = open(filename, 'r')
        for line in fh.readlines():
            sentenceSplitted = line.split(' ')
            for wordFromSentence in sentenceSplitted:
                word, label = wordFromSentence.split('_')
                self.labels.add(str(label).replace('\n', ''))
                if word in self.words:
                    probabilitiesDict = self.words[word]
                    if label in probabilitiesDict:
                        probabilitiesDict[label] += 1
                    else:
                        probabilitiesDict[label] = 1
                else:
                    self.words[word] = {label : 1}

        fh.close()


    def classify(self, sentence):

        estimatedSequence = []

        for word in sentence.split(' '):
            if word in self.words:
                probabilites = self.words[word]
                estimatedSequence.append(max(probabilites, key=probabilites.get))
            else:
                estimatedSequence.append('Unknown')
        return estimatedSequence

