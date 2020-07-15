import matplotlib.pyplot as plt
import csv
import pandas as pd
from pandas import DataFrame
from mpl_toolkits.mplot3d import Axes3D
fields = ['a', 'b', 'counts']
df = pd.read_csv('parameter_sweep.csv',skipinitialspace=True, usecols=fields) 
print(df.head())
print(df.keys())
threedee = plt.figure().gca(projection='3d')
threedee.scatter(df.a, df.b, df.counts)
threedee.set_xlabel('a')
threedee.set_ylabel('b')
threedee.set_zlabel('counts error')
plt.show()

plt.scatter(df.a, df.counts)
plt.xlabel("a")
plt.ylabel("error")
plt.show()


plt.scatter(df.b, df.counts)
plt.xlabel("b")
plt.ylabel("error")
plt.show()

"""
X = df.a
Y = df.b
Z = df.counts

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.contour3D(X, Y, Z, 50, cmap='binary')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
"""
