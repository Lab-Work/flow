"""
notes:
    no non csv files in Param_Sweep
    error in : loss_values.append(L(transformed_data[i:],transformed_real_data)) no ,
    get_L_dist not Dist
"""

import numpy as np
import os
from Obj_Func_Comp import SimInfo
import matplotlib.pyplot as pt 
from matplotlib  import cm


def getABLStatsData(true_a, true_b):
    csv_folder = 'Param_Sweep/'
    test_folder = 'Test_Set/'
    csv_files = os.listdir(csv_folder)
    # put each siminfo into dict to then later reference
    sim_info_dict = dict.fromkeys(csv_files)
    for csv_file in csv_files: 
            sim_info_dict[csv_file] = SimInfo(csv_folder=csv_folder,file_name=csv_file)
    # Fix one parameter value: a=.5,b=1.1
    a = true_a
    b = true_b
    csv_file_real = 'a-'+str(a)+'b-'+str(b)+'.csv'
    speed_true = np.loadtxt(test_folder+csv_file_real)
    # plot expected L for all parameter sets and make clear which is the 'true'
    for csv_file in csv_files: 
            # Set the 'real speed' to be what corresponds to the 'true' parameter values
            sim_info_dict[csv_file].setRealSpeedsData(real_speed_data_new=speed_true)
    L_expectations = dict.fromkeys(csv_files) # Expected value from distribution of L values on phi(x),phi(y)
    L_dist_vals = dict.fromkeys(csv_files)
    L_plot = [] #tuple of (a, b, expected_L,isRealParam)

    for csv_file in csv_files:
        #For each param set assess the expected L:
        sim_info =  sim_info_dict[csv_file]
        a_sim = sim_info.a
        b_sim = sim_info.b
        L = sim_info.getSPD
        phi = sim_info.getMean
        L_dist = sim_info.get_L_dist(L,phi) # vector of loss function evals: L(phi(X),phi(y))
        L_expect = sim_info.get_L_Expect(L,phi)
        L_expectations[csv_file] = L_expect
        L_dist_vals[csv_file] = L_dist
        if csv_file == csv_file_real:
            L_plot.append((a_sim, b_sim, L_expect, True))
        else:
            L_plot.append((a_sim, b_sim, L_expect, False))

    a_vals = [i[0] for i in L_plot]
    b_vals = [i[1] for i in L_plot]
    L_vals = [i[2] for i in L_plot]
    TrueIndex = [i[3] for i in L_plot].index(True)
    return a_vals, b_vals, L_vals, TrueIndex


def getLStatsData(true_a, true_b):
    csv_folder = 'Param_Sweep/'
    test_folder = 'Test_Set/'
    csv_files = os.listdir(csv_folder)
    # put each siminfo into dict to then later reference
    sim_info_dict = dict.fromkeys(csv_files)
    for csv_file in csv_files: 
            sim_info_dict[csv_file] = SimInfo(csv_folder=csv_folder,file_name=csv_file)
    # Fix one parameter value: a=.5,b=1.1
    a = true_a
    b = true_b
    print(a,b)
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
        L = sim_info.getSPD
        phi = sim_info.getMean
        L_dist = sim_info.get_L_dist(L,phi) # vector of loss function evals: L(phi(X),phi(y))
        L_expect = sim_info.get_L_Expect(L,phi)
        L_expectations[csv_file] = L_expect
        L_dist_vals[csv_file] = L_dist
        if csv_file == csv_file_real:
            L_plot.append((L_expect,max(L_dist),min(L_dist),True))
        else:
            L_plot.append((L_expect,max(L_dist),min(L_dist),False))
    # plot results: Sorted by L_expect plot showing range of L (given by L_dist_vals), mark true value in some way

    sorted_by_L_exp = sorted(L_plot, key=lambda tup: tup[0])
    x_L_expect = [i for i in range(len(L_plot))]
    L_exp = [i[0] for i in sorted_by_L_exp]
    L_max = [i[1] for i in sorted_by_L_exp]
    L_min = [i[2] for i in sorted_by_L_exp]
    TrueIndex = [i[3] for i in sorted_by_L_exp].index(True)
    return L_exp, L_max, L_min, TrueIndex

def createLossValuesPlot(true_a, true_b):
    fig = pt.figure()
    L_exp, L_max, L_min, TrueIndex = getLStatsData(true_a, true_b) 
    x_L_expect = [i for i in range(len(L_exp))]
    pt.plot(x_L_expect, L_exp, 'b.')
    pt.plot(x_L_expect, L_max, 'g.')
    pt.plot(x_L_expect, L_min, 'y.')
    #true
    pt.plot(x_L_expect[TrueIndex], L_exp[TrueIndex], 'rs')
    pt.plot(x_L_expect[TrueIndex], L_max[TrueIndex], 'rs')
    pt.plot(x_L_expect[TrueIndex], L_min[TrueIndex], 'rs')

    pt.title("a: {}, b: {}".format(true_a, true_b))
    pt.xlabel("Simulations")
    pt.ylabel("Loss Function Evaulations")
    pt.legend(["expected", "max", "min"])
    fig.savefig("figures/a-{}b-{}loss.png".format(true_a,true_b), dpi=600)
    pt.close(fig)
 #   pt.show()

def createABLCountourPlot(true_a, true_b): 
    fig = pt.figure()
    a_vals, b_vals, L_vals, TrueIndex = getABLStatsData(true_a, true_b)
    pt.scatter(a_vals, b_vals, c=L_vals)
#    pt.scatter(a_vals[TrueIndex], b_vals[TrueIndex])
    pt.annotate("True Point", (a_vals[TrueIndex], b_vals[TrueIndex]), rotation=60)
    pt.title("a: {}, b: {}".format(true_a, true_b))
    pt.colorbar()
    pt.xlabel("a values")
    pt.ylabel("b values")
    fig.savefig("figures/a-{}b-{}color.png".format(true_a,true_b), dpi=600)
    pt.close(fig)
 #   pt.show()

def getPercentageLessThanLTrue(true_a, true_b): #horrible name I am sorry
    L_exp, L_max, L_min, TrueIndex = getLStatsData(true_a, true_b) 
    totalPoints = len(L_exp)
    return (TrueIndex*100)/totalPoints

def createAllPossiblePlots():
    """
    call this function to create all possible plots
    """
    true_as = [round(0.5+0.1*i,2) for i in range(9)]
    true_bs = [round(1.0+0.1*i,2) for i in range(6)]
    for i in range(len(true_as)):
        for j in range(len(true_bs)):
            createABLCountourPlot(true_as[i],true_bs[j])
            createLossValuesPlot(true_as[i],true_bs[j])

def createPercentageAnalysisColorPlot(LfuncName, PhiFuncName):
    fig = pt.figure(figsize=(8.0, 5.0))
    true_as = [round(0.5+0.1*i,2) for i in range(9)]
    true_bs = [round(1.0+0.1*i,2) for i in range(6)]
    percentages = [] #tuple of (a,b,percentage_val)
    for i in range(len(true_as)):
        for j in range(len(true_bs)):
            percentages.append((true_as[i],true_bs[j],getPercentageLessThanLTrue(true_as[i],true_bs[j])))
    a_vals= [i[0] for i in percentages]
    b_vals= [i[1] for i in percentages]
    L_vals= [i[2] for i in percentages]
    x_vals = [i for i in range(len(a_vals))]
    pt.scatter(a_vals, b_vals, c=L_vals, clim = [0, 100])
#    pt.scatter(a_vals[TrueIndex], b_vals[TrueIndex])
    pt.colorbar()
    score = round(sum(L_vals) /  (len(true_as)*len(true_bs)), 4)
    pt.title("Loss function: {}, Phi operator: {}, <L,Phi> score = {}".format(LfuncName, PhiFuncName, score))
    pt.xlabel("a values")
    pt.ylabel("b values")
    fig.savefig("figures/{}and{}color.png".format(LfuncName,PhiFuncName), dpi=600)
  #  for i, txt in enumerate(params):
  #      pt.annotate(txt, (x_vals[i], L_vals[i]))
  #  pt.show()
    pt.close(fig)

def createPercentageAnalysisPlot(LfuncName, PhiFuncName):
    true_as = [round(0.5+0.1*i,2) for i in range(9)]
    true_bs = [round(1.0+0.1*i,2) for i in range(6)]
    percentages = [] #tuple of (a,b,percentage_val)
    for i in range(len(true_as)):
        for j in range(len(true_bs)):
            percentages.append((true_as[i],true_bs[j],getPercentageLessThanLTrue(true_as[i],true_bs[j])))
    a_vals= [i[0] for i in percentages]
    b_vals= [i[1] for i in percentages]
    L_vals= [i[2] for i in percentages]
    x_vals = [i for i in range(len(a_vals))]
    params = list(zip(a_vals, b_vals))
    pt.plot(x_vals, L_vals, '-.')
    pt.ylabel("Percentage of points that achieve lower expected loss than true point")
    pt.title("Loss function: {}, Phi operator: {}".format(LfuncName, PhiFuncName))
    pt.ylim([0,100])
    for i, txt in enumerate(params):
        pt.annotate(txt, (x_vals[i], L_vals[i]))
    pt.show()

def testPlots():
    createABLCountourPlot(1.3, 1.2)
    createABLCountourPlot(0.5, 1.2)
    createABLCountourPlot(1.1, 1.5)
    createABLCountourPlot(0.7, 1.0)
    createLossValuesPlot(1.3, 1.2)
    createLossValuesPlot(0.5, 1.2)
    createLossValuesPlot(1.1, 1.5)
    createLossValuesPlot(0.7, 1.0)

if __name__ == "__main__":
   # testPlots()
   createPercentageAnalysisColorPlot("SPD", "Mean")
