from HMM import HMM
import time



hmm = HMM()

startLoading = time.time()

hmm.loadTrainningData('Data/macmorpho-train.txt')
endLoading = time.time()
print(str(endLoading - startLoading) + ' seconds to train' )


start = time.time()
result = hmm.classify('Vou ali', 5)
end = time.time()


while True:
    string = input("Digite a frase a ser classificada:\n")

    print(str(end - start) + ' seconds to classify' )


    if string == 'q':
        break
    result = hmm.classify(string, 3)

    phrase = string.split(' ')
    print()
    for i,word in enumerate(phrase):
        label = result[i].value[0]
        print(word + " -> " + label)

    print()