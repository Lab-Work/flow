"""
@author: Sadman Ahmed Shanto
"""
import csv
import numpy as np
import matplotlib.pyplot as plt

def readData(csvFile):
    data = np.loadtxt(csvFile)
    return data

def plotGraph(data,params):
    xvals = [i for i in range(len(data[0]))]
    for i in range(len(data)):
        plt.plot(xvals, data[i], label="iter = {}".format(i))
    plt.xlabel("Measurement Number")    
    plt.ylabel("Speeds (m/s)")
  #  plt.legend()
    plt.title("[a,b] = {}".format(params))
    plt.show()

def rmse(diff_vector):
    return np.sqrt(np.mean((diff_vector)**2))

def getSpeedErrorVector(sim,real):
    return sim - real

"""

    rmse_vector = []
    fname = open('data/error_vector.csv','ab')
    while num_repeat != 0:
        print("Sim number: ", 6-num_repeat)
        vector = np.array(obj_func(params))
        rmse_vector.append(rmse(vector))
     #   saveErrors(vector, params,fname="error_vector.csv", delim=";")
        np.savetxt(fname, [np.concatenate((params,vector))], delimiter=',',fmt='%2.5f')
        num_repeat-=1

    def getRMSEOfMeanSpeedError(self,rmse_vector):
        mean_rmse = np.mean(rmse_vector)
        print("RMSE vector: {}".format(rmse_vector))
        print("Mean RMSE: {}".format(mean_rmse))
        return mean_rmse

    rmse_vector = []
    total_sims = num_repeat
    while num_repeat != 0:
        print("Sim number: ", 6-num_repeat)
        vector = np.array(obj_func(params))
        rmse_vector.append(vector)
        num_repeat-=1


    def getMeanRMSOfSpeedError(self,rmse_vector):
        rmse_vector = np.array(rmse_vector)
        mean_error_vector = (1.0 /total_sims) * rmse_vector.sum(axis=0)
        mean_rmse = self.rmse(mean_error_vector)
        print("Mean error vector: {}".format(mean_error_vector))
        print("RMSE of mean error vector: {}".format(mean_rmse))
        return mean_rmse

    while num_repeat != 0:
        print("Sim number: ", 6-num_repeat)
        vector1 = np.array(obj_func(params))
        rmse_vector1.append(rmse(vector1))
        rmse_vector2.append(vector1)
        num_repeat-=1
    rmse_vector1 = np.array(rmse_vector1)
    rmse_vector2 = np.array(rmse_vector2)
    mean_error_vector = (1.0 /total_sims) * rmse_vector2.sum(axis=0)
    e1 = np.mean(rmse_vector1)
    e2 = rmse(mean_error_vector)
    error = (e1+e2)/2.0

"""


def sas_error_func(data,params,num_sim):
    real = data[0]
    data = list(data)
    data = [data[i * num_sim:(i + 1) * num_sim] for i in range((len(data) + num_sim - 1) // num_sim )]
    errors = []
    for sims in data:
        rmse_1 = []
        rmse_2 = []
        total_sims = num_sim
        for sim in sims:
            sim = np.array(sim)
            vector = getSpeedErrorVector(sim, real)
            rmse_1.append(rmse(vector))
            rmse_2.append(vector)
        rmse_1 = np.array(rmse_1)
        rmse_2 = np.array(rmse_2)
        mean_error_vector = (1.0 /total_sims) * rmse_2.sum(axis=0)
        e1 = np.mean(rmse_1)
        e2 = rmse(mean_error_vector)
        error = (e1+e2)/2.0
        errors.append(error)
    xvals = [i for i in range(len(errors))]
    mean = np.mean(errors)
    median = np.median(errors)
    plt.plot(xvals,errors)
    plt.ylabel("SAS error func")
    plt.title("[a,b] = {} mean RMSE = {:.3f} median RMSE = {:.3f}".format(params, mean, median))
    plt.show()
    plt.hist(errors, bins='auto')
    plt.title("Histogram with \"auto\" bins and [a,b] = {} ".format(params))
    plt.xlabel("SAS error func")
    plt.ylabel("Frequency")
    plt.show()


def plotRMSE(data,params):
    real = data[0]
    rmse_arr = []
    for i in range(len(data)):
        sim = data[i]
        rmse_arr.append(rmse(sim-real))
    rmse_arr = np.array(rmse_arr)
    mean = np.mean(rmse_arr)
    median = np.median(rmse_arr)
    xvals = [i for i in range(len(rmse_arr))]
    plt.plot(xvals, rmse_arr)
    plt.title("[a,b] = {} mean RMSE = {:.3f} median RMSE = {:.3f}".format(params, mean, median))
    plt.ylabel("RMSE values")
    plt.show()

def plotHisto(data,params):
    real = data[0]
    rmse_arr = []
    for i in range(len(data)):
        sim = data[i]
        rmse_arr.append(rmse(sim-real))
    rmse_arr = np.array(rmse_arr)
    plt.hist(rmse_arr, bins='auto')
    plt.title("Histogram with \"auto\" bins and [a,b] = {} ".format(params))
    plt.xlabel("RMSE values")
    plt.xlabel("Frequency")
    plt.show()


if __name__ == "__main__":
    info = {
        'd0' : readData('data/a-0.5b-1.0.csv'),
        'd1' : readData('data/a-0.5b-1.1.csv'),
        'd2' : readData('data/a-0.5b-1.2.csv'),
        'd3' : readData('data/a-0.5b-1.3.csv'),
        'd4' : readData('data/a-0.5b-1.4.csv')
    }
    params = [[0.5,1.0],[0.5,1.1],[0.5,1.2],[0.5,1.3],[0.5,1.4]]
    i = 0
    for key, value, in info.items():
        sas_error_func(info[key], params[i], 5)
        #plotHisto(info[key],params[i])
        #plotRMSE(info[key],params[i])
        #plotGraph(info[key], params[i])
        i+=1

