"""
@author: Sadman Ahmed Shanto
"""
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

dataFile = "varying_a_speeds.csv"
fidelity = 30

def getTimeSeries(data):
    f = data
    t = [fidelity*i for i in range(len(f))]
    dt = fidelity
    return f,t,dt

def getFFT(data,a_label):
    f,t,dt = getTimeSeries(data)
    n = len(t) 
    fhat = np.fft.fft(f,n)
    PSD = fhat * np.conj(fhat) / n
    freq = (1/(dt*n)) * np.arange(n)
    L = np.arange(1,np.floor(n/2),dtype="int") #for plotting first half (symmetry)
    sns.set_palette(sns.color_palette("hls", 50))
   # plt.title("Fast Fourier Transform of Speeds Data")
    plt.plot(freq[L],PSD[L],label="a = {}".format(a_label))
    plt.plot(freq[L],PSD[L])
    plt.xlim(freq[L[0]],freq[L[-1]])
    plt.xlabel("Frequency")
    plt.ylabel("Power Spectrum")
    plt.legend()

if __name__ ==  "__main__":
    a_range = [0.3,2.0]
    num_a_samples = 18
    num_per_param_samples = 1
    a = np.linspace(a_range[0],a_range[1],num_a_samples,endpoint=True)
    df = pd.read_csv(dataFile)
    count = 0
    for row in df.itertuples(index = True, name ='Pandas'):
        getFFT(np.array(row),a[count])
        count+=1
    plt.show()
