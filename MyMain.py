from HMM import HMM
import time

# Ainda que eu falasse a língua dos anjos e falasse a língua dos homens
# Às vezes no silêncio da noite eu fico imaginando nós dois
# Às vezes no silêncio da noite eu fico imaginando nós dois
# O que sabemos é uma gota, o que ignoramos é um oceano.
# Se eu vi mais longe, foi por estar sobre ombros de gigantes.


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


    phrase = string.replace('.', ' .').replace(',', ' ,').replace('?', ' ?').replace('!', ' !').split(' ')
    print()
    for i,word in enumerate(phrase):
        label = result[i]
        print(word + " -> " + label)

    print()
    print(str(end - start) + ' seconds to classify' )
