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

    def __init__(self, csvFileInfo):
        self.a = csvFileInfo[0]
        self.b = csvFileInfo[1]
        self.csvFile = csvFileInfo[2]
        self.speedData = np.loadtxt(self.csvFile)
        self.realSpeedData = self.getRealSpeedsData()
    """
    METHODS STILL NEEDED:
        getter methods for more phi functions
        getter methods for more L functions
        complete test method for the pipeline (launchTest)
        plotter methods
    """
    def getRealSpeedsData(self, isSameFile=True):
        if isSameFile:
            real = self.speedData[0] #using the first line as real data
        else:
            # THIS PART NEEDS CHANGE: I made this structure so that you can use real data from same file or some other file
            # you mentioned something about rerunning a parameter sweep and using that as real data
            # if you do that just make sure you change the following part
            real = np.loadtxt("where ever the vector csv is stored")
        return real

    #L functions
    def getRMSE(self, simSpeed):
        return np.sqrt(np.average(np.multiply((self.realSpeedData-simSpeed),(self.realSpeedData-simSpeed))))

    def getMAE(self, simSpeed):
            return np.average(np.abs(self.realSpeedData-simSpeed))

    def getSSE(self, simSpeed):
            return np.sum(np.multiply((self.realSpeedData-simSpeed),(self.realSpeedData-simSpeed)))

    #Phi functions
    def getAbsolutAmplitude_diff(self, simSpeed):
            amplitude_x = np.max(self.realSpeedData)-np.min(self.realSpeedData)
            amplitude_y = np.max(simSpeed)-np.min(simSpeed)
            return np.abs(amplitude_y-amplitude_x)

    def getIdentity(self, simSpeed):
        #I am not too sure if this is the correct implementaion
        return self.realSpeedData - simSpeed

    def launchTest(self,phi, L):
        # this function is supposed to take a phi func and L fun as an input and launch whatever test you wanted to do 
        # and return whatever value you need
        phi_all_samples = []
        L_all_samples = []
        for individual_speed_data in self.speedData:
            phi_all_samples.append(phi(individual_speed_data))
            L_all_samples.append(L(individual_speed_data))
        phi_all_samples = np.array(phi_all_samples)
        L_all_samples = np.array(L_all_samples)
        # i forgot what the next steps are, also I am not too sure if this is what you actually wanted as well
        # we can also store information within the object/ return key info for making plots from this

if __name__ == "__main__":
    dir_to_csv_files = "/Users/sshanto/summer_2020/vu/flow/Calibration/Optimization/MegaSimAnalysis/Param_Sweep/"
    csvFiles = [] #each element is a tuple of (a,b,csvfile)

    for file in glob.glob(dir_to_csv_files+"*csv"):
        fname = os.path.splitext(file)[0].split("/")[-1]
        b = float(fname.split("b")[1])
        a = float(fname.split("b")[0].split("a")[-1])
        csvFiles.append((a,b,file))

    allSims = [SimInfo(csvFiles[i]) for i in range(len(csvFiles))] # stores all SimInfo objects from all the data files in this array
    for sim in allSims:
        # Example1 : phi = Identity, and L = RMSE 
        sim.launchTest(sim.getIdentity,sim.getRMSE)
        # Example2 : phi = Identity, and L = SSE
        sim.launchTest(sim.getIdentity,sim.getSSE)
        # Example3 : phi = Identity, and L = MAE
        sim.launchTest(sim.getIdentity,sim.getMAE)
