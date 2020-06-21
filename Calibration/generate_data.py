"""
author: Sadman Ahmed Shanto
usage: p3 generate_data.py num_of_sims csvFileName.csv regime
"""
import random
import csv
import sys
import numpy as np

#default params
defaultIDM = [1,1.5,0,30,1,4,2] #a,b,noise,v0,T,delta,s0, experiment_number=0 (default)
defaultIDM_congestedWaves = [1.3, 2.0, 0.1, 30.0,1.0,4.0,2.0]
defaultIDM_congestedNoWaves = [2.3, 2.0, 0.1, 30.0,1.0,4.0,2.0]
defaultCF = [2.6,4.5,0.5,1.0,2.5,30,1.0,0.1,0.5] # accel, decel, sigma, tau, minGap, maxSpeed, speedFactor, speedDev, impatience 
#defaultEnv = [] #maxAcc, maxDec, targetVelocity
#defaultNet = []
#defaultSUMO = []
defaultParams = [defaultIDM, defaultCF]

def changeIDMparam(index):
  #  IDMParamSet = defaultIDM[:]  #for default free flow regime  
  #  IDMParamSet = defaultIDM_congestedWaves[:]  #for default congested waves regime
    IDMParamSet = defaultIDM_congestedNoWaves[:]  #for default congested no waves regime
    if index == 0: #a
        IDMParamSet[index] = random.uniform(1,4)
    elif index == 1: #b
        IDMParamSet[index] = random.uniform(1,5)
    elif index == 2:  #noise
        IDMParamSet[index] = random.uniform(0,2)
    elif index == 3:  #v0
        IDMParamSet[index] = random.uniform(20,50)
    elif index == 4:  #T
        IDMParamSet[index] = random.uniform(1,3)
    elif index == 5:  #delta
        IDMParamSet[index] = random.uniform(2,6)
    elif index == 6:  #s0
        IDMParamSet[index] = random.uniform(1,5)
    return IDMParamSet

#function to generate IDM params
def IDMparams(isRandom, a, b, noise, v0, T, delta, s0):
    if (not isRandom): #determined
        return [a,b,noise,v0,T,delta,s0]
    else: #random
        return [random.uniform(a[0],a[1]), random.uniform(b[0],b[1]),
                random.uniform(noise[0],noise[1]),
                random.uniform(v0[0],v0[1]), random.uniform(T[0],T[1]),
                random.uniform(delta[0],delta[1]),
                random.uniform(s0[0],s0[1])]

#function to generate CF params
def CFparams(isRandom, accel, decel, sigma, tau, minGap, maxSpeed, speedFactor, speedDev, impatience):
    if (not isRandom): #determined
        return [isRandom, accel, decel, sigma, tau, minGap, maxSpeed,
                speedFactor, speedDev, impatience]
    else: #random
        return [random.uniform(accel[0],accel[1]), random.uniform(decel[0],decel[1]),
                random.uniform(sigma[0],sigma[1]),
                random.uniform(tau[0],tau[1]), random.uniform(minGap[0],minGap[1]),
                random.uniform(maxSpeed[0],maxSpeed[1]),
                random.uniform(speedFactor[0],speedFactor[1]),
                random.uniform(speedDev[0],speedDev[1]),
                random.uniform(impatience[0],impatience[1])]
"""
                                    << NOT NEEDED FOR NOW  >>

#function to generate Envparams
def Envparams(isRandom, maxAcc, maxDec, tV):
    if (not isRandom): #determined
        return [maxAcc, maxDec, tV]
    else: #random
        return [random.uniform(maxAcc[0],maxAcc[1]),
                random.uniform(maxDec[0],maxDec[1]),
                random.uniform(tV[0],tV[1])]

#function to generate Net params
def Netparams(isRandom, length, lanes, sl, edges):
    if (not isRandom): #determined
        return [length, lanes, sl, edges]
    else: #random
        return [random.uniform(length[0],length[1]),
                random.uniform(lanes[0],lanes[1]),
                random.uniform(sl[0],sl[1]),
                random.uniform(edges[0],edges[1])]

#function to generate SUMO params
def SUMOparams(isRandom, sstep, lres, srad):
    if (not isRandom): #determined
        return [sstep, lres, srad]
    else: #random
        return [random.uniform(sstep[0],sstep[1]),
                random.uniform(lres[0],lres[1]),
                random.uniform(srad[0],srad[1])]
                                << NOT NEEDED FOR NOW  >>
"""

#function to generate params vector 
def getParams(isRandom, a, b, noise, v0, T, delta, s0, accel, decel, sigma, tau, minGap, maxSpeed, speedFactor, speedDev, impatience, numExp):
    idmParams = IDMparams(isRandom, a, b, noise, v0, T, delta, s0)
    cfParams = CFparams(isRandom, accel, decel, sigma, tau, minGap, maxSpeed, speedFactor, speedDev, impatience)
    return [idmParams+cfParams+[numExp]]

def getIDMParams(isRandom, a, b, noise, v0, T, delta, s0):
    idmParams = IDMparams(isRandom, a, b, noise, v0, T, delta, s0)
    return [idmParams]

#function to write into csv
def createInput(numExp):
    with open( sys.argv[2], 'w', newline='') as file:
        writer = csv.writer(file)
        for i in range(numExp):
            inputParams = getParams(True, (1,4), (1,5), (0,2), (20,50), (1,3), (2,6), (1,5), (1,4), (1,5), (0,1), (1,3), (2,4), (50,50), (1.0,1.0), (0.1,0.1), (0,1), i+1)
            writer.writerows(inputParams)

#function to write into csv
def createIDMInputRandomly(numExp):
    with open( sys.argv[2], 'a', newline='') as file:
        writer = csv.writer(file)
     #   print([defaultIDM])
     #   writer.writerows([defaultIDM])
        for i in range(numExp):
            inputParams = getIDMParams(True, (1,4), (1,5), (0,2), (20,50), (1,3), (2,6), (1,5))
      #      print(inputParams)
            writer.writerows(inputParams)


def createIDMInputOneParameterRandomly(index, numExp):
    with open(sys.argv[2], 'a', newline='') as file:
        writer = csv.writer(file)
     #   print([defaultIDM])
        for i in range(numExp):
            inputParams = changeIDMparam(index)
         #   print(inputParams)
            writer.writerows([inputParams])

def createIDMInputDefault():
    with open( sys.argv[2], 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows([defaultIDM])

def createIDMCongestedWavesInputDefault():
    with open( sys.argv[2], 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows([defaultIDM_congestedWaves])

def createIDMCongestedNoWavesInputDefault():
    with open( sys.argv[2], 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows([defaultIDM_congestedNoWaves])

def createIDMInputParameterUniformly(index,num, defaulData):
    with open( sys.argv[2], 'a', newline='') as file:
        writer = csv.writer(file)
        IDMParamSet = defaulData[:]
        if index == 0: #a
            options = list(np.linspace(1,5,num))
            while len(options)!=0:
                IDMParamSet[index] = options.pop(0)
                writer.writerows([IDMParamSet])
        elif index == 1: #b
            options = list(np.linspace(1,5,num))
            while len(options)!=0:
                IDMParamSet[index] = options.pop(0)
                writer.writerows([IDMParamSet])
        elif index == 2:  #noise
            options = list(np.linspace(0,2,num))
            while len(options)!=0:
                IDMParamSet[index] = options.pop(0)
                writer.writerows([IDMParamSet])
        elif index == 3:  #v0
            options = list(np.linspace(15,30,num))
            while len(options)!=0:
                IDMParamSet[index] = options.pop(0)
                writer.writerows([IDMParamSet])
        elif index == 4:  #T
            options = list(np.linspace(1,4,num))
            while len(options)!=0:
                IDMParamSet[index] = options.pop(0)
                writer.writerows([IDMParamSet])
        elif index == 5:  #delta
            options = list(np.linspace(2,6,num))
            while len(options)!=0:
                IDMParamSet[index] = options.pop(0)
                writer.writerows([IDMParamSet])
        elif index == 6:  #s0
            options = list(np.linspace(1,5,num))
            while len(options)!=0:
                IDMParamSet[index] = options.pop(0)
                writer.writerows([IDMParamSet])
        return IDMParamSet

#main
def main_og():
    num = int(sys.argv[1])
    #createIDMInputDefault()
    createIDMCongestedNoWavesInputDefault()
    for i in range(len(defaultIDM)):
        createIDMInputOneParameterRandomly(i,num)
    createIDMInputRandomly(1)

def main_uni():
    num = int(sys.argv[1])
    regime = str(sys.argv[3])
    if regime=="free":
        createIDMInputDefault()
        for i in range(len(defaultIDM)):
            createIDMInputParameterUniformly(i,num,defaultIDM)
        createIDMInputRandomly(1)
    elif regime=="congestedWaves":
        createIDMCongestedWavesInputDefault()
        for i in range(len(defaultIDM)):
            createIDMInputParameterUniformly(i,num,defaultIDM_congestedWaves)
        createIDMInputRandomly(1)
    elif regime=="congestedNoWaves":
        createIDMCongestedNoWavesInputDefault()
        for i in range(len(defaultIDM)):
            createIDMInputParameterUniformly(i,num,defaultIDM_congestedNoWaves)
        createIDMInputRandomly(1)

main_uni()
