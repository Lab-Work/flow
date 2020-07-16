
import numpy as np
# import highway_free_flow as hff
import highway_congested as hc
import time, random, csv, os, sys
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns

b_val = 2.0

#step 1
real_params = [1.3,b_val]
real_results = hc.HighwayCongested(wave_params=real_params)
original_count = np.array(real_results.getCountsData())
original_speed = np.array(real_results.getVelocityData())
#mean_original_speed = np.mean(original_speed)
#mean_original_count = np.mean(original_count)
#std_original_speed = np.std(original_speed)
#std_original_count = np.std(original_count)

#step 2
a_range = [0.3,2.0]
num_a_samples = 18
num_per_param_samples = 1
a_vals = np.linspace(a_range[0],a_range[1],num_a_samples)
a_vals = list(a_vals)


#step 3
#main data format:
#    a val, b val, mean_counts, std_counts, count_error_wrt_origina, mean_speed, std_speed, speed_error_wrt_original
#seperate data file:
#    a val, b val, counts array, speed array
def adjustSize(sim, real):
    real = list(real)
    sim = list(sim)
    while len(real) > len(sim):
        real.pop()
    while len(sim) > len(real):
        sim.pop()
    return [np.array(sim),np.array(real)]

def selectNumSamples(simmed_measures, real_measures, num_samples_from_end):
    simmed_measures, real_measures = adjustSize(simmed_measures,real_measures)
    simmed_measures_trimmed = simmed_measures[- num_samples_from_end:]
    real_measures_trimmed = real_measures[- num_samples_from_end:]
    return [simmed_measures_trimmed,real_measures_trimmed]

def getSpeedError(simmed_speed):
    error_speeds = ((simmed_speed - original_speed)**2).sum()
    return error_speeds

def getCountsError(simmed_counts):
    error_counts = ((simmed_counts - original_count)**2).sum()
    return error_counts

num_samples_kept = 15

def createStatsFile(a,sim_counts,sim_speed):
    mean_counts = np.mean(sim_counts)
    mean_speed = np.mean(sim_speed)
    std_counts = np.std(sim_counts)
    std_speed = np.std(sim_speed)
    counts_error = getCountsError(sim_counts)
    speed_error = getSpeedError(sim_speed)
    data_line = [a, b_val, mean_counts, std_counts, counts_error, mean_speed, std_speed, speed_error]
    with open("main_data.csv", 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows([data_line])

counts = []
speeds = []
#adjusting the size of orginal data
original_count = original_count[-num_samples_kept:] 
original_speed = original_speed[-num_samples_kept:] 

for a in a_vals:
    print('a value: '+str(a))
    sim_params = [a,b_val]
    sim_results = hc.HighwayCongested(wave_params=sim_params)
    sim_counts = np.array(sim_results.getCountsData())
    sim_speeds = np.array(sim_results.getVelocityData())
    createStatsFile(a, sim_counts[-num_samples_kept:], sim_speeds[-num_samples_kept:])
    sim_results.destroyCSV()
    counts.append(sim_counts[-num_samples_kept:])
    speeds.append(sim_speeds[-num_samples_kept:])

counts = np.array(counts)
speeds = np.array(speeds)

np.savetxt('varying_a_counts.csv',counts,delimiter=',')
np.savetxt('varying_a_speeds.csv',speeds,delimiter=',')
np.savetxt('varying_a_aVals.csv',a_vals,delimiter=',')
print('Sampling finished.')

#plot
def selectColor(val):
    cmap = plt.cm.get_cmap('Spectral')
    rgba = cmap(val)
    rgba = tuple(int((255*x)) for x in rgba[0:3])
    rgba = 'rgb'+str(rgba)
    return rgba

a_vals = np.array(a_vals)
colour = [i / a_vals.max() for i in a_vals]

sns.set_palette(sns.color_palette("hls", 20))
for i in range(len(a_vals)):
    plt.plot([x for x in range(len(speeds[i]))], speeds[i], label="a = {}".format(a_vals[i]))
plt.legend()
plt.ylabel('Average Speeds [m/s]')
plt.xlabel('Measurement Number')
plt.title('Affects of varying a')
plt.savefig("plot_v_a.png")
plt.show()


for i in range(len(a_vals)):
    plt.plot([x for x in range(len(counts[i]))], counts[i], label="a = {}".format(a_vals[i]))
plt.legend()
plt.ylabel('Average Counts')
plt.xlabel('Measurement Number')
plt.title('Affects of varying a')
plt.savefig("plot_q_a.png")
plt.show()
