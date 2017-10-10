from Sentence import Sentence

class Data:

    def sentencesFromFile(self, filename):

        fh = open(filename, 'r')

        sentences = [Sentence]

        sentences = list(map(lambda sentence : Sentence(sentence), fh.readlines()))

        fh.close()

        return sentences
