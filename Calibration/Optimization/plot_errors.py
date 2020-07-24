import numpy as np
import pandas as pd
import csv, time
import matplotlib.pyplot as plt

class ErrorPlotter:

    def __init__(self,csv_file1,csv_file2,numParams):
        self.f1 = csv_file1
        self.f2 = csv_file2
        self.timestr = time.strftime("%Y%m%d_%H%M%S")
        self.readEvery = 1
        self.columns = 2
        self.num_sim = 5
        self.numParams = numParams
    
    def plotErrorForSingleParam(self):
        errors = []
        params = []
        with open(self.f1, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            for lines in csv_reader:
                param = lines[1].split("[")[1].split("]")[0]
                errors.append(float(lines[0]))
                params.append(float(param))
        errors = errors[::self.readEvery]  #every other term
        params = params[::self.readEvery]
        x = [i+1 for i in range(len(errors))]
        figplt = plt.plot(x, errors, '--o')
        num = self.readEvery*(len(errors)) -  1
        plt.ylabel("Error")
        plt.xlabel("Iteration")
        plt.title("Initial [v0, T]: " + str(params[0]) + " Final [v0,T]: " + str(params[-1])+"\n Iterations: " + str(num))
        for i, txt in enumerate(params):
            plt.annotate(txt, (x[i], errors[i]))
        plt.savefig("figures/error_latest_"+self.timestr+".png")
        plt.show()
        #return figplt

if __name__ == "__main__":
    error = ErrorPlotter("data/joint_rmse_error1.csv", "data/lamda_error_vector.csv",1)
    error.plotErrorForSingleParam()
    """
    f1 = error.plotErrorForSingleParam()
    error1 = ErrorPlotter("data/mean_rmse1.csv", "data/lamda_error_vector.csv", 1)
    f2 = error1.plotErrorForSingleParam()
    error2 = ErrorPlotter("data/rmse_mean1.csv", "data/lamda_error_vector.csv", 1)
    f3 = error2.plotErrorForSingleParam()
    plt.legend(["obj func","mean RMSE","RMSE mean_vect"])
    plt.show()
    """