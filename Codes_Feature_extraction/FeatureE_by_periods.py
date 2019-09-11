#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[2]:


#--------------------------package---------------------------
import json
import os
import pandas as pd
import csv
from sklearn import linear_model
from sklearn.metrics import r2_score
import pylab as pl
import scipy.signal as signal
from scipy import fftpack
from scipy.fftpack import fft,ifft
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import animation
import math
#import obspy as obs
mpl.use('TkAgg')

#------------------------variable-----------------------
from PLC_process import filter_data
from PLC_process import csv_no
from PLC_process import number_csv_no
from PLC_process import dataset_z

#------------------------function------------------------
from DataProcessing import PSD
from DataProcessing import PSDextract




#---------------------------------------------MAIN---------------------------------------------
pivot = 0
fileindex = 0
dataset = [[] for _ in range(48)]
#dataset: 48*?
#?: [ [data_x], [data_y], [data_z] ]

path="Sensor/01-qLua/01/" #the directory of data readed

path_list = os.listdir(path)
path_list.sort(key=lambda x: int(x[:-4])) #sort filenames, e.g. 1.csv, put away '.csv', then sort by number


for filename in path_list:
    pivot = 0
    dataset_x = []
    dataset_y = []
    dataset_z = []
    # if fileindex != 5:
    #     fileindex += 1
    #     continue
    with open(path + filename, 'r') as file:
        csv_file = csv.reader(file)
        for signals in csv_file:
            if pivot == 0:
                pivot += 1
            else:
                if len(signals[0]) == 0 or len(signals[1]) == 0 or len(signals[2]) == 0:
                    #print('Error data: ' + path + filename + ' ' + str(pivot))
                    #print(signals)
                    pivot += 1
                    continue
                if abs(float(signals[0])) > 1000 or abs(float(signals[1])) > 1000 or abs(float(signals[2])) > 1000:
                    #print('Error data: ' + path + filename + ' ' + str(pivot))
                    #print(signals)
                    pivot += 1
                    continue
                dataset_x.append(float(signals[0]))
                dataset_y.append(float(signals[1]))
                dataset_z.append(float(signals[2]))
                pivot += 1
    dataset[fileindex].append(dataset_x)
    dataset[fileindex].append(dataset_y)
    dataset[fileindex].append(dataset_z)
    fileindex += 1


# In[3]:


test_data_0degree = filter_data[0] #0 degree
Fs = 25600

def CompressFilterData(filter_data):
    # data form: [ [3, 996], [3, 997], [3, 998],......,[4, 305],......,[14, 196],...... ]
    filter_data_new = []
    sign = 0
    for i in range(len(filter_data)):
        if sign == 0:
            fileindex = filter_data[i][0]
            dataindex = filter_data[i][1]
            start = filter_data[i][1]
            end = start + 1
            sign = 1
            continue
        if filter_data[i][0] == fileindex and filter_data[i][1] == dataindex + 1:
            dataindex = filter_data[i][1]
            if i == len(filter_data) - 1:
                end = dataindex
                temp = [fileindex, start, end]
                filter_data_new.append(temp)
        else:
            end = dataindex
            temp = [fileindex, start, end]
            filter_data_new.append(temp)
            fileindex = filter_data[i][0]
            dataindex = filter_data[i][1]
            start = filter_data[i][1]
            end = start + 1
    return filter_data_new


# In[4]:


test_data_0degree_new = CompressFilterData(test_data_0degree)

result3380_3480 = []
result3650_3750 = []
result4150_4250 = []
result4425_4525 = []
result7240_7340 = []
result7785_7885 = []
result8050_8150 = []
result8600_8700 = []

for i in range(len(test_data_0degree_new)):
    file_index = test_data_0degree_new[i][0]  # 3
    signal_index_start = test_data_0degree_new[i][1]  # 996
    signal_index_end = test_data_0degree_new[i][2] # 1008
    cut_index_start = int(signal_index_start / number_csv_no[file_index - 1] * len(dataset[file_index - 1][0])) #x-axis
    cut_index_end = int((signal_index_end + 1) / number_csv_no[file_index - 1] * len(dataset[file_index - 1][0])) #x-axis
    data = dataset[file_index - 1][0][cut_index_start:cut_index_end]  # x-axis data in 3.csv
    N = len(data)
    dataPSD = PSD(data, N, Fs)
    dataPSD = np.array(dataPSD)
    
    F = list(map(lambda x: (x - 1) * Fs / N, list(range(N + 1))))
    plt.plot(F[0:int(N/2)], np.log(dataPSD[0:int(N/2)])*10, ".")
    plt.savefig("./fig/" + str(i) + ".png")
    plt.cla()
    
    printlist = []
    for j in range(len(dataPSD[0:int(N/2)])):
        if (np.log(dataPSD[0:int(N/2)])*10)[j] > -15:
            printlist.append(j/N*Fs)
    
    
    jj = 0
    while jj < len(printlist):
        if printlist[jj] < 3000.0:
            del printlist[jj]
            jj -= 1
        jj += 1
            
    print(printlist)
    
    
    result33803480 = PSDExtract_s2e(dataPSD, N, Fs, 3400, 3500)
    #result33803480 = math.log(result33803480)*10
    result3380_3480.append(result33803480)
    
    result36503750 = PSDExtract_s2e(dataPSD, N, Fs, 3700, 3800)
    #result36503750 = math.log(result36503750) * 10
    result3650_3750.append(result36503750)
    
    result41504250 = PSDExtract_s2e(dataPSD, N, Fs, 4200, 4300)
    #result41504250 = math.log(result41504250) * 10
    result4150_4250.append(result41504250)
    
    result44254525 = PSDExtract_s2e(dataPSD, N, Fs, 4500, 4600)
    #result44254525 = math.log(result44254525) * 10
    result4425_4525.append(result44254525)
    
    result72407340 = PSDExtract_s2e(dataPSD, N, Fs, 7300, 7400)
    #result72407340 = math.log(result72407340) * 10
    result7240_7340.append(result72407340)
    
    result77857885 = PSDExtract_s2e(dataPSD, N, Fs, 7800, 7900)
    #result77857885 = math.log(result77857885) * 10
    result7785_7885.append(result77857885)
    
    result80508150 = PSDExtract_s2e(dataPSD, N, Fs, 8100, 8200)
    #result80508150 = math.log(result80508150) * 10
    result8050_8150.append(result80508150)
    
    result86008700 = PSDExtract_s2e(dataPSD, N, Fs, 8600, 8700)
    #result86008700 = math.log(result86008700) * 10
    result8600_8700.append(result86008700)

    # if result < 0.25:
    #     print("Z-data test: ")
    #     print("fileindex: " + str(file_index))
    #     print("cut_index_start; " + str(cut_index_start))
    #     print("cut_index_end" + str(cut_index_end))
    #     print(" ")



# error_data = test_data_0degree[40:50]
# print(error_data)
# z_test = []
#
# for i in range(len(error_data)):
#     index = sum(list(map(lambda x: number_csv_no[x], list(range(0, error_data[i][0] - 1, 1))))) + error_data[i][1]
#     z_test.append(dataset_z[index])
#
# plt.subplot(221)
# z_test_x = range(len(z_test))
# plt.plot(z_test_x, z_test)


# In[31]:


#-----------------------------plot 8 special Hz points--------------------------
X = range(len(test_data_0degree_new))

plt.title("3380-3480")
plt.plot(X, result3380_3480, "r.")
plt.savefig("./fig_8PSD_peak/3380_3480.png")
plt.cla()

plt.title("3650-3750")
plt.plot(X, result3650_3750, "r.")
plt.savefig("./fig_8PSD_peak/3650_3750.png")
plt.cla()

plt.title("4150-4250")
plt.plot(X, result4150_4250, "r.")
plt.savefig("./fig_8PSD_peak/4150_4250.png")
plt.cla()

plt.title("4425-4525")
plt.plot(X, result4425_4525, "r.")
plt.savefig("./fig_8PSD_peak/4425_4525.png")
plt.cla()

plt.title("7240-7340")
plt.plot(X, result7240_7340, "r.")
plt.savefig("./fig_8PSD_peak/7240_7340.png")
plt.cla()

plt.title("7785-7885")
plt.plot(X, result7785_7885, "r.")
plt.savefig("./fig_8PSD_peak/7785_7885.png")
plt.cla()

plt.title("8050-8150")
plt.plot(X, result8050_8150, "r.")
plt.savefig("./fig_8PSD_peak/8050_8150.png")
plt.cla()

plt.title("8600-8700")
plt.plot(X, result8600_8700, "r.")
plt.savefig("./fig_8PSD_peak/8600_8700.png")
plt.cla()

