import matplotlib.pyplot as plt
import csv
import pandas as pd
from pandas import DataFrame

df = pd.read_csv('main_data.csv', names = ['a', 'b', 'mean_counts', 'std_counts', 'counts_error', 'mean_speed', 'std_speed', 'speed_error'])
print(df.head())
print(df["mean_speed"])

df.plot(x='a', y='mean_speed')
plt.ylabel("Average Speed")
plt.show()

df.plot(x='a', y='mean_counts')
plt.ylabel("Average Counts")
plt.show()

df.plot(x='a', y='std_speed')
plt.ylabel("Standard Deviation Speed")
plt.show()

df.plot(x='a', y='std_counts')
plt.ylabel("Standard Deviation Counts")
plt.show()

df.plot(x='a', y='speed_error')
plt.ylabel("Error in Speed")
plt.show()

df.plot(x='a', y='counts_error')
plt.ylabel("Error in Counts")
plt.show()
