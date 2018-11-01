#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 11:35:53 2018
@author: paluchlab
"""
from __future__ import division
#import skimage.io as io
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
#from scipy.stats import  mannwhitneyu, mstats
import matplotlib
import os
import math
import csv

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
# Choose features from heteromotility table to be used for PCA and t-SNE
# Add them to the col-List below
col = [
#       'Well/XY',
       'cell_id',  
       'total_distance', 'net_distance', 'linearity', 'spearmanrsq', 'progressivity',
       'max_speed', 'min_speed', 'avg_speed',
       'MSD_slope', 'hurst_RS', 'nongauss', 'disp_var', 'disp_skew',
       'rw_linearity', 'rw_netdist',
       'rw_kurtosis01', 'rw_kurtosis02', 'rw_kurtosis03', 'rw_kurtosis04', 'rw_kurtosis05',
#       'rw_kurtosis06', 'rw_kurtosis07', 'rw_kurtosis08', 'rw_kurtosis09', 'rw_kurtosis10',
       'avg_moving_speed01', 'avg_moving_speed02', 'avg_moving_speed03', 'avg_moving_speed04', 'avg_moving_speed05',
#       'avg_moving_speed06', 'avg_moving_speed07', 'avg_moving_speed08', 'avg_moving_speed09', 'avg_moving_speed10',
       'time_moving01', 'time_moving02', 'time_moving03', 'time_moving04', 'time_moving05',
#       'time_moving06', 'time_moving07', 'time_moving08', 'time_moving09', 'time_moving10',
       'autocorr_1', 'autocorr_2', 'autocorr_3', 'autocorr_4', 'autocorr_5',
#       'autocorr_6', 'autocorr_7', 'autocorr_8', 'autocorr_9', 'autocorr_10',
       'p_rturn_9_5', 'p_rturn_9_6',
       'p_rturn_10_5', 'p_rturn_10_6',
       'p_rturn_11_5', 'p_rturn_11_6',
       'mean_theta_9_5', 'min_theta_9_5', 'max_theta_9_5',
       'mean_theta_9_6', 'min_theta_9_6', 'max_theta_9_6',
       'mean_theta_10_5', 'min_theta_10_5', 'max_theta_10_5',
       'mean_theta_10_6', 'min_theta_10_6', 'max_theta_10_6',
       'mean_theta_11_5', 'min_theta_11_5', 'max_theta_11_5',
       'mean_theta_11_6', 'min_theta_11_6', 'max_theta_11_6',
#       'Test_coulmn','Test_coulmn2',
       ] 

# Choose an average speed threshold speed_thresh in px/frame, cells moving 
# slower than this threshold wont be considered for analysis
speed_thresh = 1.0
# create a directory with your heteromotility stats .csv 

base="TrackMate_Analysis/XY_data_120/HM_output/SH_HiThru_Test/"
dirlist=os.listdir(base)
#dirlist = ["output"]

colors=['xkcd:azure','xkcd:darkblue','xkcd:cyan',
        'xkcd:sienna','brown',
        'xkcd:orange','xkcd:red',
        'green',
        ]
#colors=[0,1,2,3,4]
    
for thisdir in dirlist:
    if os.path.isdir(base+thisdir) and not thisdir.startswith('_'):
    #    directory = './May 2018 - Tests_SameLength/output_path_1EG/'
        # All files in this directory ending with .csv will be considered for analysis
        directory = "./"+base+thisdir+"/"
        
        files = os.listdir(directory)
        files = [f for f in files if '.csv' in f]
        # Reads in the csv in pandas, adds a label column = filename, drops all cells
        # slower than speed_thresh
        samples, labels =[],[]
        count=0
        for filename in files:
            df = pd.read_csv(directory + filename , usecols = col)
            df['label'] = filename.replace('.csv','')
            labels.append(filename.replace('.csv',''))
            samples.append(df[df.avg_speed>speed_thresh])
            if(filename.endswith('.csv')):
                count+=1
        labels=labels[::-1]
        
        with open(directory+filename) as csvFile:
            reader = csv.reader(csvFile)
            col = next(reader)[1:]
#            print (field_names_list)
#        break
    
        '''        
        plt.hist(speed_6[speed_6 > 1], bins = 10, alpha = 0.5)
        plt.hist(speed_10[speed_10 > 1], bins = 10, alpha = 0.5)
        print (mstats.normaltest(speed_10[speed_10 > 1]))
        mean_6 = np.mean(speed_6[speed_6 > 1])
        mean_10 = np.mean(speed_10[speed_10 > 1])
        print (mannwhitneyu(speed_6[speed_6 > 1], speed_10[speed_10 > 1]))
        
        '''        
        
        
        # All samples will be put together in df
        df = pd.concat(samples, ignore_index = True)
        # For analysis we drop cell_id and split off the label column
        label_df = df.label
        df = df.drop(['label'], axis = 1).drop(['cell_id'], axis = 1)
        # Data is normalized/scaled to ensure equal contribution from all features
        normalized_df=(df-df.min())/(df.max()-df.min())
        # Create a PCA object from sklearn.decomposition
        pca = PCA()
        # Perform PCA on the normalized data and return transformed principal components
        transformed = pca.fit_transform(normalized_df.values)
        components = pca.components_
        normed_comp = abs(components)/np.sum(abs(components),axis = 0)
        
        # Calculates variance contribution of each principal component
        expl_var_ratio = pca.explained_variance_ratio_
        # Creates a scatter plot of the first two principal components
        w, h = plt.figaspect(1.)
        pca_fig, pca_ax =plt.subplots(figsize=(w,h))

        x=0
        for i in labels:
            pca_ax.scatter(transformed[:,0][label_df == i], transformed[:,1][label_df == i], 
                        label = str(i), alpha=0.5, s=5, c=colors[x])
            x+=1
    #    pca_ax.legend()

#        handles,labels = pca_ax.get_legend_handles_labels()
#        handles=handles[::-1]
#        labels=labels[::-1]
#        pca_ax.legend(handles,labels)
        pca_ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
              ncol=math.ceil(count/2), fancybox=True, shadow=False, prop={'size': 6}, 
              framealpha=0.75)
        pca_ax.spines['right'].set_visible(False)
        pca_ax.spines['top'].set_visible(False)
        pca_ax.set_xlabel('PC1 (variance ' + str(int(expl_var_ratio[0]*100))+ ' %)')
        pca_ax.set_ylabel('PC2 (variance ' + str(int(expl_var_ratio[1]*100))+ ' %)')
        # Saves pca in directory
#        pca_fig.savefig(base + '__' + thisdir + '_pca_.pdf',  bbox_inches='tight')
        pca_fig.savefig(base + '__' + thisdir + '_pca_.png',  bbox_inches='tight',dpi=300)

        
        from sklearn.manifold import TSNE
        # Creates t-SNE plot without axis
        tsne = TSNE(n_components = 2, init = 'pca', random_state= 0 )
        tsne_points = tsne.fit_transform(normalized_df.values)
        fig, ax = plt.subplots(figsize=(w,h))
        ax.axis('off')
        x=0
        for i in labels:
            ax.scatter(tsne_points[:,0][label_df == i], tsne_points[:,1][label_df == i], 
                   label = str(i), alpha=0.5, s=5, c=colors[x])
            x+=1
    #    ax.legend(loc=2)
#        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
#              ncol=math.ceil(count/2), fancybox=True, shadow=False, prop={'size': 6},
#              framealpha=0.75)
        
        ax.legend(loc='upper left', #bbox_to_anchor=(0.5, 1.05),
              ncol=1, fancybox=True, shadow=False, prop={'size': 6},
              framealpha=0.75)
        # Saves t-SNE plot in directory
#        fig.savefig(base + '__' + thisdir + '_tsne_.pdf',  bbox_inches='tight')
        fig.savefig(base + '__' + thisdir + '_tsne_.png',  bbox_inches='tight',dpi=300)
        
        
        plt.close(pca_fig)
        plt.close(fig)

        