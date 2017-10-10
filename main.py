from HMM import HMM



hmm = HMM()

hmm.loadTrainningData('Data/macmorpho-train.txt')

result = hmm.classify('Eu amo a Ruana', 5)

print(result)


