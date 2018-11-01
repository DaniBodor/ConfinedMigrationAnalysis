# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 10:32:45 2018

@author: dani
"""

from __future__ import division
import skimage.io as io
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from scipy.stats import  mannwhitneyu, mstats
import os
import math
import csv
import sys
import matplotlib.patches as mpatches


# for color coding by condition; currently unused
#c_un = 'red'
#c_ck = 'blue'
#c_eg = 'green'
#c_tr = 'purple'



base = "./TrackDataNew/XY_data/HM_output/"
filelist = os.listdir(base)
paraset = []

# initiate dictionaries to store data in
DataMean = {}
DataMean_norm={}
DataVar = {}
DataVar_norm={}
DataCV = {}
DataCV_norm={}



datalist = []
zero_data_counter=0     
zero_data_list = []
for filename in filelist:
    if filename.endswith('.csv') and not filename.startswith('_'):
        file = base + filename
        data = pd.read_csv(file)
        datalist.append(filename[:-4])
        
        ## fill parameter list first time a file is opened (they are all identical)
        ## create a dictionary for each
        if paraset == []:
            with open(file, newline='') as f:    
                reader = csv.reader(f)
                paraset = next(reader)
                for para in paraset:
                    DataMean.update({para:[]})
                    DataVar.update({para:[]})
                    DataCV.update({para:[]})
        
        ## add stats columns to dictionaries
        count = 0
        for para in paraset:
            count += 1
            try:
                data_av = data[para].mean()
                data_var = data[para].var()
                
                ## set coeff of var to 0 if the mean is 0
                if data_av == 0:
                    data_cv = 0
                    zero_data_counter += 1
                    zero_data_list.append(para + '('+filename +')')
                elif data_var == 0 :
                    print ("zero variance in non-zero average of "+para)
                    sys.exit("zero variance in non-zero average of "+para)
                else:
                    data_cv = np.sqrt(data_var)/np.abs(data_av) 
                
                DataMean[para].append(data_av)
                DataVar[para].append(data_var)
                DataCV[para].append(data_cv)
                
            ## in case data is non-numbers (for 'Well X/Y' column), use the filename instead
            except TypeError:
                DataMean[para].append(filename[:-4])
                DataVar[para].append(filename[:-4])
                DataCV[para].append(filename[:-4])
                
if zero_data_counter>0:
    print('total 0s found: '+str(zero_data_counter))
    print('0s found in this data:')
    print (zero_data_list)

## correct 'cell_id' to indicate the total number of cells in sample
    ## cell_id ranges from 0 to N-1, so the average is (0.5N-0.5)
DataMean['cell_id'] = [i*2+1 for i in DataMean['cell_id']]
DataVar['cell_id'] =  [i*2+1 for i in DataMean['cell_id']]
DataCV['cell_id'] =   [i*2+1 for i in DataMean['cell_id']]

## fix name and # of cells
#DataMean['Exp'] = DataMean.pop('Well/XY')
#DataMean['N'] = DataMean.pop('cell_id')


## create normalized data
## there's a problem here that data with positive and negative values don't normalize well!
for para in DataMean:
    if para == 'Exp' or para == 'N' or para == 'cell_id' or para == 'Well/XY':
        DataMean_norm[para] = DataMean[para]
        DataVar_norm[para] = DataVar[para]
        DataCV_norm[para] = DataCV[para]
    else:
        norm_mean = np.mean(DataMean[para])
        norm_var =  np.mean(DataVar[para])
        norm_cv =   np.mean(DataCV[para])
        DataMean_norm[para] = DataMean[para] / norm_mean
        DataVar_norm[para]  = DataVar[para] /  norm_var
        DataCV_norm[para]   = DataCV[para] /   norm_cv
        

## create plots of data
cols = ['tab:blue', 'tab:orange', 'tab:green', 
        'tab:red', 'tab:purple', 'tab:brown', 
        'tab:pink', 'tab:olive', 'tab:cyan', 'tab:gray']

im_types = ['Norm_mean','Norm_var','CV','NormCV']
im_data_list = [DataMean_norm,DataVar_norm,DataCV,DataCV_norm]
if len (im_types) != len(im_data_list):
    sys.exit('im_types[] and im_data_list[] must have same length')
T = len(im_types)

base_stats = paraset[2:17]
rw_kurt = paraset[17:27]
av_sp = paraset[27:37]
t_mov = paraset[37:47]
autocorr = paraset[47:57]
turns = paraset[57:63]
figs = [base_stats,rw_kurt,av_sp,t_mov,autocorr]
                # ,turns, paraset[2:]]
fignames = ['base_stats','rw_kurt','av_sp','t_mov','autocorr']
                #,'turns','all']
if len (figs) != len(fignames):
    sys.exit('figs[] and fignames[] must have same length')


patchList = []
legend_counter=0
for dataset in datalist:
    patch = mpatches.Patch(color=cols[legend_counter], label=dataset, alpha = 0.5)
    patchList.append(patch)
    legend_counter+=1



figcount=0
for p in figs:
    for im in im_data_list:
        fig = plt.figure(figcount)
        ax = plt.subplot(111)
        for para in im :
            if para in p:
                count=0
                for x in im[para]:
                    plt.scatter(para, x, alpha=0.5, c=cols[count])
                    count += 1

        #### Figure formatting        
        ## title
        plt.suptitle(im_types[figcount%T]+' ---- '+fignames[math.floor(figcount/T)], fontsize=16)
        ## Angle x-axis labels
        plt.xticks(ha="right", rotation = 45)
        ## Put a legend to the right of the current axis
        ax.legend(handles = patchList, loc='center left', bbox_to_anchor=(1, 0.5))
        ## Make sure that entire x axis label makes the image
        plt.gcf().subplots_adjust(bottom=0.25,right=.84)

        ## Save fig
        savename = (str(figcount+1) + '_'+ 
                        fignames[math.floor(figcount/len(im_types))] +'_'+ 
                        im_types[figcount%4] + '.png')
        fig.savefig(base + savename, dpi=300)
        print (savename + ': done')
        plt.close() # close them to save memory in case there's too many popping up
        figcount +=1
#        sys.exit()



### create csv files for normalized and unnormalized averages
#zd = zip(*DataMean.values())
#with open(base+'_Av.csv', 'w',newline='') as f_out:
#    writer = csv.writer(f_out, delimiter=',')
#    writer.writerow(DataMean.keys())
#    writer.writerows(zd)
#
#zd2 = zip(*DataMean_norm.values())
#with open(base+'_Av_Norm.csv', 'w',newline='') as f_norm:
#    writer = csv.writer(f_norm, delimiter=',')
#    writer.writerow(DataMean_norm.keys())
#    writer.writerows(zd2)
#

print ('all done')
print ('need to add a filter on non-migratory cells')