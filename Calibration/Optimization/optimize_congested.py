"""
@author: Sadman Ahmed Shanto
references for realistic params and bounds: 
    https://traffic-simulation.de/info/info_IDM.html, 
    https://tigerprints.clemson.edu/cgi/viewcontent.cgi?referer=&httpsredir=1&article=2936&context=all_theses
"""
from scipy.optimize import minimize
import highway_congested as hc
import numpy as np
import time, random, csv, os, sys
import matplotlib.pyplot as plt

realistic_params = [0.8]
num_samples_from_end = 15
real_sim = hc.HighwayCongested(wave_params=realistic_params)
measured_counts = np.array(real_sim.getCountsData())
measured_velocity = np.array(real_sim.getVelocityData())
mean_original_speed = np.mean(measured_velocity)
mean_original_count = np.mean(measured_counts)
std_original_speed = np.std(measured_velocity)
std_original_count = np.std(measured_counts)

#function definitions
def adjustSize(sim, real):
    real = list(real)
    sim = list(sim)
    while len(real) > len(sim):
        real.pop()
    while len(sim) > len(real):
        sim.pop()
    return [np.array(sim),np.array(real)]

def selectNumSamples(simmed_measures,real_measures,num_samples_from_end):
    simmed_measures, real_measures = adjustSize(simmed_measures,real_measures)
    simmed_measures_trimmed = simmed_measures[-num_samples_from_end:]
    real_measures_trimmed = real_measures[-num_samples_from_end:]
    return [simmed_measures_trimmed,real_measures_trimmed]

#objective function
def objective(params):
    sim = hc.HighwayCongested(wave_params=params)
    simmed_velocity = np.array(sim.getVelocityData())
    simmed_speed, measured_speed = selectNumSamples(simmed_velocity, measured_velocity, num_samples_from_end)
    error_speeds = ((simmed_speed - measured_speed)**2).sum()
    print("simmed wave params [a,b]: {} {}".format(sim.a, sim.b))
    print("simmed other params [v0, T, delta, s0] : {} {} {} {} ".format(sim.v0, sim.T, sim.delta, sim.s0))
    print("speed error: " + str(error_speeds))
    saveErrors(error_speeds, params)
    sim.destroyCSV()
    return error_speeds

def mean_objective(params):
    sim = hc.HighwayCongested(wave_params=params)
    simmed_mean_speed = sim.getMeanSpeed()
    error = abs(simmed_mean_speed - mean_original_speed)
    print("error: ", error)
    saveErrors(error, params)
    sim.destroyCSV()
    return error

def lambda_objective(params,lamda=0.25):
    sim = hc.HighwayCongested(wave_params=params)
    simmed_mean_speed = sim.getMeanSpeed()
    simmed_std_speed = sim.getStdSpeed()
    error = (1-lamda)*abs(simmed_mean_speed - mean_original_speed) + lamda*abs(simmed_std_speed-std_original_speed)
    print("error: ", error)
    saveErrors(error, params)
    sim.destroyCSV()
    return error

def addError(vals, isCounts, stdv):
    if isCounts:
        y = np.round(np.random.normal(vals,stdv))
        return np.where(y<0, 0, y)
    else:
        y = np.random.normal(vals,stdv)
        return np.where(y<0, 0, y)

def getSpeedErrorVector(params):
    sim = hc.HighwayCongested(wave_params=params)
    simmed_velocity = np.array(sim.getVelocityData())
    simmed_speed, measured_speed = selectNumSamples(simmed_velocity, measured_velocity, num_samples_from_end)
    error_vector = simmed_speed - measured_speed
    print("\tsimmed wave params [a,b]: {} {}".format(sim.a, sim.b))
    print("\tsimmed other params [v0, T, delta, s0] : {} {} {} {} ".format(sim.v0, sim.T, sim.delta, sim.s0))
    print("\tspeed error vector: " + str(error_vector))
    sim.destroyCSV()
    return error_vector

def rmse(diff_vector):
    return np.sqrt(np.mean((diff_vector)**2))

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

def average_of_multiple_sims_objective(params, obj_func=getSpeedErrorVector,num_repeat=5):
    rmse_vector = []
    fname = open('data/error_vector.csv','ab')
    while num_repeat != 0:
        print("Sim number: ", 6-num_repeat)
        vector = np.array(obj_func(params))
        rmse_vector.append(rmse(vector))
     #   saveErrors(vector, params,fname="error_vector.csv", delim=";")
        np.savetxt(fname, [np.concatenate((params,vector))], delimiter=',',fmt='%2.5f')
        num_repeat-=1
    rmse_vector = np.array(rmse_vector)
    mean_rmse = np.mean(rmse_vector)
    print("RMSE vector: {}".format(rmse_vector))
    print("Mean RMSE: {}".format(mean_rmse))
    fname.close()
    saveErrors(mean_rmse, params, fname="rmse_error.csv", delim=",")
    return mean_rmse

def saveErrors(error, params, fname="error.csv", delim=","):
    with open("data/"+fname, 'a') as f:
        f.write(str(error)+delim+str(params)+"\n")

def rmse_of_mean_error_vector(params,obj_func=getSpeedErrorVector,num_repeat=5):
    rmse_vector = []
    fname = open('data/error_vector_2.csv','ab')
    total_sims = num_repeat
    while num_repeat != 0:
        print("Sim number: ", 6-num_repeat)
        vector = np.array(obj_func(params))
        rmse_vector.append(vector)
     #   saveErrors(vector, params,fname="error_vector.csv", delim=";")
        np.savetxt(fname, [np.concatenate((params,vector))], delimiter=',',fmt='%2.5f')
        num_repeat-=1
    rmse_vector = np.array(rmse_vector)
    mean_error_vector = (1.0 /total_sims) * rmse_vector.sum(axis=0)
    mean_rmse = rmse(mean_error_vector)
    print("Mean error vector: {}".format(mean_error_vector))
    print("RMSE of mean error vector: {}".format(mean_rmse))
    fname.close()
    saveErrors(mean_rmse, params, fname="rmse_mean_error_vector.csv", delim=",")
    return mean_rmse


def joint_rmse_obj(params,obj_func=getSpeedErrorVector,num_repeat=5):
    rmse_vector1 = []
    rmse_vector2 = []
    total_sims = num_repeat
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
    print("RMSE vector: {}".format(rmse_vector1))
    print("Mean RMSE: {}".format(e1))
    print("Mean error vector: {}".format(mean_error_vector))
    print("RMSE of mean error vector: {}".format(e2))
    print("Final error: {}".format(error))
    saveErrors(error, params, fname="joint_rmse_error1.csv", delim=",")
    saveErrors(e1, params, fname="mean_rmse1.csv", delim=",")
    saveErrors(e2, params, fname="rmse_mean1.csv", delim=",")
    return error

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

guess = [1.3]

#optimize
option = {"disp": True, "xatol": 0.01, "fatol": 0.01}  #default values 0.0001
sol = minimize(joint_rmse_obj,guess, method="Nelder-Mead", options=option)

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
