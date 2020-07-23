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
        plotHisto(info[key],params[i])
        #plotGraph(info[key], params[i])
        i+=1

