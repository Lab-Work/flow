
import numpy as np
# import highway_free_flow as hff
import highway_congested as hc
import time, random, csv, os, sys


b = 1.2

folder_path = '/Users/vanderbilt/Desktop/Research_2020/CIRCLES/Model_Dev/flow/Calibration/Optimization/Error_Sweep/b-1.2/'

sim_length = 3000 #20 minutes
num_samples_from_end = 25 #Doesn't record first 7.5 minutes

num_a_samples = 10

a_vals = np.linspace(.1,2.0,num_a_samples)
a_vals = list(a_vals)

num_sims = 10

speeds = dict.fromkeys(a_vals)


for a in a_vals:
	speeds[a] = []
	sim_params = [a,b]
	print('Simulating: '+str(sim_params))
	for i in range(num_sims):
		print('Simulation Number: '+str(i))

		sim_results = hc.HighwayCongested(wave_params=sim_params,sim_length=sim_length)

		sim_speeds = np.array(sim_results.getVelocityData())

		sim_speeds = sim_speeds[-num_samples_from_end:]

		speeds[a].append(sim_speeds)

	speeds[a] = np.array(speeds[a])
	file_name = folder_path + 'a-' + str(a) + '.csv'
	np.savetxt(file_name,speeds[a])
	print('Value saved: '+str(a))


	





