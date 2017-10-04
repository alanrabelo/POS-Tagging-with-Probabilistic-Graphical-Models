from Sentence import Sentence

class Data:

    def sentencesFromFile(self, filename):

        fh = open(filename, 'r')

        sentences = [Sentence]

        sentences = list(map(lambda sentence : Sentence(sentence), fh.readlines()))

        print(sentences[1].labels)

        fh.close()

        return sentences
