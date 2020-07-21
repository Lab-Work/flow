"""
sas message
Currently working on multiple sim code
"""
import numpy as np
import highway_congested as hc
import random, csv, os
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns
import pandas as pd
from pandas import DataFrame

class ParamSweep:

    def __init__(self,b_val=2,real_a=1.3,
                 range_a=[0.3,2.0],
                 num_a_samples=18,
                 num_samples_kept=15,
                 sample_time_mins=10,  #mins
                 consideration_time = 20,  #mins
                 numSamples=5):

        self.b_val = b_val
        self.real_a = real_a
        self.real_params = [self.real_a,self.b_val]
        self.real_results = hc.HighwayCongested(wave_params=self.real_params)
        self.fidelity = self.real_results.fidelity
        self.original_count = np.array(self.real_results.getCountsData())
        self.original_speed = np.array(self.real_results.getVelocityData())
        self.a_range = range_a
        self.num_a_samples = num_a_samples
        self.num_per_param_samples = 1
        self.a_vals = np.linspace(self.a_range[0],self.a_range[1],self.num_a_samples)
        self.a_vals = list(self.a_vals)
        self.num_samples_kept = num_samples_kept
        self.sample_time_mins = sample_time_mins
        self.consideration_time = consideration_time
        self.numSamples = numSamples
        self.deleteExistingDataFile()

    def deleteExistingDataFile(self):
        os.remove('main_data.csv')

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

    def getRMSEOfMeanErrorVector(self, sim_results, a):
        pass

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

    def plotSpeedGraph(self,speeds):
        sns.set_palette(sns.color_palette("hls", 20))
        for i in range(len(self.a_vals)):
            plt.plot([x for x in range(len(speeds[i]))], speeds[i], label="a = {}".format(self.a_vals[i]))
        plt.legend()
        plt.ylabel('Average Speeds [m/s]')
        plt.xlabel('Measurement Number')
        plt.title('Affects of varying a')
        plt.savefig("plot_v_a.png")
        plt.show()

    def plotCountsGraph(self, counts):
        for i in range(len(self.a_vals)):
            plt.plot([x for x in range(len(counts[i]))], counts[i], label="a = {}".format(self.a_vals[i]))
        plt.legend()
        plt.ylabel('Average Counts')
        plt.xlabel('Measurement Number')
        plt.title('Affects of varying a')
        plt.savefig("plot_q_a.png")
        plt.show()

    def getAbsSquaredError(self, sim_results, a):
        sim_counts = np.array(sim_results.getCountsData())
        sim_speeds = np.array(sim_results.getVelocityData())
        self.createStatsFile(a, sim_counts[-self.num_samples_kept:], sim_speeds[-self.num_samples_kept:])
        sim_results.destroyCSV()
        return sim_counts[-self.num_samples_kept:], sim_speeds[-self.num_samples_kept:]

    def saveNumpyTxtFiles(self, counts, speeds, delim = ','):
        np.savetxt('varying_a_counts.csv',counts,delimiter=delim)
        np.savetxt('varying_a_speeds.csv',speeds,delimiter=delim)
        np.savetxt('varying_a_aVals.csv',self.a_vals,delimiter=delim)

    def getRandomSampleofSizeX(self,all_data, X, consideration):
        max_size = len(all_data)
        randNum = random.randint(max_size-consideration, max_size)
        if (len(all_data[randNum:]) >= X):
            return np.array(all_data[randNum:randNum+X])
        else:
            self.getRandomSampleofSizeX(all_data,X,consideration)

    def rmse(self, diff_vector):
        return np.sqrt(np.mean((diff_vector)**2))

    def saveErrors(self, error, params, fname="error.csv", delim=","):
        with open("data/"+fname, 'a') as f:
            f.write(str(error)+delim+str(params)+"\n")

    def runMultipleSimParameterSweep(self, numSamples=self.numSamples):
        """
        required plots:
            1) RMSE(average_vector) vs a_val
            2) 5 speeds vector for 1 a on all a_vals
        """
        fname = open('data/param_sweep_speeds.csv','ab')
        vector_size = int((self.sample_time_mins * 60)/self.fidelity)
        consider_size = int((self.consideration_time * 60)/self.fidelity)
        self.original_speed = self.getRandomSampleofSizeX(self.original_speed, vector_size, consider_size)
        speeds_vector = []
        for a in self.a_vals:
            print('a value: '+str(a))
            sim_params = [a,self.b_val]
            sim_results = hc.HighwayCongested(wave_params=sim_params)
            sim_speeds = np.array(sim_results.getVelocityData())
            total_sims = numSamples
            rmse_vector = []
            while numSamples != 0:
                speed_s = self.getRandomSampleofSizeX(sim_speeds, vector_size, consider_size)
                rmse_vector.append(speed_s)
                np.savetxt(fname,[np.concatenate((sim_params,speed_s))], delimiter=',',fmt='%2.5f')
                numSamples-=1
            speeds_vector.append(rmse_vector)
            rmse_vector = np.array(rmse_vector)
            mean_error_vector = (1.0 / total_sims) * rmse_vector.sum(axis=0)
            mean_rmse = self.rmse(mean_error_vector)
            print("Mean error vector: {}".format(mean_error_vector))
            print("RMSE of mean error vector: {}".format(mean_rmse))
            fname.close()

    def runSingleSimParameterSweep(self):
        counts = []
        speeds = []
        self.original_count = self.original_count[-self.num_samples_kept:] 
        self.original_speed = self.original_speed[-self.num_samples_kept:] 
        for a in self.a_vals:
            print('a value: '+str(a))
            sim_params = [a,self.b_val]
            sim_results = hc.HighwayCongested(wave_params=sim_params)
            counts_sim, speeds_sim = self.getAbsSquaredError(sim_results,a)
            counts.append(counts_sim)
            speeds.append(speeds_sim)
        counts = np.array(counts)
        speeds = np.array(speeds)
        self.saveNumpyTxtFiles(counts,speeds)
        print('Sampling finished.')
        self.a_vals = np.array(self.a_vals)
        self.plotSpeedGraph(speeds)
        self.plotCountsGraph(counts)

    def getStatsPlots(self):
        df = pd.read_csv('main_data.csv', names = ['a', 'b', 'mean_counts', 'std_counts', 'counts_error', 'mean_speed', 'std_speed', 'speed_error'])

        df.plot(x='a', y='mean_speed')
        plt.ylabel("Average Speed")
        plt.show()

        df.plot(x='a', y='mean_counts')
        plt.ylabel("Average Counts")
        plt.show()

        df.plot(x='a', y='std_speed')
        plt.ylabel("Standard Deviation Speed")
        plt.show()

        df.plot(x='a', y='std_counts')
        plt.ylabel("Standard Deviation Counts")
        plt.show()

        df.plot(x='a', y='speed_error')
        plt.ylabel("Error in Speed")
        plt.show()

        df.plot(x='a', y='counts_error')
        plt.ylabel("Error in Counts")
        plt.show()

if __name__ == "__main__":
    param1 = ParamSweep()
    param1.runSingleSimParameterSweep()
    param1.getStatsPlots()
