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
mpl.use('TkAgg')

#------------------------function------------------------
from DataProcessing import PSD
from DataProcessing import PSDextract


#---------------------------------------------Read current data (csv)---------------------------------------------
pivot = 0
fileindex = 0
dataset_current = [[] for _ in range(48)] #48 is the number of files
#dataset: 48*?
#?: [ data_current ]

path="Sensor/01-qLua/01/" #the directory of data readed

path_list = os.listdir(path)
path_list.sort(key=lambda x: int(x[:-4])) #sort filenames, e.g. 1.csv, put away '.csv', then sort by number


for filename in path_list:
    pivot = 0
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
                    print('Error data: ' + path + filename + ' ' + str(pivot))
                    print(signals)
                    pivot += 1
                    continue
                if abs(float(signals[0])) > 1000 or abs(float(signals[1])) > 1000 or abs(float(signals[2])) > 1000:
                    print('Error data: ' + path + filename + ' ' + str(pivot))
                    print(signals)
                    pivot += 1
                    continue
                dataset_current[fileindex].append(signals[3])
                pivot += 1
                
    fileindex += 1


# In[3]:


current_data_file1 = dataset_current[0]
N = len(current_data_file1)
Fs = 25600
dataPSD = PSD(current_data_file1, N, Fs)
F = list(map(lambda x: (x-1)*Fs/N, list(range(N+1))))

plt.plot(F[0:int(N/2)], np.log(dataPSD[0:int(N/2)])*10)
plt.show()

