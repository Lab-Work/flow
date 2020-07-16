import numpy as np
import random, csv, time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

speeds = np.array( list(np.array([12,14,15.41])), list(np.array([11,18,21.123])), list(np.array([0,8,18.6])) )
a_vals = np.array([1,2,3])
c = a_vals
colors = plt.cm.coolwarm(c)
for i in range(len(a_vals)):
    plt.plot([x for x in range(speeds[i])], speeds[i], edgecolors=colors)
plt.ylabel('Average Speeds [m/s]')
plt.xlabel('Measurement Number')
plt.title('Affects of varying a')
plt.show()














"""

x = np.array([1,2,3,4,53,21])

def eror(vals, isCounts, stdv):
    if isCounts:
        y = np.round(np.random.normal(vals,stdv))
        return np.where(y<0, 0, y) 
    else:
        y = np.random.normal(vals,stdv)
        return np.where(y<0, 0, y) 

#print(eror(x, True, 3))
#print(eror(x, False, 4))

def plotErrors(error):
    timestr = time.strftime("%Y%m%d_%H%M%S")
    csvName = "error" + ".csv"
    with open(csvName, "a") as file:
        writer = csv.writer(file)
        writer.writerow([error])

#plotErrors(12)
#plotErrors(123)
#plotErrors(3)
#plotErrors(10)


def animate():
    graph_data = open('error.csv','r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    i = 0
    for line in lines:
        i += 1
        if len(line) > 1:
            x = float(line)
            xs.append(float(x))
            ys.append(i)
    plt.plot(ys, xs)
    plt.ylabel("Error")
    plt.xlabel("Iteration")
    plt.show()

#animate()

def adjustSize(sim, real):
      while len(real) > len(sim):
          real.pop()
      while len(sim) > len(real):
          sim.pop()
      print(len(real))
      print(len(sim))
      return [sim,real]

sim = [1,2,3,4,5,6,70,1,12]
real = [0,1,2,3,4,5,6,2,1,12,22,7]

x,y = adjustSize(sim,real)

print(x)
print(y)

"""
