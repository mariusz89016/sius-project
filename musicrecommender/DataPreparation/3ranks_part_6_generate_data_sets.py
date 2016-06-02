__author__ = 'Olek'

import numpy as np
import random

np.random.seed(666)

dataFile = "Data/finalData3ranks.txt"

TrainingSetFile = "DataSets3ranks/TrainingSet"
ValidationSetFile = "DataSets3ranks/ValidationSet"
TestSetFile = "DataSets3ranks/TestSet"
ValidationFromTrainingSetFile = "DataSets3ranks/ValidationFromTrainingSet"

result = []
ValidationSet = []
TrainingSet = []
TestSet = []
ValidationFromTrainingtSet = []

TestSetSize = 40000
ValidationSetSize = 40000


with open(dataFile) as data:
    for line in data:
        artists = [int(z) for z in line.replace("\n","").split(" ")[:-1:2]]
        ranks = [int(z) for z in line.replace("\n","").split(" ")[1::2]]

        result.append((artists, ranks))

indexes = np.arange(len(result))
np.random.shuffle(indexes)

for index in indexes:
    if(len(TestSet) < TestSetSize):
        TestSet.append(result[index])
    elif(len(ValidationSet) < ValidationSetSize):
        ValidationSet.append(result[index])
    else:
        TrainingSet.append(result[index])

for index in np.random.choice(indexes[TestSetSize+ValidationSetSize+1:], len(TrainingSet)/10, replace=False):
    ValidationFromTrainingtSet.append(result[index])


np.save(TrainingSetFile, TrainingSet)
np.save(ValidationSetFile, ValidationSet)
np.save(TestSetFile, TestSet)
np.save(ValidationFromTrainingSetFile, ValidationFromTrainingtSet)


print("TestSet size: ", len(TestSet))
print("ValidationSet size: ", len(ValidationSet))
print("TrainingSet size: ", len(TrainingSet))
print("ValidationFromTrainingtSet size: ", len(ValidationFromTrainingtSet))