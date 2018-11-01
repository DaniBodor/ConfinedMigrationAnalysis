# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 10:28:49 2018

@author: dani

Make tSNE & PCA plots for each combination of 2 channels from same movie

"""


from __future__ import division
import skimage.io as io
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from scipy.stats import  mannwhitneyu, mstats
import matplotlib
import os
import math
import csv


# set speed threshold for analysis (in px/frame)
threshold = 1

colors=['g','m']
# not sure what next 2 parameters do exactly, sth to do with formatting though
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

# set which 
col = [#'Well/XY', 'cell_id',  
       'total_distance', 'net_distance', 'linearity', 'spearmanrsq', 'progressivity',
       'max_speed', 'min_speed', 'avg_speed',
       'MSD_slope', 'hurst_RS', 'nongauss', 'disp_var', 'disp_skew',
       'rw_linearity', 'rw_netdist',
       'rw_kurtosis01', 'rw_kurtosis02', 'rw_kurtosis03', 'rw_kurtosis04', 'rw_kurtosis05',
       'rw_kurtosis06', 'rw_kurtosis07', 'rw_kurtosis08', 'rw_kurtosis09', 'rw_kurtosis10',
       'avg_moving_speed01', 'avg_moving_speed02', 'avg_moving_speed03', 'avg_moving_speed04', 'avg_moving_speed05',
       'avg_moving_speed06', 'avg_moving_speed07', 'avg_moving_speed08', 'avg_moving_speed09', 'avg_moving_speed10',
       'time_moving01', 'time_moving02', 'time_moving03', 'time_moving04', 'time_moving05',
       'time_moving06', 'time_moving07', 'time_moving08', 'time_moving09', 'time_moving10',
       'autocorr_1', 'autocorr_2', 'autocorr_3', 'autocorr_4', 'autocorr_5',
       'autocorr_6', 'autocorr_7', 'autocorr_8', 'autocorr_9', 'autocorr_10',
       'p_rturn_9_5', 'p_rturn_9_6', 'p_rturn_10_5', 'p_rturn_10_6', 'p_rturn_11_5', 'p_rturn_11_6',
       'mean_theta_9_5', 'min_theta_9_5', 'max_theta_9_5', 'mean_theta_9_6', 'min_theta_9_6', 'max_theta_9_6',
       'mean_theta_10_5', 'min_theta_10_5', 'max_theta_10_5', 'mean_theta_10_6', 'min_theta_10_6', 'max_theta_10_6',
       'mean_theta_11_5', 'min_theta_11_5', 'max_theta_11_5', 'mean_theta_11_6', 'min_theta_11_6', 'max_theta_11_6']



indir = indir = "./TrackMate_Analysis/XY_data/HM_output/"
outdir = indir+'HM_Plots/'
if not os.path.exists(outdir):
    os.makedirs(outdir)

#file_list = [f for f in os.listdir(indir) if f.endswith('Channel1_SpotsStats.csv')]
file_list = [f for f in os.listdir(indir) if f.endswith('Channel1_SpotsStats.csv') and f.startswith('HMout_00')]

for file in file_list:
    Ch1 = indir+file
    Ch2 = indir+file.replace('Channel1','Channel2')
    if os.path.exists(Ch2):
        samples, labels =[],[]
        df_Ch1 = pd.read_csv(Ch1,usecols = col)
        df_Ch2 = pd.read_csv(Ch2,usecols = col)



