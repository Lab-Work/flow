import numpy as np
# import highway_free_flow as hff
import highway_congested as hc
import time, random, csv, os, sys


real_params = [0.73,1.67]
real_results = hc.HighwayCongested(wave_params=real_params)
real_counts = np.array(real_results.getCountsData())
real_velocity = np.array(real_results.getVelocityData())

real_results_rerun = hc.HighwayCongested(wave_params=real_params)
real_counts_rerun = np.array(real_results_rerun.getCountsData())
real_velocity_rerun = np.array(real_results_rerun.getVelocityData())

simmed_params = [.83,1.57]
simmed_results = hc.HighwayCongested(wave_params=simmed_params)
simmed_counts = np.array(simmed_results.getCountsData())
simmed_velocity = np.array(simmed_results.getVelocityData())

simmed_params_new = [2.0,1.57]
simmed_results_new = hc.HighwayCongested(wave_params=simmed_params_new)
simmed_counts_new = np.array(simmed_results_new.getCountsData())
simmed_velocity_new = np.array(simmed_results_new.getVelocityData())


pt.plot(real_velocity)
pt.plot(real_velocity_rerun)
pt.plot(simmed_velocity)
pt.plot(simmed_velocity_new)
pt.xlabel('Measurement Number')
pt.ylabel('Average Speed [m/s]')
pt.show()


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
    return error_count


