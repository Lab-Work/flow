import matplotlib.pyplot as plt
import csv
import pandas as pd
import numpy as np
import Process_Flow_Outputs as PFO
import time

class Plotter:

    def __init__(self, csv1, csv2, sim_length, road_length, aval1, aval2):
        self.csv1 = csv1
        self.csv2 = csv2
        self.sim_length = sim_length
        self.road_length = road_length
        self.aval1 = aval1
        self.aval2 = aval2
        self.fidelity = 30
        self.position_for_count = 800
        self.countsData = []
        self.speedData = []
        self.timeData = []

    def processMacroData(self,csvFile):
        highway_data = PFO.SimulationData(csv_path = csvFile)
        pos_dict = highway_data.get_Timeseries_Dict(data_id='TOTAL_POSITION',want_Numpy=True)
        vel_dict =highway_data.get_Timeseries_Dict(data_id='SPEED',want_Numpy=True)
        position_for_count = self.position_for_count #radar reading position
        vTime_array = []  # array to store (time, velocity) results
        for veh_id in highway_data.veh_ids:  # looping through all cars
            pos_data = pos_dict[veh_id]  # store position information for each car
            end_pos = pos_data[1, -1]
            veh_data = vel_dict[veh_id]
            if(end_pos > position_for_count):  # if car crossed the radar line point
                t = 0
                p = pos_data[1, t]  # position at which car was spawned
                while(p < position_for_count):
                    t += 1
                    p = pos_data[1, t]
                vTime_array.append((pos_data[0, t], veh_data[1, t]))
        vTime_array.sort(key=lambda x: x[0])
        count_num, average_speed, times_data = self.countsEveryXSeconds(self.fidelity, vTime_array)
        self.countsData, self.speedData, self.timeData = count_num, average_speed, times_data

    def countsEveryXSeconds(self, x, sorted_counts):
        i = 0
        m = 0
        j = 1
        comp = x
        c = []
        mc = []
        meanSpeed = []
        while (i < len(sorted_counts)):
            while( (m!=len(sorted_counts)) and ((j-1)*comp <= sorted_counts[m][0] <=   j*comp) ) :
                c.append(sorted_counts[m])
                m+=1
            i = m
            j+=1
            d = c.copy()
            mc.append(d)
            #print(d)
            if (len(d) == 0):
                meanSpeed.append(0)
            else:
                meanSpeed.append(round(sum(i for _, i in d)/len(d),3))
            c.clear()
        mcc = []
        for k in mc:
            mcc.append(len(k))
        time = [30*i for i in range(1,len(mcc)+1)]
     #   print("last time: ", sorted_counts[-1][0])
        if (sorted_counts[-1][0] > float(self.sim_time)*60):
            mcc.pop()
            meanSpeed.pop()
            time.pop()
     #   print("len(speeds), speeds: {} , {}".format(len(meanSpeed), meanSpeed))
     #   print("len(counts), counts: {} , {}".format(len(mcc), mcc))
     #   print("len(time) , time: {} {}".format(len(time), time))
        return mcc, meanSpeed, time


    def getSpaceTimeDiagram(self, timeCut=0, hcut=0):
        data1 = PFO.SimulationData(csv_path = self.csv1)
        data2 = PFO.SimulationData(csv_path = self.csv2)
        edge_list = ['highway_0']
        lane_list = ['0']
        time_range = [timeCut, self.sim_length]
        pos_range = [0+hcut,self.road_length-hcut]
        clim = [0,30]
        fileName = "figures/DualSpaceTimePlot.png"
        marker_size=1.0
        coloring_Attribute = 'SPEED'
        plot1 = data1.plot_Time_Space(coloring_Attribute=coloring_Attribute,edge_list=edge_list,lane_list=lane_list,clim=clim,fileName=fileName,time_range=time_range,pos_range=pos_range,marker_size=marker_size,multiple=True)
        plot2 = data2.plot_Time_Space(coloring_Attribute=coloring_Attribute,edge_list=edge_list,lane_list=lane_list,clim=clim,fileName=fileName,time_range=time_range,pos_range=pos_range,marker_size=marker_size,multiple=True)
        fig, (ax1, ax2) = plt.subplots(1, 2, sharex=True)
        fig.suptitle('Space Time Diagrams')
        im1 = ax1.scatter(plot1[0],plot1[1],s=plot1[2],c=plot1[3],marker=plot1[4])
        ax1.set_title("a = {}".format(self.aval1))
       # im1.set_clim(clim)
        ax1.set_ylabel("Position (m)")
        im2 = ax2.scatter(plot2[0],plot2[1],s=plot2[2],c=plot2[3],marker=plot2[4])
        ax2.set_title("a = {}".format(self.aval2))
       # im2.set_clim(clim)
        ax2.set_xlabel("Time (s)")
       # plt.colorbar(im2)
        plt.savefig(fileName)
        plt.show()

    def getRadarDataPlot(self, data1, data2, fname, ylab):
        xval = [i for i in range(len(data1))]
        plt.plot(xval, data1, label="a = {}".format(self.aval1))
        plt.plot(xval, data2, label="a = {}".format(self.aval2))
        plt.xlabel("Measurement Number")
        plt.ylabel(ylab)
        plt.legend()
        plt.title("{} Data at a = {}".format(ylab, self.aval1))
        plt.savefig("figures/radar_plot_"+fname+".png")
        plt.show()


"""
New Class
"""

class RDSData:

    def __init__(self, csvFile, a_val,sim_time):
        self.csvFile = csvFile
        self.fidelity = 30
        self.position_for_count = 800
        self.countsData = []
        self.speedData = []
        self.timeData = []
        self.a_val = a_val
        self.sim_time = sim_time

    def processMacroData(self):
        highway_data = PFO.SimulationData(csv_path = self.csvFile)
        pos_dict = highway_data.get_Timeseries_Dict(data_id='TOTAL_POSITION',want_Numpy=True)
        vel_dict =highway_data.get_Timeseries_Dict(data_id='SPEED',want_Numpy=True)
        position_for_count = self.position_for_count #radar reading position
        vTime_array = []  # array to store (time, velocity) results
        for veh_id in highway_data.veh_ids:  # looping through all cars
            pos_data = pos_dict[veh_id]  # store position information for each car
            end_pos = pos_data[1, -1]
            veh_data = vel_dict[veh_id]
            if(end_pos > position_for_count):  # if car crossed the radar line point
                t = 0
                p = pos_data[1, t]  # position at which car was spawned
                while(p < position_for_count):
                    t += 1
                    p = pos_data[1, t]
                vTime_array.append((pos_data[0, t], veh_data[1, t]))
        vTime_array.sort(key=lambda x: x[0])
        count_num, average_speed, times_data = self.countsEveryXSeconds(self.fidelity, vTime_array)
        self.countsData, self.speedData, self.timeData = count_num, average_speed, times_data
        return self.countsData, self.speedData, self.timeData 

    def countsEveryXSeconds(self, x, sorted_counts):
        i = 0
        m = 0
        j = 1
        comp = x
        c = []
        mc = []
        meanSpeed = []
        while (i < len(sorted_counts)):
            while( (m!=len(sorted_counts)) and ((j-1)*comp <= sorted_counts[m][0] <=   j*comp) ) :
                c.append(sorted_counts[m])
                m+=1
            i = m
            j+=1
            d = c.copy()
            mc.append(d)
            #print(d)
            if (len(d) == 0):
                meanSpeed.append(0)
            else:
                meanSpeed.append(round(sum(i for _, i in d)/len(d),3))
            c.clear()
        mcc = []
        for k in mc:
            mcc.append(len(k))
        time = [30*i for i in range(1,len(mcc)+1)]
     #   print("last time: ", sorted_counts[-1][0])
        if (sorted_counts[-1][0] > float(self.sim_time)*60):
            mcc.pop()
            meanSpeed.pop()
            time.pop()
     #   print("len(speeds), speeds: {} , {}".format(len(meanSpeed), meanSpeed))
     #   print("len(counts), counts: {} , {}".format(len(mcc), mcc))
     #   print("len(time) , time: {} {}".format(len(time), time))
        return mcc, meanSpeed, time


"""
if __name__ == "__main__":
    fig  = Plotter("data/highway_a73.csv", "data/highway_a13_2.csv", 2250, 1600,0.73,0.73)
    f1 = RDSData("data/highway_a73.csv", 0.73, 2250)
    f2 = RDSData("data/highway_a73_2.csv", 0.73, 2250)
    f1_data= f1.processMacroData()
    f2_data= f2.processMacroData()
    #fig.getSpaceTimeDiagram()
    fig.getRadarDataPlot(f1_data[1], f2_data[1], "speeds_sim_04", "Speeds")
    fig.getRadarDataPlot(f1_data[0], f2_data[0], "counts_sim_04", "Counts")
"""
