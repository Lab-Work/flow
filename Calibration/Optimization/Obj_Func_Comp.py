"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
======================
George Update: 
======================
import numpy as np
import maplotlib.pyplot as pt
import os
from scipy.optimize import minimize
import Explore_Calibration

# TODO: Hold out true samples for each parameter



# Example1 : phi = Identity, and L = RMSE 
	# For each param calculate L compared to all samples -> This makes a pdf of L values
	# For each L distribution calculate



# Example2 : phi = Identity, and L = SSE
# Example3 : phi = Identity, and L = MAE


#### Now look at
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
#======================
#Shanto Update: 
#======================

import numpy as np
import matplotlib.pyplot as pt
import os
from scipy.optimize import minimize
#import Explore_Calibration
import glob, os

class SimInfo:
    '''
    class for doing feature extraction and loss function comparison on a data set corresponding to a certain
    parameter set.

    '''

    def __init__(self, csv_folder,file_name):

        self.a,self.b = self.get_params_csv_name(file_name)
        self.csv_path = csv_folder + file_name
        self.speedData = np.loadtxt(self.csv_path)
        self.num_samples = len(self.speedData)
        self.realSpeedData = self.getRealSpeedsData()
    """
    METHODS STILL NEEDED:
        getter methods for more phi functions
        getter methods for more L functions
        complete test method for the pipeline (launchTest)
        plotter methods
    """

    def get_params_csv_name(self,file_name):
        a_pos = 2
        b_pos = a_pos
        while(file_name[b_pos] != 'b'):
            b_pos += 1
        b_pos += 2

        a_val = float(file_name[a_pos:b_pos-2])

        b_val = float(file_name[b_pos:-4])

        return [a_val,b_val]

    def getRealSpeedsData(self):
        file_name = 'a-'+str(self.a)+'b-'+str(self.b)+'.csv'
        real_speed_data = np.loadtxt('Test_Set/'+file_name)
        return real_speed_data


    def setRealSpeedsData(self,real_speed_data_new):
        '''
        Want to be able to set a new real speed, that may not correspond to this parameters true
        speed sample, because we're comparing to a different parameter set.
        '''
        self.realSpeedData = real_speed_data_new



    #L functions


    def RMSE(self,x,y):
        return np.sqrt(np.average(np.multiply((x-y),(x-y))))

    def MAE(self,x,y):
        return np.average(np.abs(x-y))

    def SSE(self,x,y):
        return np.sum(np.multiply((x-y),(x-y)))

    # George: Problem with current implementation is that you need to possible transform the data
    # before pushing through the loss metric. Can't compare

    # def getRMSE(self, simSpeed):
    #     return np.sqrt(np.average(np.multiply((self.realSpeedData-simSpeed),(self.realSpeedData-simSpeed))))

    # def getMAE(self, simSpeed):
    #         return np.average(np.abs(self.realSpeedData-simSpeed))

    # def getSSE(self, simSpeed):
    #         return np.sum(np.multiply((self.realSpeedData-simSpeed),(self.realSpeedData-simSpeed)))

    #Phi functions
    def getAmplitude(self, simSpeed):
        amplitude_x = np.max(simSpeed)-np.min(simSpeed)
        return amplitude_x

    def getMean(self, simSpeed):
        return np.average(simSpeed)

    def get_Mean_and_std(self,simSpeed):
        return [np.average(simSpeed),np.std(simSpeed)]

    def getIdentity(self, simSpeed):
        return simSpeed


    # For processing the transformations and 

    def get_Transformed_Data(self,phi):
        '''Runs all the t'''
        transformed_data = []
        for i in range(self.num_samples):
            simSpeed = self.speedData[i,:]
            transformed_data.append(phi(simSpeed))
        transformed_real_data  = phi(self.realSpeedData)
        return [transformed_data,transformed_real_data]

    def get_L_dist(self,L,phi):
        transformed_data,transformed_real_data = self.get_Transformed_Data(phi)
        loss_values = []
        for i in range(self.num_samples):
            loss_values.append(L(transformed_data[i,:],transformed_real_data))
        return loss_values

    def get_L_Expect(self,L,phi):
        '''This is the final output for assessing objective of a candidate L and phi'''
        return np.average(self.get_L_dist(L,phi))         


    # def launchTest(self,phi, L):
    #     # this function is supposed to take a phi func and L fun as an input and launch whatever test you wanted to do 
    #     # and return whatever value you need
    #     phi_all_samples = []
    #     L_all_samples = []
    #     for individual_speed_data in self.speedData:
    #         phi_all_samples.append(phi(individual_speed_data))
    #         L_all_samples.append(L(individual_speed_data))
    #     phi_all_samples = np.array(phi_all_samples)
    #     L_all_samples = np.array(L_all_samples)
    #     # i forgot what the next steps are, also I am not too sure if this is what you actually wanted as well
    #     # we can also store information within the object/ return key info for making plots from this


# George: Just commenting this out temporarily to test

if __name__ == "__main__":
    csv_folder = 'Param_Sweep/'
    file_name = 'a-0.5b-1.0.csv'
    sim_info = SimInfo(csv_folder = csv_folder,file_name = file_name)
#     dir_to_csv_files = "/Users/sshanto/summer_2020/vu/flow/Calibration/Optimization/MegaSimAnalysis/Param_Sweep/"
#     csvFiles = [] #each element is a tuple of (a,b,csvfile)

#     for file in glob.glob(dir_to_csv_files+"*csv"):
#         fname = os.path.splitext(file)[0].split("/")[-1]
#         b = float(fname.split("b")[1])
#         a = float(fname.split("b")[0].split("a")[-1])
#         csvFiles.append((a,b,file))

#     allSims = [SimInfo(csvFiles[i]) for i in range(len(csvFiles))] # stores all SimInfo objects from all the data files in this array
#     for sim in allSims:
#         # Example1 : phi = Identity, and L = RMSE 
#         sim.launchTest(sim.getIdentity,sim.getRMSE)
#         # Example2 : phi = Identity, and L = SSE
#         sim.launchTest(sim.getIdentity,sim.getSSE)
#         # Example3 : phi = Identity, and L = MAE
#         sim.launchTest(sim.getIdentity,sim.getMAE)
