import numpy as np
nT = 3
nU = 6
k = 2

nGroups = int(nU / k)
D = np.random.randint(10,size=(nU,nT))

def scramble_P():
    P1 = np.random.permutation(D)
    P = []
    for i in range(0,nU,k):
        group = P1[i:i+k]
        P.append(list(np.median(group,axis=0)))
    return P


loop = 10

for i in range(10):
    P = scramble_P()
    A = np.zeros(shape = (nGroups,nU))
    for it,r in enumerate(P):
        d = [np.linalg.norm(r-dd) for dd in D]
        nn = [index for index, value in sorted(enumerate(d), key=lambda x: x[1])]

        for c in nn:
            if list(A[it]).count(1) < k:
                A[it][c] = 1 
            else:
                break
    print(A)