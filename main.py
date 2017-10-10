from HMM import HMM



hmm = HMM()

hmm.loadTrainningData('Data/macmorpho-train.txt')

result = hmm.classify('Meu computador está com defeito', 5)

print(result)


