import numpy as np
from from scipy.spatial import distance import jensenshannon as JS_dist



def ecdf(data):
    """ Compute ECDF """
    x = np.sort(data)
    n = x.size
    y = np.arange(1, n+1) / n
    return(x,y)

def get_binned_probabilities(num_bin,)

def calc_JS_dist(p,q):