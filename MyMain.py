from HMM import HMM



hmm = HMM()

hmm.loadTrainningData('Data/macmorpho-train.txt')

result = hmm.classify('vou ali .', 5)

print(result)
