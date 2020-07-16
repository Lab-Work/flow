import numpy as np
# import highway_free_flow as hff
import highway_congested as hc
import time, random, csv, os, sys


real_params = [0.3,1.67]

num_sims = 50

counts = []
speeds = []

<<<<<<< HEAD
num_samples_from_end = 45
sim_length =  4500
=======
num_samples_from_end = 15
>>>>>>> 559ca576eb26d3cf2e1eaecae7936754ad6c75ce

for i in range(num_sims):
	#Simulatees many times using the same parameters to examine stochasticity in the model:
	print('Simulation Number: '+str(i))
<<<<<<< HEAD
	real_results = hc.HighwayCongested(wave_params=real_params,sim_length=sim_length)
=======
	real_results = hc.HighwayCongested(wave_params=real_params)
>>>>>>> 559ca576eb26d3cf2e1eaecae7936754ad6c75ce
	real_counts = np.array(real_results.getCountsData())
	real_speeds = np.array(real_results.getVelocityData())

	counts.append(real_counts[-num_samples_from_end:])
	speeds.append(real_speeds[-num_samples_from_end:]) 

counts = np.array(counts)
speeds = np.array(speeds)

np.savetxt('multi_sim_same_params_counts.csv',counts)
np.savetxt('multi_sim_same_params_speeds.csv',speeds)

print('Sampling finished.')

