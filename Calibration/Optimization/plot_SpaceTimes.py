import os 
import numpy as np
import Process_Flow_Outputs as PFO

figures_path = '/Users/vanderbilt/Desktop/Research_2020/CIRCLES/Model_Dev/flow/Calibration/Optimization/figures/'
data_path = '/Users/vanderbilt/Desktop/Research_2020/CIRCLES/Model_Dev/flow/Calibration/Optimization/data/'
csv_files = os.listdir(data_path)
csv_files.remove('.DS_Store')

num_files = 10

lane_list = ['0']
edge_list = ['highway_0']

for i in range(num_files):
	print('Image number: '+str(i))

	csv_path = data_path + csv_files[i]
	image_name = figures_path + 'TimeSpace_'+str(i)+'.png'

	SimulationData = PFO.SimulationData(csv_path = csv_path)
	SimulationData.plot_Time_Space(edge_list=edge_list,lane_list=lane_list,fileName=image_name,time_range=[0,2000],pos_range=[0000,1600])