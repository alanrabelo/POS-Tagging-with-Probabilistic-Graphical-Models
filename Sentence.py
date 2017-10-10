from Enums import Label

class Sentence:

    def __init__(self, sentence : str):
        self.words = list(map(lambda wordInSentence : wordInSentence.split('_')[0], sentence.split(' ')))
        self.labels = list(map(lambda wordInSentence : wordInSentence.split('_')[1].replace('\n', '').replace('-', '_').replace('+', '__'), sentence.split(' ')))

        for index,label in enumerate(self.labels):

                if label.startswith('PREP'):
                    self.labels[index] = Label['PREP']
                    continue
                if label.startswith('PRO') or label.startswith('PDEN'):
                    self.labels[index] = Label['PRO']
                    continue
                if label.startswith('K'):
                    self.labels[index] = Label['K']
                    continue
                if label.startswith('N'):
                    self.labels[index] = Label['N']
                    continue
                if label.startswith('ADV'):
                    self.labels[index] = Label['ADV']
                    continue

                self.labels[index] = Label[label]


