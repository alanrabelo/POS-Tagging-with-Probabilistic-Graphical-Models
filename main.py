from HMM import HMM



hmm = HMM()

hmm.loadTrainningData('Data/macmorpho-train.txt')

result = hmm.classify('Jogar bola', 5)
result2 = hmm.classify('Jogar bola', 5)

print(result)
print(result2)


