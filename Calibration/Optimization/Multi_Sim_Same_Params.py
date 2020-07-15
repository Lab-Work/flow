import numpy as np
# import highway_free_flow as hff
import highway_congested as hc
import time, random, csv, os, sys


real_params = [0.3,1.67]

num_sims = 50

counts = []
speeds = []

num_samples_from_end = 15

for i in range(num_sims):
	#Simulatees many times using the same parameters to examine stochasticity in the model:
	print('Simulation Number: '+str(i))
	real_results = hc.HighwayCongested(wave_params=real_params)
	real_counts = np.array(real_results.getCountsData())
	real_speeds = np.array(real_results.getVelocityData())

	counts.append(real_counts[-num_samples_from_end:])
	speeds.append(real_speeds[-num_samples_from_end:]) 

counts = np.array(counts)
speeds = np.array(speeds)

np.savetxt('multi_sim_same_params_counts.csv',counts)
np.savetxt('multi_sim_same_params_speeds.csv',speeds)

print('Sampling finished.')

