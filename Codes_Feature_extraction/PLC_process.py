#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[2]:


#-------------------------package--------------------------
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

#--------------------------Read plc.csv---------------------------------
pivot = 0
dataset_x = []
dataset_y = []
dataset_z = []
csv_no = [] #start from 1

filename="PLC/qLua-01.csv" #the directory of data readed

with open(filename, 'r') as file:
    csv_file = csv.reader(file)
    for signals in csv_file:
        if pivot == 0:
            pivot += 1
        else:
            if len(signals[2]) == 0 or len(signals[3]) == 0 or len(signals[4]) == 0:
                print('Error data: ' + filename + ' ' + str(pivot))
                print(signals)
                pivot += 1
                continue
            if abs(float(signals[2])) > 1000 or abs(float(signals[3])) > 1000 or abs(float(signals[4])) > 1000:
                print('Error data: ' + filename + ' ' + str(pivot))
                print(signals)
                pivot += 1
                continue
            # if float(signals[4]) > -400.0: #the threshold of z-axis (PLC)
            #     print('The tool is not working: ' + filename + ' ' + str(pivot))
            #     print(signals)
            #     pivot += 1
            #     continue
            dataset_x.append(float(signals[2]))
            dataset_y.append(float(signals[3]))
            dataset_z.append(float(signals[4]))
            csv_no.append(int(signals[5]))
            pivot += 1


# In[3]:


#--------------------------csv number-------------------------------
number_csv_no = [] #the number of 1s, 2s,......, 48s
pivotat = 0
for i in range(1, max(csv_no)+1, 1):
    sum = 0
    while pivotat < len(csv_no):
        if csv_no[pivotat] == i:
            sum += 1
            pivotat += 1
        else:
            break
    number_csv_no.append(sum)

csv_index = [] #the index of 1s. 2s.....
for i in range(0, max(csv_no), 1):
    num = number_csv_no[i]
    csv_list = [a for a in range(1, num+1, 1)] #start from 1
    csv_index.extend(csv_list)


# In[4]:


#------------------------------delete not working data in z axis----------------------------------
def delete_Z_notworking(dataset_x, dataset_y, dataset_z, csv_no, number_csv_no, csv_index):
    dataindex = 0
    while dataindex < len(dataset_x):
        if dataset_z[dataindex] > -400: #the threshold of z-axis not working in PLC
            del dataset_x[dataindex]
            del dataset_y[dataindex]
            del dataset_z[dataindex]
            csvindex = csv_no[dataindex]
            del csv_no[dataindex]
            number_csv_no[csvindex - 1] -= 1
            del csv_index[dataindex]
            dataindex -= 1
            #print("Delete points because of z-axis not working data: " + str(dataindex))
        dataindex += 1

delete_Z_notworking(dataset_x, dataset_y, dataset_z, csv_no, number_csv_no, csv_index)


#-----------------------delete duplicated points------------------------
def duplicate(dataset1, dataset2, dataset3, csv_no, csv_index):
    dataset1_tmp = dataset1.copy()
    dataset2_tmp = dataset2.copy()
    dataset3_tmp = dataset3.copy()
    csv_no_tmp = csv_no.copy()
    csv_index_tmp = csv_index.copy()
    length = len(dataset1_tmp) - 1
    step = 0
    while step < length:
        if dataset1_tmp[step] == dataset1_tmp[step+1] and dataset2_tmp[step] == dataset2_tmp[step+1]:
            del dataset1_tmp[step + 1]
            del dataset2_tmp[step + 1]
            del dataset3_tmp[step + 1]
            del csv_no_tmp[step + 1]
            del csv_index_tmp[step + 1]
            step = step - 1

        step = step + 1
        length = len(dataset1_tmp) - 1
    return dataset1_tmp, dataset2_tmp, dataset3_tmp, csv_no_tmp, csv_index_tmp


dataset_x_dup, dataset_y_dup, dataset_z_dup, csv_no_dup, csv_index_dup = duplicate(dataset_x, dataset_y, dataset_z, csv_no, csv_index)


# In[5]:


# #-----------------------plot PLC------------------------
#
# # del dataset_x_dup[0:40]
# # del dataset_z_dup[0:40]
# fig = plt.figure()
# ax = fig.add_subplot(221)
#
# plt.plot(dataset_x_dup, dataset_y_dup)
# line, = ax.plot([], [], 'ro', animated=False)
# data_x = []
# data_y = []
#
# def update(i):
#     i = int(i)
#     data_x.append(dataset_x_dup[i])
#     data_y.append(dataset_y_dup[i])
#     if len(data_x) >= 10:
#         line.set_data(data_x[i-10:i], data_y[i-10:i])
#     else:
#         line.set_data(data_x, data_y)
#     line.set_markerfacecolor('r')
#     line.set_markersize(4)
#     line.set_linestyle('None')
#     return line,
#
# ani = animation.FuncAnimation(fig=fig, func=update, frames=50000, interval=500, blit=True)
# #ani.save('PLC.gif', writer='imagemagick')
# plt.show()


# In[6]:


#--------------------recognize periods----------------------
def separate2graph(dataset_x, dataset_y, dataset_z, csv_no, csv_index):
    graph1_x = []
    graph1_y = []
    graph1_z = []
    graph2_x = []
    graph2_y = []
    graph2_z = []
    csv_no1 = []
    csv_no2 = []
    csv_index1 = []
    csv_index2 = []
    #center_x = np.mean(np.array(dataset_x))
    center_x = -500 #eyes
    for i in range(len(dataset_x)):
        if dataset_x[i] < center_x:
            graph1_x.append(dataset_x[i])
            graph1_y.append(dataset_y[i])
            graph1_z.append(dataset_z[i])
            csv_no1.append(csv_no[i])
            csv_index1.append(csv_index[i])
        else:
            graph2_x.append(dataset_x[i])
            graph2_y.append(dataset_y[i])
            graph2_z.append(dataset_z[i])
            csv_no2.append(csv_no[i])
            csv_index2.append(csv_index[i])
    #print("Center of two graphs: " + " " + str(center_x))
    return graph1_x, graph1_y, graph1_z, graph2_x, graph2_y, graph2_z, csv_no1, csv_index1, csv_no2, csv_index2


def getCenter2D(dataset_x, dataset_y):
    center_x = np.mean(np.array(dataset_x))
    center_y = np.mean(np.array(dataset_y))
    return center_x, center_y


def distance2D(point1_x, point1_y, point2_x,  point2_y):
    return math.sqrt((point1_x-point2_x)**2+(point1_y-point2_y)**2)


def angle2D(point1_x, point1_y, center_x, center_y):
    return math.atan2((point1_y-center_y), (point1_x-center_x))/math.pi*180 + 180


def separatePeriods(graph_x, graph_y, graph_z, center_x, center_y):
    Period1_x = [0 for _ in range(360)]
    Period1_y = [0 for _ in range(360)]

    for i in range(len(graph_x)):
        index = int(math.floor(angle2D(graph_x[i], graph_y[i], center_x, center_y)))
        if Period1_x[index] == 0:
            Period1_x[index] = graph_x[i]
            Period1_y[index] = graph_y[i]

    return Period1_x, Period1_y


def filter_Points_by_Angle(graph_x, graph_y, graph_z, center_x, center_y, csv_no, csv_index):
    #20 degrees per index
    #filter_data: 18*?
    #?: [ [csv_no, csv_idnex],................, [csv_no, csv_idnex] ]
    filter_data = [[] for _ in range(18)]
    for i in range(len(graph_x)):
        index = int(math.floor(angle2D(graph_x[i], graph_y[i], center_x, center_y)/20))
        onepoint = []
        onepoint.append(csv_no[i])
        onepoint.append(csv_index[i])
        filter_data[index].append(onepoint)

    return filter_data


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


# In[7]:


# #------------------------plot angle separation (dup version)----------------------------
# graph1_x_dup, graph1_y_dup, graph1_z_dup, graph2_x_dup, graph2_y_dup, graph2_z_dup, csv_no1_dup, csv_index1_dup, csv_no2_dup, csv_index2_dup = \
#     separate2graph(dataset_x_dup, dataset_y_dup, dataset_z_dup, csv_no_dup, csv_index_dup)
# #center_x, center_y = getCenter2D(graph1_x, graph1_y)
# #print("Center of graph1: " + " " + str(center_x) + " " + str(center_y))
# center_x = -720
# center_y = 135
# Period1_x_dup, Period1_y_dup = separatePeriods(graph1_x_dup, graph1_y_dup, graph1_z_dup, center_x, center_y)
# plt.subplot(222)
# plt.plot(graph1_x_dup, graph1_y_dup, "b")
# plt.subplot(223)
# plt.plot(Period1_x_dup, Period1_y_dup, "b.")
# plt.show()

#-------------------------------filter data by angles-------------------------------

center_x = -720
center_y = 135

graph1_x, graph1_y, graph1_z, graph2_x, graph2_y, graph2_z, csv_no1, csv_index1, csv_no2, csv_index2 =     separate2graph(dataset_x, dataset_y, dataset_z, csv_no, csv_index)

filter_data = filter_Points_by_Angle(graph1_x, graph1_y, graph1_z, center_x, center_y, csv_no1, csv_index1)

filter_data_compressed = [[] for _ in range(18)]
for i in range(len(filter_data)):
    filter_data_compressed[i] = CompressFilterData(filter_data[i])
    
print(filter_data_compressed[0][0:5])
print(filter_data_compressed[1][0:5])

