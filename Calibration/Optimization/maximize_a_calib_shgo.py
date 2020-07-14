"""
@author: Sadman Ahmed Shanto
@usage: python maximize_a_calib.py a_guess v0_guess T_guess
"""

'''
Note from George:

The goal here should be to take in some parameter set/calibration objective pair and then find
a new set of parameters that optimizes a new sensitivity objective. By the team we're exploring
sensitivity the calibration problem should

'''

import numpy as np
import matplotlib.pyplot as plt
import highway_free_flow as hff
import time, random, csv, os, sys
from scipy.optimize import Bounds
from scipy.optimize import minimize
from scipy.optimize import NonlinearConstraint
from scipy.optimize import SR1
from scipy.optimize import shgo

Nfeval = 1 #tracks the number of iterations in optimization routine

#realistic sim
realistic_params = [0.73,1.67]
real_sim = hff.HighwayFreeFlow(realistic_params)
measured_counts = np.array(real_sim.getCountsData())
measured_velocity = np.array(real_sim.getVelocityData())

#Should be starting from where ever your current best guess is:
calibrated_params = [0.83,1.57]

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

def adjustSize(sim, real):
    real = list(real)
    sim = list(sim)
    while len(real) > len(sim):
        real.pop()
    while len(sim) > len(real):
        sim.pop()
    return [np.array(sim),np.array(real)]

def setGuessedParams():
    return [float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])]

#a,v0,T
bounds = [(0,np.inf),(0,np.inf)]
# guess = setGuessedParams()

best_error = getSpeedError(calibrated_params) 
print("Initial error: ", best_error)

def getErrorDifference(params):
    new_sim_error = getSpeedError(params)
    error_diff = (new_sim_error - best_error)**2
    print("error difference: " + str(error_diff))
    return error_diff

def getSpeedErrorPercentage(params):
    #This is a SENSITIVITY constraint
    new_sim_error = getSpeedError(params)
    error_diff = new_sim_error - best_error
    if error_diff  == 0:
        percent_error = 0
    else:
        percent_error = error_diff/new_sim_error
    print("error percetange: " + str(100*percent_error) + " %")
    return percent_error

#setting up the error constraints
max_error_diff = 10

def nl_constraint(params):
    return - getErrorDifference(params) + max_error_diff

error_constraint = ({'type': 'ineq', 'fun': nl_constraint})

#sensitivity obj func
def objective(params):
    #This is a SENSITIVITY objective
    a = params[0]
    b = params[1]
 #   print("value of \"a\" parameter: ", a)
 #   print("value of \"b\" parameter: ", b)
    return -a-b

# the following function gets executed when an iteration is complete (using for print outs)
def callbackF(params):
    global Nfeval
    print('Iter: {0:4d}, a: {1: 3.6f}, b: {2: 3.6f}, obj: {3: 3.6f}, error_diff: {4: 3.6f}'.format(Nfeval, params[0], params[1], objective(params), getErrorDifference(params)))
    Nfeval += 1

#calls and starts the optimization routine
sol = shgo(objective, bounds=bounds, constraints=error_constraint, iters=1, callback=callbackF, options={'disp':True}) 
print(sol.x)
print("Other local minima found: ")
print(sol.xl)
print("Corresponding func evals:")
print(sol.funl)
