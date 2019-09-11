#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[2]:


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

#--------------------------split the files by its TimeStamp-----------------------
def TimeStampSplit(str):
    #input string of timestamp
    #output a nubmer that can be used to compare timestamp
    datesplit = str.split(' ')
    date = datesplit[0]
    time = datesplit[1]

    YMDsplit = date.split('-')
    year = float(YMDsplit[0])
    month = float(YMDsplit[1])
    day = float(YMDsplit[2])

    timesplit = time.split(':')
    hour = float(timesplit[0])
    minute = float(timesplit[1])
    second = float(timesplit[2])

    return year * 1000000 + month * 100000 + day * 1000 + hour * 10 + minute * 0.1 + second * 0.001

#--------------------------concatenate dataset by S0x (Json version)------------------------
def concatDataset(list, start, end):
    #input the list & start dict & end dict
    #output concatenated dataSet of the list
    dataset_cat_S01 = []
    dataset_cat_S02 = []
    dataset_cat_S03 = []
    for i in range(end-start+1):
        for j in range(4):
            if list[start + i]['data'][j]['signalName'] == 'S01':
                dataset_cat_S01 = dataset_cat_S01 + list[start + i]['data'][j]['dataSet']
            elif list[start + i]['data'][j]['signalName'] == 'S02':
                dataset_cat_S02 = dataset_cat_S02 + list[start + i]['data'][j]['dataSet']
            elif list[start + i]['data'][j]['signalName'] == 'S03':
                dataset_cat_S03 = dataset_cat_S03 + list[start + i]['data'][j]['dataSet']
    return dataset_cat_S01, dataset_cat_S02, dataset_cat_S03


#--------------------------Envelope & Hibert Transformation-------------------------
#t = np.arange(0, start-end+1, 1/25600.0)
def plotEnvelope(data):
    pl.subplot(221)
    original_data = np.array(data)
    pl.plot(original_data, label=u"Original_data")
    pl.legend()
    pl.subplot(222)
    hx_original = fftpack.hilbert(original_data)
    envelope1 = np.sqrt(original_data**2 + hx_original**2)
    pl.plot(envelope1, "r", linewidth=2, label=u"Envelope1")
    pl.title(u"Hilbert Transform")
    pl.legend()
    pl.show()


#----------------------------Calculate the means----------------------------------
def Calcmean(data, L, interval):
    #data is the set
    #L presents how many of the data will be calculated for mean, int
    #l presents the interval of data chosen, which sparse the dataset, int
    data_mean = []
    data = np.array(data)
    for i in range(len(data)):
        if i % interval == 0 and i != 0:
            if i > L:
                mean = np.mean(data[i-L+1:i+1])
                data_mean.append(mean)


    return data_mean

#----------------------------Calculate R-square------------------------------------
def CalcR2(data1, data2):
    #data1, data2 are ndarray
    SStot = np.sum((data1 - np.mean(data1)) ** 2)
    SSres = np.sum((data1 - data2) ** 2)
    R2 = 1-SSres/SStot
    return R2

#----------------------------Calculate correlation coefficient-------------
def Calccorr(data1, data2):
    # data1, data2 are ndarray
    data1 = data1.flatten().tolist()
    data2 = data2.flatten().tolist()
    data1 = pd.Series(data1)
    data2 = pd.Series(data2)
    corr_coef = data1.corr(data2)
    corr_coef = -1 * math.log(1-corr_coef*corr_coef, 10)
    return corr_coef

#----------------------------Linear regression--------------------------------------
def LinearReg(data, L, interval):
    #data is the set of mean
    #L presents how many of the data will be calculated for mean, int
    #l presents the interval of data chosen, which sparse the dataset, int
    data = np.array(data)
    linearLength = int(L/interval)
    X = np.array(range(1, linearLength+1, 1)).reshape(-1, 1)
    Corr = []
    for i in range(len(data)-linearLength+1): #len(data)-linearLength+1
        datasets = data[i:(i+linearLength)]
        datasets = datasets.reshape(-1, 1)
        #model = linear_model.LinearRegression()
        #model.fit(X, datasets)
        #slope = model.coef_[0][0]
        #intercept = model.intercept_[0]
        #data_pred = datasets * slope + intercept
        corr = Calccorr(datasets, X)
        Corr.append(corr)

    Corr = np.array(Corr)

    return Corr, linearLength

#---------------------------Separate Working period---------------------
def SeparatePeriod(dataset, linearLength, Corr, threshold=2.9):
    #Corr is the list of correlation coefficients after the linear calculation
    #threshold is to distinguish the starts and ends of period
    LeftIndex = []
    RightIndex = []
    ascentIndex = []
    descentIndex = []
    sign = 0
    Corr_list = Corr.tolist()
    for i in range(len(Corr)):
        if Corr[i] > threshold and sign == 0:
            LeftIndex.append(i)
            sign = 1
        elif Corr[i] < threshold and sign == 1:
            RightIndex.append(i)
            sign = 0

    for i in range(len(LeftIndex)):
        peak = Corr_list.index(max(Corr[LeftIndex[i]:RightIndex[i]]))
        if dataset[peak] < dataset[peak+1]:
            ascentIndex.append(peak)
        else:
            descentIndex.append(peak)
    return ascentIndex, descentIndex


#---------------------------PSD------------------------------
def PSD(data, N, Fs):
    #data is the signal data in time domain
    #N is the number of sample points
    #Fs is the sample rate
    Y = fft(data)
    Ayy = abs(Y)

    Ayy = Ayy/(N/2) #the practical amplitude
    Ayy[0] = Ayy[0]/2
    F = list(map(lambda x: (x-1)*Fs/N, list(range(N+1)))) #the practical frequency
    # pl.subplot(335)
    # pl.plot(F[0:int(N/2)], np.log(Ayy[0:int(N/2)])*10)
    # return Ayy[0:int(N)]
    return Ayy[0:int(N/2)]


#-----------------------------PSD extraction----------------------
def PSDextract(FreqInterval, dataPSD, N, Fs):
    #FreqInterval is the interval we set up to distinguish the feature frequency
    #dataPSD is the amplitude in frequency domain versus 0-Fs/2, which haven't been squared (equal to energy)
    PSDlist = []
    dataPSD_list = dataPSD.tolist()
    for i in range(int(Fs/2/FreqInterval)):
        result = sum([k*k for k in dataPSD_list[int(FreqInterval*i*N/Fs): int(FreqInterval*(i+1)*N/Fs)]])
        PSDlist.append(result)
    PSDlist = [k/sum(PSDlist) for k in PSDlist]
    return np.array(PSDlist) #PSDlist[0] means the energy percentage of 0-100Hz (0-FreqInterval*1 Hz)


#----------------------------Read data from json--------------------------------
# path="./20190703-1/"
# path_list = os.listdir(path)
# file_list=[]
# for filename in path_list:
#     with open('./' + path + filename, 'r') as file:
#         load_dict = json.load(file)
#         file_list.append(load_dict)
#
# file_list_sorted = sorted(file_list, key=lambda x:TimeStampSplit(x['dataTimeStamp'])) # sort the files by their dataTimeStamp
# start = 0 #number of files
# end = 9
# dataset_cat_S01, dataset_cat_S02, dataset_cat_S03 = concatDataset(file_list_sorted, start, end) #list


# In[3]:


#--------------------------Read csv-------------------------------------------



#---------------------------------------------------MAIN------------------------------------------------------------
pivot = 0
fileindex = 0
dataset = [[] for _ in range(48)]
#dataset: 48*?
#?: [ [data_x], [data_y], [data_z] ]


path="Sensor/01-qLua/01/" #the directory of data readed
# with open('./Output/' + 'output-r1el-04.csv', 'a', newline='') as labelout: #the directory of data written
#     csv_write = csv.writer(labelout, dialect='excel')
#     Label = ['#', 'RUL(min)']
#     for i in range(128):
#         name = str(i*100) + ' - ' + str((i+1)*100)+ 'Hz' + ' (x-axis)'
#         Label.append(name)
#     for i in range(128):
#         name = str(i*100) + ' - ' + str((i+1)*100)+ 'Hz' + ' (y-axis)'
#         Label.append(name)
#     for i in range(128):
#         name = str(i*100) + ' - ' + str((i+1)*100)+ 'Hz' + ' (z-axis)'
#         Label.append(name)
#     csv_write.writerow(Label)

path_list = os.listdir(path)
path_list.sort(key=lambda x: int(x[:-4])) #sort filenames, e.g. 1.csv, put away '.csv', then sort by number
for filename in path_list:
    pivot = 0
    dataset_x = []
    dataset_y = []
    dataset_z = []
#     if fileindex != 40:
#         fileindex += 1
#         continue
    with open(path + filename, 'r') as file:
        csv_file = csv.reader(file)
        for signals in csv_file:
            if pivot == 0:
                pivot += 1
            else:
                if len(signals[0]) == 0 or len(signals[1]) == 0 or len(signals[2]) == 0:
                    print('Error data: ' + path + filename + ' ' + str(pivot))
                    print(signals)
                    pivot += 1
                    continue
                if abs(float(signals[0])) > 1000 or abs(float(signals[1])) > 1000 or abs(float(signals[2])) > 1000:
                    print('Error data: ' + path + filename + ' ' + str(pivot))
                    print(signals)
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


# In[11]:


#--------------------------global variables------------------------------
#Some global variables are defined here
data_x = dataset_x  #datasets of vibration signals of x,y,z axis
data_y = dataset_y
data_z = dataset_z
L = 10000 #the length of data about mean filter
interval = 40 #the times that data contract by when calculating the mean
Fs = 25600 #the sample rate
FreqInterval = 100 #The frequency interval of PSD
PSDdata_Interval = 10000

#------------------------------------data Processing-------------------------------------

#------------------------------mean filter to separate periods-----------------------
# data_x_abs = list(map(abs, data_x))
# dataset_x_mean = Calcmean(data_x_abs, L, interval)
#
# pl.subplot(331)
# data_x_abs = np.array(data_x_abs)
# pl.plot(data_x_abs)
#
# pl.subplot(332)
# dataset_x_mean = np.array(dataset_x_mean) #data after mean filter
# pl.plot(dataset_x_mean)
#
# Corr, linearLength = LinearReg(dataset_x_mean, L, interval) #correlation coefficient per L points
# pl.subplot(333)
# pl.plot(Corr)
#
#
# ascentIndex, descentIndex = SeparatePeriod(dataset_x_mean, linearLength, Corr)
#
# Workingdata = data_x[(interval*(ascentIndex[0]+linearLength)+L):(interval*descentIndex[0]+L)] #Working data at #1 period
#
# pl.subplot(334)
# pl.plot(Workingdata)



def PSDExtract_s2e(dataPSD, N, Fs, start, end):
    PSDlist = []
    dataPSD_list = dataPSD.tolist()
    startindex = int(math.floor(start/(Fs/N)))
    endindex = int(math.floor(end/(Fs/N)))
    
    result = sum([k * k for k in dataPSD_list[startindex: endindex]])
   
    return result


#---------------------------------PSD feature extraction------------------------------------


PSD_x_97_103 = []
PSD_y_97_103 = []
PSD_z_97_103 = []
for i in range(0, 12, 1):
    data_x = dataset[i][0]
    data_y = dataset[i][1]
    data_z = dataset[i][2]
    PSD_x_97_103 = []
    PSD_y_97_103 = []
    PSD_z_97_103 = []
    
    #------x axis-------
    x_length = int(len(data_x)/PSDdata_Interval)
    for j in range(x_length-1):
        N = len(data_x)
        data_x_PSD = PSD(data_x[PSDdata_Interval*j:PSDdata_Interval*(j+1)], N, Fs)
        x_PSD_result = PSDExtract_s2e(data_x_PSD, N, Fs, 97, 103)
        if x_PSD_result == 0:
            continue
        x_PSD_result = math.log(x_PSD_result)*10 #dB
        PSD_x_97_103.append(x_PSD_result)
        
    #------y axis------- 
    y_length = int(len(data_y)/PSDdata_Interval)
    for jj in range(y_length-1):
        N = len(data_y)
        data_y_PSD = PSD(data_y[PSDdata_Interval*jj:PSDdata_Interval*(jj+1)], N, Fs)
        y_PSD_result = PSDExtract_s2e(data_y_PSD, N, Fs, 97, 103)
        if y_PSD_result == 0:
            continue
        y_PSD_result = math.log(y_PSD_result)*10 #dB
        PSD_y_97_103.append(y_PSD_result)
    
    #------z axis-------
    z_length = int(len(data_z)/PSDdata_Interval)
    for jjj in range(z_length-1):
        N = len(data_z)
        data_z_PSD = PSD(data_z[PSDdata_Interval*jjj:PSDdata_Interval*(jjj+1)], N, Fs)   
        z_PSD_result = PSDExtract_s2e(data_z_PSD, N, Fs, 97, 103)
        if z_PSD_result == 0:
            continue
        z_PSD_result = math.log(z_PSD_result)*10 #dB
        PSD_z_97_103.append(z_PSD_result)
    
    plt.title("X-axis: 97-103Hz" + "file " + str(i+1))
    X = range(len(PSD_x_97_103))
    plt.plot(X, PSD_x_97_103)
    plt.savefig("./fig97_103/" +  "x_file " + str(i+1) + ".png")
    plt.cla()
    
    plt.title("Y-axis: 97-103Hz" + "file " + str(i+1))
    Y = range(len(PSD_y_97_103))
    plt.plot(Y, PSD_y_97_103)
    plt.savefig("./fig97_103/" +  "y_file " + str(i+1) + ".png")
    plt.cla()
    
    plt.title("Z-axis: 97-103Hz" + "file " + str(i+1))
    Z = range(len(PSD_z_97_103))
    plt.plot(Z, PSD_z_97_103)
    plt.savefig("./fig97_103/" +  "z_file " + str(i+1) + ".png")
    plt.cla()



# plt.subplot(221)
# plt.title("X-axis: 97-103Hz")
# X = range(len(PSD_x_97_103))
# plt.plot(X, PSD_x_97_103)

# plt.subplot(222)
# plt.title("Y-axis: 97-103Hz")
# Y = range((len(PSD_y_97_103))
# plt.plot(Y, PSD_y_97_103)

# plt.subplot(223)
# plt.title("Z-axis: 97-103Hz")
# Z = range((len(PSD_z_97_103))
# plt.plot(Z, PSD_z_97_103)

#plt.show()

# # ------------------x-axis-------------------- #unitTime Workingdata_tmp N_tmp
    
# Workingdata = data_x
# N = len(Workingdata)
# unitTime = 500 #7200
# for i in range(unitTime):
#     Workingdata_tmp = Workingdata[int(i/unitTime*N):int((i+1)/unitTime*N)]
#     N_tmp = len(Workingdata_tmp)
#     pl.subplot(221)
#     pl.plot(Workingdata_tmp)
#     dataPSD = PSD(Workingdata_tmp, N_tmp, Fs) #data of PSD
#     pl.subplot(222)
#     pl.plot(dataPSD)
#     pointnum = int(FreqInterval/(Fs/N_tmp))
#     PSDlist_x = PSDextract(FreqInterval, dataPSD, N_tmp, Fs) #energy percentage in different frequency intervals(e.g. 0-100Hz)
#     pl.subplot(223)
#     pl.plot(PSDlist_x)
#     print(pivot)

# # ------------------y-axis--------------------
# Workingdata = data_y
# N = len(Workingdata)
# dataPSD = PSD(Workingdata, N, Fs)  # data of PSD
# pointnum = int(FreqInterval / (Fs / N))
# PSDlist_y = PSDextract(FreqInterval, dataPSD, N, Fs)  # energy percentage in different frequency intervals(e.g. 0-100Hz)

# #------------------z-axis--------------------
# Workingdata = data_z
# N = len(Workingdata)
# dataPSD = PSD(Workingdata, N, Fs)  # data of PSD
# pointnum = int(FreqInterval / (Fs / N))
# PSDlist_z = PSDextract(FreqInterval, dataPSD, N, Fs)  # energy percentage in different frequency intervals(e.g. 0-100Hz)

# #-------------------------------write csv----------------------------
# filenum = 10 #number of files in the directory, which decides the total RUL
# # with open('./Output/' + 'output-r1el-04.csv', 'a', newline='') as out: #the directory of data written
# #     csv_write = csv.writer(out, dialect='excel')
# #     RUL = filenum * 5 - fileindex * 5
# #     datalist = [fileindex, RUL]
# #     datalist.extend(PSDlist_x.tolist())
# #     datalist.extend(PSDlist_y.tolist())
# #     datalist.extend(PSDlist_z.tolist())
# #     csv_write.writerow(datalist)

#print(str(fileindex)+' finish!')

