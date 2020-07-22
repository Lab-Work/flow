"""
@author: Sadman Ahmed Shanto
todo:
    1) speed
    2) counts
"""
from scipy.optimize import minimize
import highway_congested as hc
import numpy as np
import time, random, csv, os, sys
import matplotlib.pyplot as plt

class ErrorFunctions:

    def __init__(self):
        pass

# main functions
    """
    inputs to non-RMSE getter functions: 
        1) simulated HighwayCongested object
        e.g. sim = hc.HighwayCongested(wave_params=params)
        2) real HighwayCongested object
        e.g. real = hc.HighwayCongested(wave_params=realistic_params)
        3) num_samples_from_end = number of data elements to kept
    """
    def getAbsoluteSquaredSpeedError(self, sim, real, num_samples_from_end):
        simmed_velocity = np.array(sim.getVelocityData())
        measured_velocity = np.array(real.getVelocityData())
        simmed_speed, measured_speed = self.selectNumSamples(simmed_velocity, measured_velocity, num_samples_from_end)
        error = ((simmed_speed - measured_speed)**2).sum()
        self.printErrorStats(sim, error)
        sim.destroyCSV()
        return error

    def getLambdaFunctionMeanStdSpeedError(self,sim,real,lamda=0.25):
        simmed_mean_speed = sim.getMeanSpeed()
        simmed_std_speed = sim.getStdSpeed()
        mean_original_speed = real.getMeanSpeed()
        std_original_speed = real.getStdSpeed()
        error = (1-lamda)*abs(simmed_mean_speed - mean_original_speed) + lamda*abs(simmed_std_speed-std_original_speed)
        self.printErrorStats(sim, error)
        sim.destroyCSV()
        return error

    def getAbsoluteSpeedError(self,sim,real):
        simmed_mean_speed = sim.getMeanSpeed()
        mean_original_speed = real.getMeanSpeed()
        error = abs(simmed_mean_speed - mean_original_speed)
        self.printErrorStats(sim, error)
        sim.destroyCSV()
        return error

    def getSpeedError(self):
        simmed_mean_speed = sim.getMeanSpeed()
        mean_original_speed = real.getMeanSpeed()
        error = simmed_mean_speed - mean_original_speed
        self.printErrorStats(sim, error)
        sim.destroyCSV()
        return error

    """
    inputs to RMSE getter functions: 
        1) simulated HighwayCongested object
        e.g. sim = hc.HighwayCongested(wave_params=params)
        2) real HighwayCongested object
        e.g. real = hc.HighwayCongested(wave_params=realistic_params)
        3) num_samples_from_end = number of data elements to kept
    """

    def getSpeedErrorVector(self,sim, real, num_samples_from_end):
        simmed_velocity = np.array(sim.getVelocityData())
        measured_velocity = np.array(real.getVelocityData())
        simmed_speed, measured_speed = self.selectNumSamples(simmed_velocity, measured_velocity, num_samples_from_end)
        error_vector = simmed_speed - measured_speed
        self.printErrorStats(sim, error_vector, sargs=" vector ")
        sim.destroyCSV()
        return error_vector

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
"""

    def getRMSEOfMeanSpeedError(self,rmse_vector):
        mean_rmse = np.mean(rmse_vector)
        print("RMSE vector: {}".format(rmse_vector))
        print("Mean RMSE: {}".format(mean_rmse))
        return mean_rmse

"""
    rmse_vector = []
    total_sims = num_repeat
    while num_repeat != 0:
        print("Sim number: ", 6-num_repeat)
        vector = np.array(obj_func(params))
        rmse_vector.append(vector)
        num_repeat-=1
"""


    def getMeanRMSOfSpeedError(self,rmse_vector):
        rmse_vector = np.array(rmse_vector)
        mean_error_vector = (1.0 /total_sims) * rmse_vector.sum(axis=0)
        mean_rmse = self.rmse(mean_error_vector)
        print("Mean error vector: {}".format(mean_error_vector))
        print("RMSE of mean error vector: {}".format(mean_rmse))
        return mean_rmse

# helper functions
   def selectNumSamples(self, simmed_measures,real_measures,num_samples_from_end):
        simmed_measures, real_measures = adjustSize(simmed_measures,real_measures)
        simmed_measures_trimmed = simmed_measures[-num_samples_from_end:]
        real_measures_trimmed = real_measures[-num_samples_from_end:]
        return [simmed_measures_trimmed,real_measures_trimmed]

    def printErrorStats(self,sim,error,sargs=" "):
        print("simmed wave params [a,b]: {} {}".format(sim.a, sim.b))
        print("simmed other params [v0, T, delta, s0] : {} {} {} {} ".format(sim.v0, sim.T, sim.delta, sim.s0))
        print("speed error" + str(sargs) + ": " + str(error))

    def adjustSize(self, sim, real):
        real = list(real)
        sim = list(sim)
        while len(real) > len(sim):
            real.pop()
        while len(sim) > len(real):
            sim.pop()
        return [np.array(sim),np.array(real)]

    

    def addError(self,vals, isCounts, stdv):
        if isCounts:
            y = np.round(np.random.normal(vals,stdv))
            return np.where(y<0, 0, y)
        else:
            y = np.random.normal(vals,stdv)
            return np.where(y<0, 0, y)

    def rmse(self, diff_vector):
        return np.sqrt(np.mean((diff_vector)**2))


#realistic_params = [0.73, 1.67, 25, 1.6, 4, 2] # a,b,v0,T,delta, s0
realistic_params = [1.3] # a,b
num_samples_from_end = 15
real_sim = hc.HighwayCongested(wave_params=realistic_params)
measured_counts = np.array(real_sim.getCountsData())
measured_velocity = np.array(real_sim.getVelocityData())
mean_original_speed = np.mean(measured_velocity)
mean_original_count = np.mean(measured_counts)
std_original_speed = np.std(measured_velocity)
std_original_count = np.std(measured_counts)


def multiple_sim_mean_std(params, obj_func=lambda_objective,num_repeat=5):
    acc_error = []
 #   fname = open('data/lamda_error_vector.csv','ab')
    while num_repeat != 0:
        print("Sim number: ", 6-num_repeat)
        err = obj_func(params)
        acc_error.append(err)
    #    np.savetxt(fname, [np.concatenate((params,err))], delimiter=',',fmt='%2.5f')
        num_repeat-=1
    acc_error = np.array(acc_error)
    print("Mean error: {}".format(np.mean(acc_error)))
  #  fname.close()
    saveErrors(np.mean(acc_error), params, fname="lambda_error.csv", delim=",")
    return np.mean(acc_error)



def saveErrors(error, params, fname="error.csv", delim=","):
    with open("data/"+fname, 'a') as f:
        f.write(str(error)+delim+str(params)+"\n")



"""
#bounds
a_bounds = (0.5,2)
b_bounds = (0.5,2)
v0_bounds = (0,30)
T_bounds = (1,3)
delta_bounds = (1,5)
s0_bounds = (0.1,5)
bnds = (a_bounds)

#initial guess
def setGuessedParams():
    return [float(sys.argv[1]), float(sys.argv[2])]

guess = [0.5] 

#optimize
option = {"disp": True, "xatol": 0.01, "fatol": 0.01}  #default values 0.0001
sol = minimize(multiple_sim_mean_std, guess, method="Nelder-Mead", options=option)

#store the optimized params,counts and speeds
opt_params = sol.x
opt_sim = hc.HighwayCongested(wave_params=opt_params)
opt_counts = np.array(opt_sim.getCountsData())
opt_velocity = np.array(opt_sim.getVelocityData())

#time
timestr = time.strftime("%Y%m%d_%H%M%S")

#plot counts data 
plt.plot([30*i for i in range(len(opt_counts))], opt_counts,"r-" ,label="fit")
plt.plot([30*i for i in range(len(measured_counts))], measured_counts, label="real")
plt.legend()
plt.xlabel("Data Taking Period")
plt.ylabel("Counts Data")
plt.title("Calibrating Counts Data (params: " + str(opt_params) + " )")
plt.savefig("figures/counts_"+timestr+".png")
plt.show()

#plot average speed data
plt.plot([30*i for i in range(len(opt_velocity))], opt_velocity,"r-" ,label="fit")
plt.plot([30*i for i in range(len(measured_velocity))], measured_velocity, label="real")
plt.legend()
plt.xlabel("Data Taking Period")
plt.ylabel("Speed Data")
plt.title("Calibrating Speed Data (params: " + str(opt_params) + " )")
plt.savefig("figures/velocity_"+timestr+".png")
plt.show()
"""
