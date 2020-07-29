"""
notes:
    make sure there are no non-csv files in Param_Sweep
"""

import numpy as np
import os
from Obj_Func_Comp import SimInfo
import matplotlib.pyplot as pt 

#Initialize an SimInfo Object for each parameter set
csv_folder = 'Param_Sweep/'
test_folder = 'Test_Set/'
csv_files = os.listdir(csv_folder)

# put each siminfo into dict to then later reference
sim_info_dict = dict.fromkeys(csv_files)
for csv_file in csv_files: 
	sim_info_dict[csv_file] = SimInfo(csv_folder=csv_folder,file_name=csv_file)


###  Look at L = RMSE and phi = I ###

# Fix one parameter value: a=.5,b=1.1
a = .5
b = 1.2
csv_file_real = 'a-'+str(a)+'b-'+str(b)+'.csv'
speed_true = np.loadtxt(test_folder+csv_file_real)

# plot expected L for all parameter sets and make clear which is the 'true'

for csv_file in csv_files: 
	# Set the 'real speed' to be what corresponds to the 'true' parameter values
	sim_info_dict[csv_file].setRealSpeedsData(real_speed_data_new=speed_true)



L_expectations = dict.fromkeys(csv_files) # Expected value from distribution of L values on phi(x),phi(y)

L_dist_vals = dict.fromkeys(csv_files)

L_plot = [] #tuple of (expected, max, min, isRealParam)

for csv_file in csv_files:
    #For each param set assess the expected L:
    sim_info =  sim_info_dict[csv_file]
    L = sim_info.getRMSE
    phi = sim_info.getIdentity
    L_dist = sim_info.get_L_dist(L,phi) # vector of loss function evals: L(phi(X),phi(y))
    L_expect = sim_info.get_L_Expect(L,phi)
    L_expectations[csv_file] = L_expect
    L_dist_vals[csv_file] = L_dist
    if csv_file == csv_file_real:
        L_plot.append((L_expect,max(L_dist),min(L_dist),True))
        print("YESSS")
    else:
        L_plot.append((L_expect,max(L_dist),min(L_dist),False))
# plot results: Sorted by L_expect plot showing range of L (given by L_dist_vals), mark true value in some way

sorted_by_L_exp = sorted(L_plot, key=lambda tup: tup[0])
x_L_expect = [i for i in range(len(L_plot))]
L_exp = [i[0] for i in sorted_by_L_exp]
L_max = [i[1] for i in sorted_by_L_exp]
L_min = [i[2] for i in sorted_by_L_exp]
TrueIndex = [i[3] for i in sorted_by_L_exp].index(True)

pt.plot(x_L_expect, L_exp, 'b.')
pt.plot(x_L_expect, L_max, 'g.')
pt.plot(x_L_expect, L_min, 'y.')
#true
pt.plot(x_L_expect[TrueIndex], L_exp[TrueIndex], 'rs')
pt.plot(x_L_expect[TrueIndex], L_max[TrueIndex], 'rs')
pt.plot(x_L_expect[TrueIndex], L_min[TrueIndex], 'rs')

pt.xlabel("Simulations")
pt.ylabel("Loss Function Evaulations")
pt.legend(["expected", "max", "min"])
pt.show()
