from Greedy import Greedy
from CRF import CRF
from Features import FeatureFunction
from Enums import Label

# greedy = Greedy()
# greedy.loadTrainningData('Data/macmorpho-train.txt')
# print(greedy.classify("Eu amo minha namorada"))


crf = CRF()
crf.loadData('Data/macmorpho-train.txt')

print(crf.predict('Eu correr rapidamente'))


