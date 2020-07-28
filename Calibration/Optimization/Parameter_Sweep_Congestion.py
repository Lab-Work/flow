
import numpy as np
# import highway_free_flow as hff
import highway_congested as hc
import time, random, csv, os, sys

import ray



folder_path = '/Users/vanderbilt/Desktop/Research_2020/CIRCLES/Model_Dev/flow/Calibration/Optimization/Param_Sweep/'
existing_files = os.listdir(folder_path)

sim_length = 3000 #20 minutes
num_samples_from_end = 25 #Doesn't record first 7.5 minutes


num_samples = 50


upper_bounds = [1.3,2.0]
lower_bounds = [0.5,1.0]

a_range = np.linspace(lower_bounds[0],upper_bounds[0],9)
b_range = np.linspace(lower_bounds[1],upper_bounds[1],11)

a_range = list(a_range)
b_range = list(b_range)

total_sim_runs = 0

sims_to_run = len(a_range)*len(b_range)*num_samples


ray.init()

print('Starting Parameter Sweep')

def check_for_existing_csv(sim_params):
	#Some results may already exist, don't want to duplicte, so look for existing
	#files and repload the results.
	a=sim_params[0]
	b=sim_params[1]
	speed_vals = []
	file_name  = 'a-'+str(a)+'b-'+str(b)+'.csv'
	if(file_name in existing_files):
		speed_vals = np.loadtxt(folder_path+file_name)
	return speed_vals



@ray.remote
def run_sim(sim_params,num_samples_from_end):
	#Function to return the results of a simulation, should be parallized w/ ray
	sim_results = hc.HighwayCongested(wave_params=sim_params)
	sim_speeds = np.array(sim_results.getVelocityData())
	sim_speeds = sim_speeds[-num_samples_from_end:]
	sim_results.destroyCSV()
	return sim_speeds

def multi_sim_run(sim_params,num_samples_from_end):
	speed_result_ids = []
	for i in range(samples_to_run):
		speed_result_ids.append(run_sim.remote(sim_params,num_samples_from_end))
		
	speed_sim_results = ray.get(speed_result_ids)
	return speed_sim_results

def save_csv(a,b,speed_vals):
	speed_vals = np.array(speed_vals)
	file_name  = 'a-'+str(a)+'b-'+str(b)+'.csv'
	np.savetxt(folder_path+file_name,speed_vals)



for a in a_range:
	for b in b_range:
		
		sim_params = [a,b]


		print('Parameter values: a: '+str(sim_params[0])+' b: '+str(sim_params[1]) + ', simulation number: '+str(total_sim_runs))


		speed_vals = check_for_existing_csv(sim_params)

		num_existing_samples = len(speed_vals)

		total_sim_runs += num_existing_samples

		speed_vals = list(speed_vals)

		samples_to_run = num_samples - num_existing_samples

		speed_sim_results = multi_sim_run(sim_params,num_samples_from_end)
		
		sim_run_succesfully = False

		# while(not sim_run_succesfully):

		# 	try:
		# 		speed_sim_results = multi_sim_run(sim_paramsnum_samples_from_end)
		# 		sim_run_succesfully = True
		# 	except:
		# 		print('Simulation failed. Trying again.')

		# print('Simulations run succesfully.')



		for sim_speeds in speed_sim_results:
			speed_vals.append(sim_speeds)	



		# total_sim_runs += num_samples

		# speed_result_ids = []

		# for i in range(samples_to_run):
		# 	speed_result_ids.append(run_sim.remote(sim_params,sim_length,num_samples_from_end))
			
		# speed_sim_results = ray.get(speed_result_ids)
		
		# for sim_speeds in speed_sim_results:
		# 	speed_vals.appen(sim_speeds)	

		# speed_vals = np.array(speed_vals)
		# file_name  = 'a-'+str(a)+'b-'+str(b)+'.csv'
		# np.savetxt(folder_path+file_name,speed_vals)

		save_csv(a,b,speed_vals)

		print('Sampling finished.')









