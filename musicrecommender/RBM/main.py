
__author__ = 'Aleksander Surman'

import threading
import numpy as np

from time import time
from DataLoader import DataLoader
from RBM import RBM
from configparser import ConfigParser
import sys

def computeRMSE(verbose = False):

    # sharing between thread
    errorsLock = threading.Lock()

    errors = []

    def threadJob(threadNumber, errorsRef, errorsLockRef):
        for _ in range(np.int(setSize/threadsNumber)):
            visibleLayer, erasedIndex, erasedRanks = GetVisiableLayer(threadNumber)
            predictions = rbm.prediction(visibleLayer, isValidation = True) # if isValidation = False take ~ 20 times more
            with errorsLockRef:
                errorsRef += [predictions[erasedIndex] - erasedRanks]

    threads = []
    for j in range(threadsNumber):
        threads.append(threading.Thread(target=threadJob, args=(j, errors, errorsLock, )))
        threads[j].start()

    for j in range(threadsNumber):
        threads[j].join()

    RMSE = np.ma.sqrt(np.ma.power(errors, 2).sum()/len(errors))

    if verbose:
        print("RMSE: {0}".format(RMSE))
    return RMSE

def learnOneEpoch(verbose = False, T=1):
    startTime = time()
    for setNumber in range(numberOfMiniSets):
        dataLoader.StartNewTrainingMiniSet()
        if setNumber + 1 == numberOfMiniSets:           # last case computing with 1 thread to reduce problem with division data onto many threads
            startTime = time()

            for _ in range(dataLoader.trainingSetSize - (setNumber + 1) * (threadsNumber * batchSizeForOneThread)):
                rbm.learn(dataLoader.GiveVisibleLayerForTraining(0), T)

            rbm.update(verbose=verbose)

            endTime = time()

            if verbose:
                print("Finish last mini set no: {0} \nTook: {1:0.5f} sec".format(setNumber, endTime - startTime))
        else:
            startTime = time()

            def threadJob(threadNumber):
                for _ in range(batchSizeForOneThread):
                    rbm.learn(dataLoader.GiveVisibleLayerForTraining(threadNumber), T)

            threads = []
            for j in range(threadsNumber):
                threads.append(threading.Thread(target=threadJob, args=(j, )))
                threads[j].start()

            for j in range(threadsNumber):
                threads[j].join()

            rbm.update(verbose=verbose) # updating after one mini set

            endTime = time()

            if verbose:
                print("Finish mini set no: {0} \nTook: {1:0.5f} sec".format(setNumber, endTime - startTime))
        sys.stdout.flush()

    endTime = time()
    if verbose:
        print("Epoch took: {0:0.5f} sec".format(endTime - startTime))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("run: python main.py config file")
        exit(-1)
    np.random.seed(666)

    #configuration
    Config = ConfigParser()
    Config.read("Configs/"+sys.argv[1])
    threadsNumber = Config.getint("RBM", "threadsNumber")
    batchSizeForOneThread = Config.getint("RBM", "batchSizeForOneThread")
    M = Config.getint("RBM", "artistsNumber")
    K = Config.getint("RBM", "ranksNumber")
    F = Config.getint("RBM", "hiddenLayerSize")
    learningRate = Config.getfloat("RBM", "learningRate")
    wDecay = Config.getfloat("RBM", "wDecay")
    updateFrequencyMAX = Config.getint("RBM", "updateFrequencyMin")
    numberOfEpoch = Config.getint("RBM", "numberOfEpoch")
    Verbose = Config.getboolean("RBM", "Verbose")

    TrainingSetFile = Config.get("RBM", "trainingSetFile")
    ValidationSetFile = Config.get("RBM", "validationSetFile")
    ValidationFromTrainingSetFile = Config.get("RBM", "validationFromTrainingSetFile")
    TestSetFile = Config.get("RBM", "testSetFile")

    dataLoader = DataLoader(trainingSetFile = TrainingSetFile, validationSetFile = ValidationSetFile, validationFromTrainingSetFile = ValidationFromTrainingSetFile, testSetFile = TestSetFile, K = K, M = M, batchSizeForOneThread = batchSizeForOneThread, threadsNumber = threadsNumber, verbose = Verbose)

    whereUpdateMax = np.where(dataLoader.updateFrequency > updateFrequencyMAX)
    dataLoader.updateFrequency[whereUpdateMax] = updateFrequencyMAX

    dataLoader.vBiasesInitialization[np.where(dataLoader.vBiasesInitialization < np.float64(0.1e-100))] = np.float64(0.1e-100)

    momentum = 0.5

    rbm = RBM(M, K, F, learningRate, momentum, wDecay, dataLoader.vBiasesInitialization, dataLoader.updateFrequency)
    numberOfMiniSets = np.int(np.ma.floor(dataLoader.trainingSetSize / (threadsNumber * batchSizeForOneThread)))


    with open("Outs/"+sys.argv[1]+"_validation_RMSE.txt", "a") as rmsesFile:
        dataLoader.StartNewValidationSet()
        GetVisiableLayer = dataLoader.GiveVisibleLayerForValidation
        setSize = dataLoader.validationSetSize
        rmsesFile.write("Epoch {0}, RMSE {1}\n".format(0, computeRMSE(verbose=Verbose)))
        rmsesFile.flush()
    with open("Outs/"+sys.argv[1]+"_training_RMSE.txt", "a") as rmsesFile:
        dataLoader.StartNewValidationFromTrainingSet()
        GetVisiableLayer = dataLoader.GiveVisibleLayerForValidationFromTraining
        setSize = dataLoader.validationFromTrainingSetSize
        rmsesFile.write("Epoch {0}, RMSE {1}\n".format(0, computeRMSE(verbose=Verbose)))
        rmsesFile.flush()

    for i in range(numberOfEpoch):
        if 6 <= i <= 10:
            rbm.setMomentum(0.8)
        if 11 <= i:
            rbm.setMomentum(0.9)

        dataLoader.StartNewEpoch()
        if i >=40:
            learnOneEpoch(verbose=Verbose, T=5)
        elif i >=20:
            learnOneEpoch(verbose=Verbose, T=3)
        else:
            learnOneEpoch(verbose=Verbose, T=1)

        with open("Outs/"+sys.argv[1]+"_validation_RMSE.txt", "a") as rmsesFile:
            dataLoader.StartNewValidationSet()
            GetVisiableLayer = dataLoader.GiveVisibleLayerForValidation
            setSize = dataLoader.validationSetSize
            rmsesFile.write("Epoch {0}, RMSE {1}\n".format(i+1, computeRMSE(verbose=Verbose)))
            rmsesFile.flush()
        with open("Outs/"+sys.argv[1]+"_training_RMSE.txt", "a") as rmsesFile:
            dataLoader.StartNewValidationFromTrainingSet()
            GetVisiableLayer = dataLoader.GiveVisibleLayerForValidationFromTraining
            setSize = dataLoader.validationFromTrainingSetSize
            rmsesFile.write("Epoch {0}, RMSE {1}\n".format(i+1, computeRMSE(verbose=Verbose)))
            rmsesFile.flush()
    rbm.saveRBM(sys.argv[1])
    sys.stdout.flush()

