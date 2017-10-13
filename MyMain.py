from HMM import HMM



hmm = HMM()

hmm.loadTrainningData('Data/macmorpho-train.txt')

while True:
    str = input("Digite a frase a ser classificada:\n")

    if str == 'q':
        break
    result = hmm.classify(str, 3)

    phrase = str.split(' ')
    print()
    for i,word in enumerate(phrase):
        label = result[0][i].value[0]
        print(word + " -> " + label)

    print()