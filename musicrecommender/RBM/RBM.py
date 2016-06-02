from numpy.ma import copy

__author__ = 'Aleksander Surman'

import numpy as np
import threading
# from scipy.special import expit as Sigmoid
Sigmoid = np.vectorize(lambda x: 1.0/(1.0+np.exp(-x)))

# def sigmoid(x):
#     return 1 / (1 + math.exp(-x))

Sigmoid = np.vectorize(lambda x: 1.0/(1.0+np.exp(-x)))

CastGeneratorToArray = lambda x: np.fromiter((x), np.float64)
CastToArray = lambda x: np.array((x), np.float64)

class RBM():
    def __init__(self, M = 17765, K = 5, F = 100, learningRate = 0.1, momentum = 0.9, wDecay = 0.001, vBiasesInitialization = None, updateFrequency = None):
        # Constants
        self.M = M
        self.K = K
        self.F = F
        self.learningRate = np.float64(learningRate)
        self.momentum = np.float64(momentum)
        self.wDecay = np.float64(wDecay)

        # Shared between threads
        self.wDeltaLock = threading.Lock()
        self.wDelta = np.zeros((K, F, M), dtype=np.float64)
        self.wDeltaCounter = np.zeros(M, dtype=np.int)

        self.hBiasesDeltaLock = threading.Lock()
        self.hBiasesDelta = np.zeros((1, F), dtype=np.float64)
        self.hBiasesDeltaCounter = np.zeros((1, F), dtype=np.int)

        self.vBiasesDeltaLock = threading.Lock()
        self.vBiasesDelta = np.zeros((K, M))
        self.vBiasesDeltaCounter = np.zeros(M, dtype=np.int)

        # Globals

        self.wGlobal = np.random.normal(0, 0.01, (K, F, M))             # Weights updating after each mini sets

        #ASK
        # self.vBiasesGlobal = np.log(vBiasesInitialization/(1-vBiasesInitialization))                      # Visible layer biases updating after each mini sets
        # self.vBiasesGlobal = vBiasesInitialization
        self.vBiasesGlobal = np.zeros((K, M), dtype=np.float64)
        self.hBiasesGlobal = np.zeros((1, F), dtype=np.float64)         # Hidden layer biases updating after each mini sets

        self.wMomentumTable = np.zeros((K, F, M), dtype=np.float64)
        self.vBiasesMomentumTable = np.zeros((K, M), dtype=np.float64)
        self.hBiasesMomentumTable = np.zeros((1, F), dtype=np.float64)

        #to make predictions faster
        self.Ranks = np.arange(1, self.K + 1, dtype=np.float64).reshape(self.K,1)

        self.updateFrequency = updateFrequency
        self.wUpdateFrequency = updateFrequency

    def setMomentum(self, momentum):
        self.momentum = momentum

    def computeProbabilityTheHiddenStates(self, v, w):
        # Eq. 2
        expressionInsideTheParentheses = np.vectorize(
            lambda j: self.hBiasesGlobal[0,j] + (np.multiply(v, w[:,j])).sum())
        return Sigmoid(expressionInsideTheParentheses(np.arange(self.F)))

    def computeUpdateTheHiddenStates(self, v, w):
        probabilities = self.computeProbabilityTheHiddenStates(v, w)
        return np.random.binomial(1,probabilities, size=(1,self.F))                   #draw a hidden feature

    def computeUpdateTheVisibleStates(self, vBiases, h, w, artistsNumber):
        # Eq. 1
        product = np.exp(vBiases+np.dot(h,w))
        return (product/product.sum(1)).reshape(self.K,artistsNumber)                #keep calm and pray it work

    def learn(self, visibleInput = None, T = 1):

        gradient = lambda _v, _h: np.multiply(_v, _h.T)  #kron was slower

        (vVector, v) = visibleInput

        w = self.wGlobal[:,:,vVector]
        vBiases = self.vBiasesGlobal[:,vVector]

        h  = self.computeUpdateTheHiddenStates(v, w)

        vCopy = np.copy(v)
        hCopy = np.copy(h)

        positiveGradient = CastToArray([gradient(v[k,:], h) for k in range(self.K)])

        for i in range(T):
            v = self.computeUpdateTheVisibleStates(vBiases, h, w, len(vVector))
            h = self.computeUpdateTheHiddenStates(v, w)

        negativeGradient = CastToArray([gradient(v[k,:], h) for k in range(self.K)])

        with self.wDeltaLock:
            self.wDelta[:,:,vVector] += positiveGradient - negativeGradient
            self.wDeltaCounter[vVector] += 1

        with self.hBiasesDeltaLock:
            self.hBiasesDelta += hCopy - h
            self.hBiasesDeltaCounter += 1

        with self.vBiasesDeltaLock:
            self.vBiasesDelta[:,vVector] += vCopy - v
            self.vBiasesDeltaCounter[vVector] += 1


    def update(self, verbose = False):
        def log(x):
            if verbose:
                print(x)

        #updating weights

        wDeltaWhere = \
            np.where(self.wDeltaCounter >= self.wUpdateFrequency)

        self.wMomentumTable[:,:,wDeltaWhere] = \
            self.momentum * self.wMomentumTable[:,:,wDeltaWhere] + \
            self.learningRate * (self.wDelta[:,:,wDeltaWhere]/self.wDeltaCounter[wDeltaWhere] -
            self.wDecay * self.wGlobal[:,:,wDeltaWhere])

        self.wGlobal[:,:,wDeltaWhere] += self.wMomentumTable[:,:,wDeltaWhere]
        self.wDeltaCounter[wDeltaWhere] = 0
        self.wDelta[:,:,wDeltaWhere] = 0
        log("Updated {0} Weights".format(wDeltaWhere[0].size))

        # updating hidden biases
        self.hBiasesMomentumTable = \
            self.momentum * self.hBiasesMomentumTable + \
            self.learningRate * (self.hBiasesDelta/self.hBiasesDeltaCounter)

        self.hBiasesGlobal += self.hBiasesMomentumTable
        self.hBiasesDeltaCounter[:] = 0
        self.hBiasesDelta[:] = 0
        log("Updated Hidden biases")

        # updating visible biases
        vBiasesWhere = \
            np.where(self.vBiasesDeltaCounter >= self.updateFrequency)

        self.vBiasesMomentumTable[:,vBiasesWhere] = \
            self.momentum * self.vBiasesMomentumTable[:,vBiasesWhere] + \
            self.learningRate * (self.vBiasesDelta[:,vBiasesWhere]/self.vBiasesDeltaCounter[vBiasesWhere])

        self.vBiasesGlobal[:,vBiasesWhere] += self.vBiasesMomentumTable[:,vBiasesWhere]
        self.vBiasesDelta[:,vBiasesWhere] = 0
        self.vBiasesDeltaCounter[vBiasesWhere] = 0
        log("Updated {0} Visible biases".format(vBiasesWhere[0].size))

    def prediction(self, visibleInput = None, isValidation = False):
        if isValidation:
            (vVector, v) = visibleInput
            w = self.wGlobal[:,:,vVector]
            vBiases = self.vBiasesGlobal[:,vVector]

            h = self.computeUpdateTheHiddenStates(v, w)
            v = self.computeUpdateTheVisibleStates(vBiases, h, w, len(vVector))

        else:
            v = visibleInput
            h = self.computeUpdateTheHiddenStates(v, self.wGlobal)
            v = self.computeUpdateTheVisibleStates(self.vBiasesGlobal, h, self.wGlobal, self.M)

        return np.multiply(v, self.Ranks).sum(0)

    def saveRBM(self, config):
        import os
        from time import strftime, localtime
        try:
            if not os.path.isdir("Saves//"):
                os.mkdir("Saves")
            saveDir = "Saves//"
        except OSError:
            saveDir = "" # if error save in . folder
            pass

        fileName = config+strftime("%Y-%m-%d-%H-%M-%S", localtime())

        np.savez(saveDir+fileName,
                 M = self.M,
                 K = self.K,
                 F = self.F,
                 learningRate = self.learningRate,
                 momentum = self.momentum,
                 wDecay = self.wDecay,

                 wDelta = self.wDelta,
                 hBiasesDelta = self.hBiasesDelta,
                 vBiasesDelta = self.vBiasesDelta,

                 wDeltaCounter = self.wDeltaCounter,
                 hBiasesDeltaCounter = self.hBiasesDeltaCounter,
                 vBiasesDeltaCounter = self.vBiasesDeltaCounter,

                 wGlobal = self.wGlobal,
                 vBiasesGlobal = self.vBiasesGlobal,
                 hBiasesGlobal = self.hBiasesGlobal,

                 wMomentumTable = self.wMomentumTable,
                 vBiasesMomentumTable = self.vBiasesMomentumTable,
                 hBiasesMomentumTable = self.hBiasesMomentumTable,

                 Ranks = self.Ranks)
        return saveDir+fileName+".npz"


def loadRBM(file):
    RBMFile = np.load(file)
    loadedRBM = RBM()
    loadedRBM.M = RBMFile['M']
    loadedRBM.K = RBMFile['K']
    loadedRBM.F = RBMFile['F']
    loadedRBM.learningRate = RBMFile['learningRate']
    loadedRBM.momentum = RBMFile['momentum']
    loadedRBM.wDecay = RBMFile['wDecay']

    loadedRBM.wDelta = RBMFile['wDelta']
    loadedRBM.hBiasesDelta = RBMFile['hBiasesDelta']
    loadedRBM.vBiasesDelta = RBMFile['vBiasesDelta']

    loadedRBM.wDeltaCounter = RBMFile['wDeltaCounter']
    loadedRBM.hBiasesDeltaCounter = RBMFile['hBiasesDeltaCounter']
    loadedRBM.vBiasesDeltaCounter = RBMFile['vBiasesDeltaCounter']

    loadedRBM.wGlobal = RBMFile['wGlobal']
    loadedRBM.vBiasesGlobal = RBMFile['vBiasesGlobal']
    loadedRBM.hBiasesGlobal = RBMFile['hBiasesGlobal']

    loadedRBM.wMomentumTable = RBMFile['wMomentumTable']
    loadedRBM.vBiasesMomentumTable = RBMFile['vBiasesMomentumTable']
    loadedRBM.hBiasesMomentumTable = RBMFile['hBiasesMomentumTable']

    loadedRBM.Ranks = RBMFile['Ranks']

    loadedRBM.wDeltaLock = threading.Lock()
    loadedRBM.hBiasesDeltaLock = threading.Lock()
    loadedRBM.vBiasesDeltaLock = threading.Lock()
    return loadedRBM

