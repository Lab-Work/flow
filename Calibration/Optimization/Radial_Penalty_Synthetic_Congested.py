"""
@author: George Gunter
"""

'''
This script will look to first solve a calibration problem on a synthetic piece of data in the
congested regime then from the best-found point solve a radial penalty analysis on the speed-variance
in order to assess for plausible differences in wave-characteristics.
'''

import numpy as np
import matplotlib.pyplot as plt
import highway_congested as hc
import time, random, csv, os, sys
from scipy.optimize import Bounds
from scipy.optimize import minimize
from scipy.optimize import NonlinearConstraint
from scipy.optimize import SR1

#realistic sim
realistic_params = [0.73, 2.0, 25.0, 4.0, 1.6, 2.0]
down_stream_speed = 10.0
real_sim = hc.HighwayCongested(realistic_params)
measured_counts = np.array(real_sim.getCountsData())
measured_velocity = np.array(real_sim.getVelocityData())

#Should be starting from where ever your current best guess is:
calibrated_params = [0.83,24.5,1.5] # Add a little bit of artificial error

#NOTE: You could plausibly include this as the input you sent from the command line. I think:

# calibrated_params = [float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])]



#function definitions
def getSpeedError(params):
    #This is a CALIBRATION objective
    sim = hff.HighwayFreeFlow(params)
    simmed_velocity = np.array(sim.getVelocityData())
    simmed_speed, measured_speed = adjustSize(simmed_velocity, measured_velocity)
    error_speeds = ((simmed_speed - measured_speed)**2).sum()
    print("simmed params: ", params)
    print("simmed speed error: " + str(error_speeds))
    return error_speeds

def getCountsError(params):
    #This is a CALIBRATION objective
    sim = hff.HighwayFreeFlow(params)
    simmed_counts = np.array(sim.getCountsData())
    simmed_count, measured_count = adjustSize(simmed_counts, measured_counts)
    error_counts = ((simmed_count - measured_count)**2).sum()
    print("simmed params: ", params)
    print("simmed counts error: " + str(error_counts))
    return error_counts

def CalibrationObjective(params):
    return getCountsError(params)

def adjustSize(sim, real):
    real = list(real)
    sim = list(sim)
    while len(real) > len(sim):
        real.pop()
    while len(sim) > len(real):
        sim.pop()
    return [np.array(sim),np.array(real)]

#a,v0,T
bounds = Bounds([0,11,1],[np.inf,30,3]) #No params should be negative
# guess = setGuessedParams()
best_error = getSpeedError(calibrated_params) #instead of guess used calibrated params

print("Initial error: ", best_error)

def getSpeedErrorPercentage(params):
    #This is a SENSITIVITY constraint
    new_sim_error = getSpeedError(params)

    error_diff = new_sim_error - best_error

    if error_diff  == 0:
        percent_error = 0
    else:
        percent_error = error_diff/new_sim_error

    print("error percetange: ", percent_error)

    return percent_error

max_error_diff = 10.0 #This should be 

error_constraint = NonlinearConstraint(getSpeedErrorPercentage,0,error_diff)


#sensitivity obj func
def objective(params):
    #This is a SENSITIVITY objective
    a = params[0]
    print("value of a parameter: ", a)
    print("the new param set is ", params)
    return -a

sol = minimize(objective, guess, method="trust-constr", bounds=bounds, constraints=error_constraint, options={'verbose': 3})
print(sol.x)
