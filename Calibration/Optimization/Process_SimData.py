"""
@author: Sadman Ahmed Shanto
usage:
    
"""
import numpy as np
import os
from Obj_Func_Comp import SimInfo
import matplotlib.pyplot as pt 
from matplotlib  import cm


def getABLStatsData(true_a, true_b, Lstring, phiString):
    """
    Lstring = string keyword that determines which Loss function to use. Options are {RMSE,SSE,MAE,SPD,}
    phiString = string keyword that determines which phi function to use. Options are {Mean, Identity, Amplitude, Std, Period, HybridPhi}
    returns: a parameters, b parameters, expected Loss eval, index position for true parameters
    """
    csv_folder = 'Param_Sweep/'
    test_folder = 'Test_Set/'
    csv_files = os.listdir(csv_folder)
    sim_info_dict = dict.fromkeys(csv_files)
    for csv_file in csv_files: 
            sim_info_dict[csv_file] = SimInfo(csv_folder=csv_folder,file_name=csv_file)
    a = true_a
    b = true_b
    csv_file_real = 'a-'+str(a)+'b-'+str(b)+'.csv'
    speed_true = np.loadtxt(test_folder+csv_file_real)
    for csv_file in csv_files: 
            sim_info_dict[csv_file].setRealSpeedsData(real_speed_data_new=speed_true)
    L_expectations = dict.fromkeys(csv_files)
    L_dist_vals = dict.fromkeys(csv_files)
    L_plot = [] #tuple of (a, b, expected_L,isRealParam)

    for csv_file in csv_files:
        sim_info =  sim_info_dict[csv_file]
        a_sim = sim_info.a
        b_sim = sim_info.b

        if Lstring == "RMSE":
            L = sim_info.getRMSE 
        elif Lstring == "MAE":
            L = sim_info.getMAE
        elif Lstring == "SSE":
            L = sim_info.getSSE
        elif Lstring == "SPD":
            L = sim_info.getSPD

        if phiString == "Mean":
            phi = sim_info.getMean
        elif phiString == "Identity":
            phi = sim_info.getIdentity
        elif phiString == "Amplitude":
            phi = sim_info.getAmplitude
        elif phiString == "Std":
            phi = sim_info.getStD
        elif phiString == "Period":
            phi = sim_info.getPeriod
        elif phiString == "HybridPhi":
            phi = sim_info.getHybridPhi

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


def getLStatsData(true_a, true_b, Lstring, phiString):
    """
    Lstring = string keyword that determines which Loss function to use. Options are {RMSE,SSE,MAE,SPD,}
    phiString = string keyword that determines which phi function to use. Options are {Mean, Identity, Amplitude, Std, Period, HybridPhi}
    returns: expected Loss eval, max Loss eval, min Loss eval, index position for true parameters
    """
    csv_folder = 'Param_Sweep/'
    test_folder = 'Test_Set/'
    csv_files = os.listdir(csv_folder)
    # put each siminfo into dict to then later reference
    sim_info_dict = dict.fromkeys(csv_files)
    for csv_file in csv_files: 
            sim_info_dict[csv_file] = SimInfo(csv_folder=csv_folder,file_name=csv_file)
    a = true_a
    b = true_b
    print(a,b)
    csv_file_real = 'a-'+str(a)+'b-'+str(b)+'.csv'
    speed_true = np.loadtxt(test_folder+csv_file_real)
    for csv_file in csv_files: 
            sim_info_dict[csv_file].setRealSpeedsData(real_speed_data_new=speed_true)
    L_expectations = dict.fromkeys(csv_files)
    L_dist_vals = dict.fromkeys(csv_files)
    L_plot = [] #tuple of (expected, max, min, isRealParam)

    for csv_file in csv_files:
        sim_info =  sim_info_dict[csv_file]
        if Lstring == "RMSE":
            L = sim_info.getRMSE 
        elif Lstring == "MAE":
            L = sim_info.getMAE
        elif Lstring == "SSE":
            L = sim_info.getSSE
        elif Lstring == "SPD":
            L = sim_info.getSPD

        if phiString == "Mean":
            phi = sim_info.getMean
        elif phiString == "Identity":
            phi = sim_info.getIdentity
        elif phiString == "Amplitude":
            phi = sim_info.getAmplitude
        elif phiString == "Std":
            phi = sim_info.getStD
        elif phiString == "Period":
            phi = sim_info.getPeriod
        elif phiString == "HybridPhi":
            phi = sim_info.getHybridPhi

        L_dist = sim_info.get_L_dist(L,phi) # vector of loss function evals: L(phi(X),phi(y))
        L_expect = sim_info.get_L_Expect(L,phi)
        L_expectations[csv_file] = L_expect
        L_dist_vals[csv_file] = L_dist
        if csv_file == csv_file_real:
            L_plot.append((L_expect,max(L_dist),min(L_dist),True))
        else:
            L_plot.append((L_expect,max(L_dist),min(L_dist),False))

    sorted_by_L_exp = sorted(L_plot, key=lambda tup: tup[0])
    x_L_expect = [i for i in range(len(L_plot))]
    L_exp = [i[0] for i in sorted_by_L_exp]
    L_max = [i[1] for i in sorted_by_L_exp]
    L_min = [i[2] for i in sorted_by_L_exp]
    TrueIndex = [i[3] for i in sorted_by_L_exp].index(True)
    return L_exp, L_max, L_min, TrueIndex


def createLossValuesPlot(true_a, true_b, Lstring, phiString):
    """
    Lstring = string keyword that determines which Loss function to use. Options are {RMSE,SSE,MAE,SPD,}
    phiString = string keyword that determines which phi function to use. Options are {Mean, Identity, Amplitude, Std, Period, HybridPhi}
    purpose: creates the Loss function statistics plot with true paramet point as red square
    """
    fig = pt.figure()
    L_exp, L_max, L_min, TrueIndex = getLStatsData(true_a, true_b, Lstring, phiString) 
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
    pt.show()
    pt.close(fig)


def createABLCountourPlot(true_a, true_b, Lstring, phiString): 
    """
    Lstring = string keyword that determines which Loss function to use. Options are {RMSE,SSE,MAE,SPD,}
    phiString = string keyword that determines which phi function to use. Options are {Mean, Identity, Amplitude, Std, Period, HybridPhi}
    purpose: creates the colored contour plot of tuple (a,b,L expected)
    """
    fig = pt.figure()
    a_vals, b_vals, L_vals, TrueIndex = getABLStatsData(true_a, true_b, Lstring, phiString)
    pt.scatter(a_vals, b_vals, c=L_vals)
    pt.annotate("True Point", (a_vals[TrueIndex], b_vals[TrueIndex]), rotation=60)
    pt.title("a: {}, b: {}".format(true_a, true_b))
    pt.colorbar()
    pt.xlabel("a values")
    pt.ylabel("b values")
    fig.savefig("figures/a-{}b-{}color.png".format(true_a,true_b), dpi=600)
    pt.show()
    pt.close(fig)


def getPercentageLessThanLTrue(true_a, true_b, Lstring, phiString): #horrible name I am sorry
    L_exp, L_max, L_min, TrueIndex = getLStatsData(true_a, true_b, Lstring, phiString) 
    totalPoints = len(L_exp)
    return (TrueIndex*100)/totalPoints


def createAllPossiblePlots(Lstring, phiString):
    """
    call this function to create L statistics and contour colored plots for all true parameter points 
    """
    true_as = [round(0.5+0.1*i,2) for i in range(9)]
    true_bs = [round(1.0+0.1*i,2) for i in range(6)]
    for i in range(len(true_as)):
        for j in range(len(true_bs)):
            createABLCountourPlot(true_as[i],true_bs[j], Lstring, phiString)
            createLossValuesPlot(true_as[i],true_bs[j], Lstring, phiString)


def createPercentageAnalysisColorPlot(LfuncName, PhiFuncName):
    """
    Lstring = string keyword that determines which Loss function to use. Options are {RMSE,SSE,MAE,SPD,}
    phiString = string keyword that determines which phi function to use. Options are {Mean, Identity, Amplitude, Std, Period, HybridPhi}
    purpose: creates the contour plot of tuple (a,b,percentage of L exp less than true param)
    """
    fig = pt.figure(figsize=(8.0, 5.0))
    true_as = [round(0.5+0.1*i,2) for i in range(9)]
    true_bs = [round(1.0+0.1*i,2) for i in range(6)]
    percentages = [] #tuple of (a,b,percentage_val)
    for i in range(len(true_as)):
        for j in range(len(true_bs)):
            percentages.append((true_as[i],true_bs[j],getPercentageLessThanLTrue(true_as[i],true_bs[j], LfuncName, PhiFuncName)))
    a_vals= [i[0] for i in percentages]
    b_vals= [i[1] for i in percentages]
    L_vals= [i[2] for i in percentages]
    x_vals = [i for i in range(len(a_vals))]
    pt.scatter(a_vals, b_vals, c=L_vals)
#    pt.scatter(a_vals[TrueIndex], b_vals[TrueIndex])
    pt.clim([0,100])
    pt.colorbar()
    score = round(sum(L_vals) /  (len(true_as)*len(true_bs)), 4)
    pt.title("Loss function: {}, Phi operator: {}, <L,Phi> score = {}".format(LfuncName, PhiFuncName, score))
    pt.xlabel("a values")
    pt.ylabel("b values")
    fig.savefig("figures/{}and{}color.png".format(LfuncName,PhiFuncName), dpi=600)
   # pt.show()
    pt.close(fig)


def createPercentageAnalysisPlot(LfuncName, PhiFuncName):
    """
    Lstring = string keyword that determines which Loss function to use. Options are {RMSE,SSE,MAE,SPD,}
    phiString = string keyword that determines which phi function to use. Options are {Mean, Identity, Amplitude, Std, Period, HybridPhi}
    purpose: creates the line plot of tuple (a,b,percentage of L exp less than true param)
    """
    fig = pt.figure(figsize=(8.0, 5.0))
    true_as = [round(0.5+0.1*i,2) for i in range(9)]
    true_bs = [round(1.0+0.1*i,2) for i in range(6)]
    percentages = [] #tuple of (a,b,percentage_val)
    for i in range(len(true_as)):
        for j in range(len(true_bs)):
            percentages.append((true_as[i],true_bs[j],getPercentageLessThanLTrue(true_as[i],true_bs[j], LfuncName, PhiFuncName)))
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
    fig.savefig("figures/{}and{}line.png".format(LfuncName,PhiFuncName), dpi=600)
    pt.show()


def testPlots(Lstring, phiString):
    """
    just to quick test some L and phi functions
    """
    createABLCountourPlot(1.3, 1.2, Lstring, phiString)
    createABLCountourPlot(0.5, 1.2, Lstring, phiString)
    createABLCountourPlot(1.1, 1.5, Lstring, phiString)
    createABLCountourPlot(0.7, 1.0, Lstring, phiString)
    createLossValuesPlot(1.3, 1.2, Lstring, phiString)
    createLossValuesPlot(0.5, 1.2, Lstring, phiString)
    createLossValuesPlot(1.1, 1.5, Lstring, phiString)
    createLossValuesPlot(0.7, 1.0, Lstring, phiString)

def createComparisonTimeSeriesPlot(a_vals, b_vals):
    csv_folder = 'Param_Sweep/'
    csv_files = ["a-"+str(a_vals[0])+"b-"+str(b_vals[0])+".csv","a-"+str(a_vals[1])+"b-"+str(b_vals[1])+".csv"]
    sim_info_dict = dict.fromkeys(csv_files)
    time_series_data = []
    for csv_file in csv_files:
            sim_info_dict[csv_file] = SimInfo(csv_folder=csv_folder,file_name=csv_file)
            time_series_data.append(sim_info_dict[csv_file].speedData)
    xvals = [30*i for i in range(len(time_series_data[0][0]))]
   # print(len(time_series_data[0][9]))
    
    pt.subplot(1,2,1)
    for i in range(len(time_series_data[0])):   
        pt.plot(xvals,time_series_data[0][i],'r')
    pt.xlabel("Time [s]")
    pt.ylabel("Speeds [m/s]")
    pt.ylim([0,20])
    pt.subplot(1,2,2)
    for i in range(len(time_series_data[1])):   
        pt.plot(xvals,time_series_data[1][i],'b')
    pt.xlabel("Time [s]")
    pt.ylabel("Speeds [m/s]")
    pt.ylim([0,20])
   # pt.savefig("_.png")
    pt.show()

if __name__ == "__main__":
    """
    createPercentageAnalysisColorPlot("MAE", "Std")
    createPercentageAnalysisColorPlot("MAE", "Amplitude")
    createPercentageAnalysisColorPlot("MAE", "HybridPhi")
    createPercentageAnalysisColorPlot("MAE", "Identity")
    createPercentageAnalysisColorPlot("MAE", "Period")
    """
    createComparisonTimeSeriesPlot([0.5,1.2], [1.3,1.3])
