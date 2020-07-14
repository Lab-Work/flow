"""
@author: Sadman Ahmed Shanto
references for realistic params and bounds: 
    https://traffic-simulation.de/info/info_IDM.html, 
    https://tigerprints.clemson.edu/cgi/viewcontent.cgi?referer=&httpsredir=1&article=2936&context=all_theses
"""
from scipy.optimize import dual_annealing 
from scipy.optimize import Bounds
import highway_free_flow as hff
import numpy as np
import time, random, csv, os, sys
import matplotlib.pyplot as plt

#realistic_params = [0.73, 1.67, 25, 1.6, 4, 2] # a,b,v0,T,delta, s0
realistic_params = [25, 1.6] # a,b,delta
real_sim = hff.HighwayFreeFlow(realistic_params)
measured_counts = np.array(real_sim.getCountsData())
measured_velocity = np.array(real_sim.getVelocityData())

#objective function
def objective(params):
    sim = hff.HighwayFreeFlow(params)
 #   simmed_counts = np.array(sim.getCountsData())
#    simmed_counts = addError(simmed_counts, True, 3)  #with error
    simmed_velocity = np.array(sim.getVelocityData())
#    simmed_velocity = addError(simmed_velocity, False, 3)  #with error
    simmed_speed, measured_speed = adjustSize(simmed_velocity, measured_velocity)
    error_speeds = ((simmed_speed - measured_speed)**2).sum()
   # error_velocity = ((simmed_velocity - measured_velocity)**2).sum()
    print("simmed params: ", params)
#    print("count error: " + str(error_counts))
    print("speed error: " + str(error_speeds))
 #   print("error: ", str(error_counts + error_velocity))
    saveErrors(error_speeds, params)
    return error_speeds


def adjustSize(sim, real):
    real = list(real)
    sim = list(sim)
    while len(real) > len(sim):
        real.pop()
    while len(sim) > len(real):
        sim.pop()
   # print(len(real))
   # print(len(sim))
    return [np.array(sim),np.array(real)]

#constraints?

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
#bnds = (v0_bounds, T_bounds)
#bnds = (a_bounds, b_bounds, v0_bounds, T_bounds, delta_bounds, s0_bounds)
bnds = list(([0.1,30],[1,3]))

#initial guess
#guess = [ 0.5, 0.5, 20, 1, 1, 0.1] #lower bounds
def setGuessedParams():
    return np.array([float(sys.argv[1]), float(sys.argv[2])])

guess = setGuessedParams()

#optimize
options = {"disp": True, "maxiter": 50} 
sol = dual_annealing(objective, bounds=bnds)

#store the optimized params,counts and speeds
opt_params = sol.x
opt_sim = hff.HighwayFreeFlow(opt_params)
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
plt.savefig("figures/counts_lsf_"+timestr+".png")
plt.show()


#plot average speed data
plt.plot([30*i for i in range(len(opt_velocity))], opt_velocity,"r-" ,label="fit")
plt.plot([30*i for i in range(len(measured_velocity))], measured_velocity, label="real")
plt.legend()
plt.xlabel("Data Taking Period")
plt.ylabel("Speed Data")
plt.title("Calibrating Speed Data (params: " + str(opt_params) + " )")
plt.savefig("figures/velocity_lsf_"+timestr+".png")
plt.show()

