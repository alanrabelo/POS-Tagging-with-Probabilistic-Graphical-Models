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

print(str(end - start) + ' seconds to classify' )

print(result)
