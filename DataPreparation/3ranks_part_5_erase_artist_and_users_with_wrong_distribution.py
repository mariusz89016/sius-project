__author__ = 'Olek'

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SpareFile = 'Data/sparseData.txt'
artistOrderFile = 'Data/artistOrder.txt'

#out
artistToIDFile = "Data/artistToID3ranks.npy"
finalDataFile = 'Data/finalData3ranks.txt'

eraseArtist = {}

minEachRank = 25
# def GimmeRank(number):
#     max1 = 0.0034
#     max2 = 0.008
#     max3 = 0.026
#
#     if 0 <= number < max1:
#         return 1
#     elif max1 <= number < max2:
#         return 2
#     elif max2 <= number < max3:
#         return 3
#     elif max3 <= number :
#         return 4

def GimmeRank(number):
    max1 = 3
    max2 = 10

    if 0 <= number < max1:
        return 1
    elif max1 <= number < max2:
        return 2
    elif max2 <= number:
        return 3


    # if 0 <= number < max1:
    #     return 1
    # elif max1 <= number < max2:
    #     return 2
    # elif max2 <= number < max3:
    #     return 3
    # elif max3 <= number :
    #     return 4

artistRanks = {}

def makeGraph(name):
    global artistRanks
    oceny = []
    for a in artistRanks.keys():
        ocena = [int(artistRanks[a][i]) for i in range(4)]
        oceny.append(ocena)

    noceny = np.array(oceny)
    means = [np.mean(noceny[:,i]) for i in range(4)]
    stds = [np.std(noceny[:,i]) for i in range(4)]

    # print(noceny)
    # print(noceny[:,0])

    o0 = noceny[:,0]
    o1 = noceny[:,1]
    o2 = noceny[:,2]
    # o3 = noceny[:,3]

    # print([np.count_nonzero(noceny[:,i]) for i in range(4)])
    print(len(o0[o0 >= minEachRank]), "/", np.count_nonzero(o0))

    print(len(o1[o1 >= minEachRank]), "/", np.count_nonzero(o1))

    print(len(o2[o2 >= minEachRank]), "/", np.count_nonzero(o2))

    # print(len(o3[o3 >= minEachRank]), "/", np.count_nonzero(o3))

    # print(means)

    # plt.figure()
    # plt.errorbar([1,2,3,4], means, yerr=stds, fmt='o')
    # plt.xlim(0,5)
    # plt.savefig(name + "Deviation")
    # plt.clf()

    counter = 0
    counter2 = 0
    for o in oceny:
        suma = sum(o)
        if o[0] >= minEachRank and o[1] >= minEachRank and o[2] >= minEachRank:# and o[3] >= minEachRank:
            counter += 1
        counter2 += 1
        p = [o[i] for i in range(4)]
        # plt.scatter([1,2,3,4], p)

    # plt.savefig(name)
    # plt.clf()

    print(counter)
    print(counter2)

users = {}
sumy = []
with open(SpareFile, encoding="utf-8") as spareFile:
    for line in spareFile:
        sline = line.replace("\n", "").split("\t")

        user = sline[0]
        userPlaySum = int(sline[1])

        numbers = [int(i) for i in sline[3:][::2]]
        artists = [i for i in sline[2:-1][::2]]

        userPlaySum = sum(numbers)
        sumy.append(userPlaySum)

        if userPlaySum <= 100 or len(numbers) <= 5:
            continue

        zipedResult = zip(artists, numbers)
        users[user] = [(artist, GimmeRank(number)) for (artist, number) in zipedResult]

print(len(users.keys()))
# print(np.mean(sumy))

for user in users.keys():
    for (artist, rank) in users[user]:
        if artist not in artistRanks:
            artistRanks[artist] = [0 for _ in range(4)]
        artistRanks[artist][rank-1] += 1

makeGraph("Graphs/beforeErase")
for xxx in range(4):
    for a in artistRanks.keys():
        o = [int(artistRanks[a][i]) for i in range(4)]

        if not (o[0] >= minEachRank and o[1] >= minEachRank and o[2] >= minEachRank):
            eraseArtist[a] = 1


    artistRanks = {}

    lens = []
    ac = 0
    c = 0

    for user in list(users.keys()):
        users[user] = [(artist, number) for (artist, number) in users[user] if artist not in eraseArtist]
        lens += [len(users[user])]

        if(len(users[user]) <= 20):
            del users[user]
        else:
            for (artist, rank) in users[user]:
                if artist not in artistRanks:
                    artistRanks[artist] = [0 for _ in range(4)]
                artistRanks[artist][rank-1] += 1

    # print(lens)
    # print(np.mean(lens))
    # print(np.std(lens))


    makeGraph("Graphs/afterErase")

print(len(users.keys()))
# exit(0)

artistToID = {}
counter = 0
with open(artistOrderFile, encoding="utf-8") as i:
    for line in i:
        if line.replace("\n","") not in eraseArtist:
            artistToID[line.replace("\n","")] = counter
            counter += 1

np.save(artistToIDFile, artistToID)

with open(finalDataFile, "w+", encoding="utf-8") as out:
    for user in list(users.keys()):
        for (artist, rank) in users[user]:
            out.write(str(artistToID[artist])+" "+str(rank)+" ")
        out.write("\n")