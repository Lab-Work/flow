import matplotlib.pyplot as plt
import csv
import pandas as pd
import numpy as np
import Process_Flow_Outputs as PFO
import time

class Plotter:

    def __init__(self, csv1, csv2, sim_length, road_length):
        self.csv1 = csv1
        self.csv2 = csv2
        self.sim_length = sim_length
        self.road_length = road_length

    def getSpaceTimeDiagram(self):
        data1 = PFO.SimulationData(csv_path = self.csv1)
        data2 = PFO.SimulationData(csv_path = self.csv2)
        edge_list = ['highway_0']
        lane_list = ['0']
        time_range = [0,self.sim_length]
        pos_range = [0,self.road_length]
        clim = [0,30]
        fileName = "figures/DualSpaceTimePlot.png"
        marker_size=1.0
        coloring_Attribute = 'SPEED'
        plot1 = data1.plot_Time_Space(coloring_Attribute=coloring_Attribute,edge_list=edge_list,lane_list=lane_list,clim=clim,fileName=fileName,time_range=time_range,pos_range=pos_range,marker_size=marker_size,multiple=True)
        plot2 = data2.plot_Time_Space(coloring_Attribute=coloring_Attribute,edge_list=edge_list,lane_list=lane_list,clim=clim,fileName=fileName,time_range=time_range,pos_range=pos_range,marker_size=marker_size,multiple=True)
        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.suptitle('Space Time Diagrams')
        ax1.scatter(plot1[0],plot1[1],s=plot1[2],c=plot1[3],marker=plot1[4])
        ax2.scatter(plot2[0],plot2[1],s=plot2[2],c=plot2[3],marker=plot2[4])
        plt.show()

if __name__ == "__main__":
    fig  = Plotter("data/highway_20200720-1658221595282302.740185-emission.csv", "data/highway_20200720-1658221595282302.740185-emission.csv", 2250, 1600)
    fig.getSpaceTimeDiagram()
