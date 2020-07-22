"""
@author: George Gunter
@usage: python maximize_a_calib.py a_guess v0_guess T_guess
"""

'''
Note from George:

The goal here should be to take in some parameter set/calibration objective pair and then find
a new set of parameters that optimizes a new sensitivity objective. By the team we're exploring
sensitivity the calibration problem should

'''

import numpy as np
import highway_free_flow as hff
import highway_congested as hc
import time, random, csv, os, sys
# from scipy.optimize import Bounds
# from scipy.optimize import minimize
# from scipy.optimize import NonlinearConstraint
# from scipy.optimize import SR1

#Nfeval = 1 #tracks the number of iterations in optimization routine

#realistic sim
realistic_params = [0.73,1.67]
real_sim = hff.HighwayFreeFlow(realistic_params)
measured_counts = np.array(real_sim.getCountsData())
measured_velocity = np.array(real_sim.getVelocityData())

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

def getSpeedError(params,num_samples_from_end):
    #This is a CALIBRATION objective
    sim = hff.HighwayFreeFlow(params)
    simmed_velocity = np.array(sim.getVelocityData())
    # simmed_speed, measured_speed = adjustSize(simmed_velocity, measured_velocity)
    simmed_speed, measured_speed = selectNumSamples(simmed_velocity, measured_velocity,num_samples_from_end)
    error_speeds = ((simmed_speed - measured_speed)**2).sum()
    print("simmed params: ", params)
    print("simmed speed error: " + str(error_speeds))
    return error_speeds

def getCountsError(params,num_samples_from_end):
    #This is a CALIBRATION objective
    sim = hff.HighwayFreeFlow(params)
    simmed_counts = np.array(sim.getCountsData())
    # simmed_count, measured_count = adjustSize(simmed_counts, measured_counts)
    simmed_count, measured_count = selectNumSamples(simmed_counts, measured_counts,num_samples_from_end)
    error_counts = ((simmed_count - measured_count)**2).sum()
    print("simmed params: ", params)
    print("simmed counts error: " + str(error_counts))
    return error_counts



upper_bounds = [3.0,3.0]
lower_bounds = [0.1,0.1]
# bounds = Bounds(lower_bounds,upper_bounds) #No params should be negative

# def getErrorDifference(params):
#     new_sim_error = getSpeedError(params)
#     error_diff = (new_sim_error - best_error)**2
#     print("error difference: " + str(error_diff))
#     return error_diff

# def getSpeedErrorPercentage(params):
#     #This is a SENSITIVITY constraint
#     new_sim_error = getSpeedError(params)
#     error_diff = new_sim_error - best_error
#     if error_diff  == 0:
#         percent_error = 0
#     else:
#         percent_error = error_diff/new_sim_error
#     print("error percetange: " + str(100*percent_error) + " %")
#     return percent_error

#setting up the error constraints
# error_constraint = NonlinearConstraint(getErrorDifference,0,max_error_diff)

#sensitivity obj func
# def objective(params):
#     #This is a SENSITIVITY objective
#     a = params[0]
#     b = params[1]
#     print("value of \"a\" parameter: ", a)
#     print("value of \"b\" parameter: ", b)
#     return -a-b

def sweep_params(num_samples=10,error_metric='Counts',num_samples_from_end=4):
    '''Gets the error values for a range of a and b values spanning the entire bounds'''
    a_range = np.linspace(lower_bounds[0],upper_bounds[0],num_samples)
    b_range = np.linspace(lower_bounds[1],upper_bounds[1],num_samples)

    a_range = list(a_range)
    b_range = list(b_range)

    error_vals = []

    print('Starting Parameter Sweep')

    for a in a_range:
        for b in b_range:
            if(error_metric == 'Counts'):
                error = getCountsError([a,b],num_samples_from_end)
                error_vals.append([a,b,error])
                print('a: '+str(a)+' b: '+str(b)+' Count Error: '+str(error))

            else:
                error = getSpeedError([a,b],num_samples_from_end)
                error_vals.append([a,b,error])
                print('a: '+str(a)+' b: '+str(b)+' Speed Error: '+str(error))

    error_vals = np.array(error_vals)

    return error_vals

error_vals = sweep_params(num_samples=10)

np.savetxt('parameter_sweep.csv',error_vals)










