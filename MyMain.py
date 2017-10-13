from HMM import HMM
import time



hmm = HMM()

startLoading = time.time()

hmm.loadTrainningData('Data/macmorpho-train.txt')
endLoading = time.time()
print(str(endLoading - startLoading) + ' seconds to train' )

while True:
    string = input("Digite a frase a ser classificada:\n")

    if string == 'q':
        break

    start = time.time()
    result = hmm.classify(string, 1)
    end = time.time()


    phrase = string.split(' ')
    print()
    for i,word in enumerate(phrase):
        label = result[i]
        print(word + " -> " + label)

    print()
    print(str(end - start) + ' seconds to classify' )
