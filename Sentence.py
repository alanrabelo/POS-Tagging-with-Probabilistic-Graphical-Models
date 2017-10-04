from Enums import Label

class Sentence:

    def __init__(self, sentence : str):
        self.words = list(map(lambda wordInSentence : wordInSentence.split('_')[0], sentence.split(' ')))
        self.labels = list(map(lambda wordInSentence : wordInSentence.split('_')[1].replace('\n', '').replace('-', '_').replace('+', '__'), sentence.split(' ')))



