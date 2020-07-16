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
    print("simmed params: ", params)
    print("speed error: " + str(error_speeds))
    saveErrors(error_speeds, params)
    sim.destroyCSV()
    return error_speeds

def mean_objective(params):
    sim = hc.HighwayCongested(wave_params=params)
    simmed_mean_speed = sim.getMeanSpeed()
    return abs(simmed_mean_speed - mean_original_speed)

def lambda_objective(params,lamda=0.25):
    sim = hc.HighwayCongested(wave_params=params)
    simmed_mean_speed = sim.getMeanSpeed()
    simmed_std_speed = sim.getStdSpeed()
    error = (1-lamda)*abs(simmed_mean_speed - mean_original_speed) + lamda*abs(simmed_std_speed-std_original_speed)
    return error

def addError(vals, isCounts, stdv):
    if isCounts:
        y = np.round(np.random.normal(vals,stdv))
        return np.where(y<0, 0, y)
    else:
        y = np.random.normal(vals,stdv)
        return np.where(y<0, 0, y)

def saveErrors(error, params):
    with open('data/error.csv', 'a') as f:
        f.write(str(error)+","+str(params)+"\n")

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
option = {"disp": True} 
sol = minimize(objective, guess, method="Nelder-Mead", options=option)

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
