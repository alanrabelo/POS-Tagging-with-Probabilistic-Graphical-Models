

class Data:

    def loadTrainningData(self, filename):
        labels = set()
        tags = []
        sentences = []
        words = dict()

        fh = open(filename, 'r')
        for line in fh.readlines():
            sentenceSplitted = line.split(' ')
            for wordFromSentence in sentenceSplitted:
                word, label = wordFromSentence.split('_')
                labels.add(str(label).replace('\n', ''))
                if word in words:
                    probabilitiesDict = words[word]
                    if label in probabilitiesDict:
                        probabilitiesDict[label] += 1
                    else:
                        probabilitiesDict[label] = 1
                else:
                    words[word] = {label : 1}

        fh.close()

        return words
