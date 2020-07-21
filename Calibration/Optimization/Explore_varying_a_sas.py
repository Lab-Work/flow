"""
Usage:
    before running this code make sure to delete any main_data.csv file in the Optimization directory
    after running this code execute the "statsPlot.py" program to generate other important plots
"""
import numpy as np
# import highway_free_flow as hff
import highway_congested as hc
import time, random, csv, os, sys
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns


class ParamSweep:

    def __init__(self,b_val=2,real_a=1.3,range_a=[0.3,2.0], num_a_samples=18, num_samples_kept=15):
        self.b_val = b_val
        self.real_a = real_a
        self.real_params = [self.real_a,self.b_val]
        self.real_results = hc.HighwayCongested(wave_params=self.real_params)
        self.original_count = np.array(self.real_results.getCountsData())
        self.original_speed = np.array(self.real_results.getVelocityData())
        self.a_range = range_a 
        self.num_a_samples = num_a_samples 
        self.num_per_param_samples = 1
        self.a_vals = np.linspace(self.a_range[0],self.a_range[1],self.num_a_samples)
        self.a_vals = list(self.a_vals)
        self.num_samples_kept = num_samples_kept

    def adjustSize(self,sim, real):
        real = list(real)
        sim = list(sim)
        while len(real) > len(sim):
            real.pop()
        while len(sim) > len(real):
            sim.pop()
        return [np.array(sim),np.array(real)]

    def selectNumSamples(self, simmed_measures, real_measures, num_samples_from_end):
        simmed_measures, real_measures = adjustSize(simmed_measures,real_measures)
        simmed_measures_trimmed = simmed_measures[- self.num_samples_from_end:]
        real_measures_trimmed = real_measures[- self.num_samples_from_end:]
        return [simmed_measures_trimmed,real_measures_trimmed]

    def getSpeedError(self,simmed_speed):
        error_speeds = ((simmed_speed - self.original_speed)**2).sum()
        return error_speeds

    def getCountsError(self,simmed_counts):
        error_counts = ((simmed_counts - self.original_count)**2).sum()
        return error_counts

    #def getRMSEOfMeanErrorVector(): 

    def createStatsFile(self,a,sim_counts,sim_speed):
        mean_counts = np.mean(sim_counts)
        mean_speed = np.mean(sim_speed)
        std_counts = np.std(sim_counts)
        std_speed = np.std(sim_speed)
        counts_error = self.getCountsError(sim_counts)
        speed_error = self.getSpeedError(sim_speed)
        data_line = [a, self.b_val, mean_counts, std_counts, counts_error, mean_speed, std_speed, speed_error]
        with open("main_data.csv", 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows([data_line])

    def runParameterSweep(self):
        counts = []
        speeds = []
        #adjusting the size of orginal data
        self.original_count = self.original_count[-self.num_samples_kept:] 
        self.original_speed = self.original_speed[-self.num_samples_kept:] 

        for a in self.a_vals:
            print('a value: '+str(a))
            sim_params = [a,self.b_val]
            sim_results = hc.HighwayCongested(wave_params=sim_params)
            sim_counts = np.array(sim_results.getCountsData())
            sim_speeds = np.array(sim_results.getVelocityData())
            self.createStatsFile(a, sim_counts[-self.num_samples_kept:], sim_speeds[-self.num_samples_kept:])
            sim_results.destroyCSV()
            counts.append(sim_counts[-self.num_samples_kept:])
            speeds.append(sim_speeds[-self.num_samples_kept:])

        counts = np.array(counts)
        speeds = np.array(speeds)

        np.savetxt('varying_a_counts.csv',counts,delimiter=',')
        np.savetxt('varying_a_speeds.csv',speeds,delimiter=',')
        np.savetxt('varying_a_aVals.csv',self.a_vals,delimiter=',')
        print('Sampling finished.')
        self.a_vals = np.array(self.a_vals)
        colour = [i / self.a_vals.max() for i in self.a_vals]

        sns.set_palette(sns.color_palette("hls", 20))
        for i in range(len(self.a_vals)):
            plt.plot([x for x in range(len(speeds[i]))], speeds[i], label="a = {}".format(self.a_vals[i]))
        plt.legend()
        plt.ylabel('Average Speeds [m/s]')
        plt.xlabel('Measurement Number')
        plt.title('Affects of varying a')
        plt.savefig("plot_v_a.png")
        plt.show()

        for i in range(len(self.a_vals)):
            plt.plot([x for x in range(len(counts[i]))], counts[i], label="a = {}".format(self.a_vals[i]))
        plt.legend()
        plt.ylabel('Average Counts')
        plt.xlabel('Measurement Number')
        plt.title('Affects of varying a')
        plt.savefig("plot_q_a.png")
        plt.show()


if __name__ == "__main__":
    param1 = ParamSweep()
    param1.runParameterSweep()
