import numpy as np
import maplotlib.pyplot as pt
import os
from scipy.optimize import minimize

#Error functions:

def RMSE(x,y):
	return np.sqrt(np.average(np.multiply((x-y),(x-y))))

def MAE(x,y):
	return np.average(np.abs(x-y))

def SSE(x,y):
	return np.sum(np.multiply((x-y),(x-y)))

def LS_fit_sin(t,x):
	'''
	Fits a sin wave to given measurements. 
	Seems extremely prone to the initial guess.
	'''


	def sample_sin(p):
		A = p[0]
		omega=p[1]
		phi = p[2]
		mu = p[3]

		x_sample = A*np.sin(omega*t + phi) + mu

		error = np.dot((x-x_sample),(x-x_sample))

		return error

	def LS_fit(p0):

		p_opt = minimize(sample_sin,p0)

		return p_opt

	p_opt = LS_fit(p0)

	return p_opt

def absolute_amplitude_diff(x,y):
	amplitude_x = np.max(x)-np.min(x)
	amplitude_y = np.max(y)-np.min(y)
	return np.abs(amplitude_y-amplitude_x)

def getFFT(x):
	fidelity = 30
	f = data
	t = [fidelity*i for i in range(len(f))]
	n = len(t) 
	fhat = np.fft.fft(f,n)

	PSD = fhat * np.conj(fhat) / n

	return PSD

def get_All_FFT(x_vals):
	f_vals = []
	for x in list(x_vals):
		f_vals.append(getFFT(x))
	return np.array(f_vals)

#For loading in data:

def get_csv_list(data_directory):
	files = os.listdir(data_directory)
	csv_files = []
	for file in files:
		if(file[-3:]=='csv'):
			csv_files.append(file)

	return csv_files

def load_all_csvs():
	csv_files = get_csv_list()
	data = dict.fromkeys(csv_files)
	for file in csv_files:
		speed_data = np.loadtxt(file)
		data[file] = speed_data
	return data

def get_params_from_csv_list(csv_list):
	params = dict.fromkeys(csv_list)
	for file_name in csv_list:
		a_pos = 2
		b_pos = a_pos
		while(file_name[b_pos] != 'b'):
			b_pos += 1
		b_pos += 2

		a_val = float(file_name[a_pos:b_pos-2])

		b_val = float(file_name[b_pos:-4])

		return [a_val,b_val]

#Use error functions and process data:

def per_sim_eval_data_set(x_vals,y,error_metric):
	evals = []
	for i in range(len(x_vals)):
		x = x_vals[i,:]
		evals.append(error_metric(x,y))
	return evals

def hist_subplot(x_val_list,y,error_metric,xlim=[0,8],ylim=[0,15],title_list=None):
	'''Not finished'''
	num_sims = len(x_val_list)
	error_list = []
	for x_vals in x_val_list:
		error = per_sim_eval_data_set(x_vals,y,error_metric)
		error_list.append(error)
	pt.figure()
	for i in range(num_sims):
		pt.subplot()

def assess_data_list(x_val_list,y,error_metric):
	assess_list = []
	for x_vals in x_val_list:
		assess_val = per_sim_eval_data_set(x_vals,y,error_metric)
		assess_list.append(assess_val)
	return assess_list

def get_true_distr(x_val,error_metric,true_index=0):
	true_val = x_val[true_ind,true_index]


