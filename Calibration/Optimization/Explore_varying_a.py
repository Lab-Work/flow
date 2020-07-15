import numpy as np
# import highway_free_flow as hff
import highway_congested as hc
import time, random, csv, os, sys


b_val = 1.67

real_params = [0.3,b_val]
real_results = hc.HighwayCongested(wave_params=real_params)
original_count = np.array(real_results.getCountsData())
original_speed = np.array(real_results.getVelocityData())


a_range = [.2,3.0]

num_a_samples = 15

num_per_param_samples = 1

a_vals = np.linspace(a_range[0],a_range[1],num_samples)

a_vals = list(a_vals)

counts = []
speeds = []

num_samples_from_end = 15

for a in a_vals:
	print('a value: '+str(a))
	sim_params = [a,b_val]
	sim_results = hc.HighwayCongested(wave_params=sim_params)
	sim_counts = np.array(sim_results.getCountsData())
	sim_speeds = np.array(sim_results.getVelocityData())

	counts.append(sim_counts[-num_samples_from_end:])
	speeds.append(sim_speeds[-num_samples_from_end:]) 

counts = np.array(counts)
speeds = np.array(speeds)

np.savetxt('varying_a_counts.csv',counts)
np.savetxt('varying_a_speeds.csv',speeds)
np.savetxt('varying_a_aVals.csv',a_vals)
np.savetxt('varying_a_original_counts.csv',counts)
np.savetxt('varying_a_original_speeds.csv',counts)

print('Sampling finished.')

