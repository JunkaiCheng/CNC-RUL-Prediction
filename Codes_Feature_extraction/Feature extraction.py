#--------------------------package-------------------------
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

#------------------------function------------------------
from DataProcessing import PSD
from DataProcessing import PSDextract
from DataProcessing import PSDExtract_s2e
from DataProcessing import Calcmean

#--------------------------Read plc.csv---------------------------------

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
    # if fileindex < 30 or fileindex > 46:
    # #if fileindex != 20:
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
                #dataset_y.append(float(signals[1]))
                #dataset_z.append(float(signals[2]))
                pivot += 1
    dataset[fileindex].append(dataset_x)
    #dataset[fileindex].append(dataset_y)
    #dataset[fileindex].append(dataset_z)
    fileindex += 1



PSDdata_Interval = 10000
Fs = 25600


PSD_x= []
Beta = []
#data_x = dataset[20][0]
for i in range(1, 47, 1):
    if i == 25:
        continue
    data_x = dataset[i][0]
    # # ------x axis-------
    # x_length = int(len(data_x) / PSDdata_Interval)
    #
    # for j in range(x_length - 1):
    #     data = data_x[PSDdata_Interval * j:PSDdata_Interval * (j + 1)]
    #     N = len(data)
    #     data_x_PSD = PSD(data, N, Fs)
    #     data_x_PSD_list = data_x_PSD.tolist()
    #     maxindex = data_x_PSD_list.index(max(data_x_PSD_list))
    #     print(maxindex*Fs/N)
    #
    #     first_harmonic = max(data_x_PSD_list)
    #     second_harmonic = data_x_PSD_list[(maxindex + 1) * 2 - 1]
    #     third_harmonic = data_x_PSD_list[(maxindex + 1) * 3 - 1]
    #
    #     har_num = 5 # second - fifth
    #     harmonic = []
    #     for k in range(1, har_num, 1):
    #         har = abs(data_x_PSD_list[(maxindex + 1) * (k + 1) - 1])
    #         harmonic.append(har)
    #     harmonic_sum = sum(harmonic)
    #
    #
    #     beta = 10 * math.log(harmonic_sum/abs(first_harmonic))
    #     Beta.append(beta)
    #     # data_x_PSD_dB = np.log(data_x_PSD) * 10
    #     # F = list(map(lambda x: (x-1)*Fs/N, list(range(N+1))))
    #     # plt.plot(F[0:int(N/2)], data_x_PSD_dB)
    #     # plt.show()
    #
    #     #x_PSD_result = PSDExtract_s2e(data_x_PSD, N, Fs, 97, 103)
    #     #x_PSD_result = math.log(x_PSD_result) * 10  # dB
    #     #PSD_x.append(x_PSD_result)
    data = data_x
    N = len(data)
    data_x_PSD = PSD(data, N, Fs)
    data_x_PSD_list = data_x_PSD.tolist()
    maxindex = data_x_PSD_list.index(max(data_x_PSD_list))
    print(maxindex*Fs/N)

    first_harmonic = max(data_x_PSD_list)
    second_harmonic = data_x_PSD_list[(maxindex + 1) * 2 - 1]
    third_harmonic = data_x_PSD_list[(maxindex + 1) * 3 - 1]

    har_num = 5 # second - fifth
    harmonic = []

    for k in range(1, har_num, 1):
        har = abs(data_x_PSD_list[(maxindex + 1) * (k + 1) - 1])
        harmonic.append(har)

    harmonic_sum = sum(harmonic)


    beta = 10 * math.log(abs(second_harmonic)/abs(first_harmonic)**2)
    Beta.append(beta)

X = range(len(Beta))
plt.plot(X, Beta)
plt.show()
