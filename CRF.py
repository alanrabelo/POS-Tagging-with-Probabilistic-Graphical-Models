import numpy.random as random
from Features import Features, FeatureFunction
from Enums import Label

class CRF:

    weigths = []
    alpha = 0.1
    numberOfFeatures = 6

    features = []
    sentences = [[str]]
    lines = [str]
    labels = [[Label]]

    def loadData(self, filename):
        fh = open(filename, 'r')
        sentences = []
        labels = []

        for line in fh.readlines():
            self.lines.append(line)
        fh.close()

        self.sentences = sentences
        self.labels = labels

    def train(self):

        sentence = []
        labelsequence = []
        features = set()
        for line in self.lines:

            sentenceSplitted = line.split(' ')
            for index in range(1, len(sentenceSplitted)):
                word, label = str(sentenceSplitted[index]).replace('\n', '').split('_')
                previousWord, previousLabel = str(sentenceSplitted[index - 1]).split('_')

                sentence.append(previousWord)
                labelsequence.append(previousLabel)

                if index == len(sentenceSplitted) - 1:
                    sentence.append(word)
                    labelsequence.append(label)

                features.add(FeatureFunction(Label[previousLabel.replace('+', '__').replace('-', '_')],
                                             Label[label.replace('+', '__').replace('-', '_')]))

            self.labels.append(labelsequence)

        return features


    def create_feature_functions(self, sentences):

        sentence = []
        labelsequence = []
        features = set()
        print('Started Creating Features')

        for line in self.lines:

            sentenceSplitted = line.split(' ')
            for i in range(1, len(sentenceSplitted)):

                word, label = str(sentenceSplitted[i]).replace('\n', '').split('_')
                previousWord, previousLabel = str(sentenceSplitted[i - 1]).split('_')

                sentence.append(previousWord)
                labelsequence.append(previousLabel)

                feature = FeatureFunction(previousLabel, label)
                features.add(feature)
                # found = False
                # for searchedFeature in features:
                #     if searchedFeature == feature:
                #         searchedFeature.numberOfUses += 1
                #         found = True
                #         break
                # if not found:
                #     features.add(feature)

        print('Finished Creating Features ' + str(len(features)))

        sortedList = sorted(list(features), key=lambda numberOfUses: numberOfUses, reverse=True)
        filtered = filter(lambda x : x.numberOfUses > float(sortedList[0].numberOfUses) / 1000, sortedList)
        return list(filtered)

    def predict(self, sentence : str):
        featuresOBJ = Features()
        best = featuresOBJ.wordToFeatures(sentence, self.create_feature_functions(self.labels), numberOfArranges=1)
        print('best combination based on features ' + str(best))
        self.weigths = [(random.randint(0, 1000)) / 1000 for _ in range(6)]
        print(self.weigths)
        return 'In Construction'



