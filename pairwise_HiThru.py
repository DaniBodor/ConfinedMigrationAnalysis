# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 10:28:49 2018

@author: dani

Make tSNE & PCA plots for each combination of 2 channels from same movie
Need to ask J. Kimmel what moving threshold is for 'time_moving01' etc. parameters
    and whether/how I can change that if needed
    this should be somewhere in the individual python files, but not necessarily easy to find
"""


from __future__ import division
import os
import pandas as pd
#import numpy as np
from matplotlib import pyplot as plt
import matplotlib
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import datetime
import seaborn as sns
#import skimage.io as io
#from scipy.stats import  mannwhitneyu, mstats
#import math
#import csv



indir = indir = "./TrackMate_Analysis/XY_data_60/HM_output-move_thresh_1/"
outdir = indir+'HM_Plots_pairwise_ALL/'


# set speed threshold for analysis (in px/frame)
#threshold = 1       # currently unused
# I will probably replace this by only using tracks that have a time_moving01>0

colors=['b','darkorange']
# not sure what next 2 parameters do exactly, sth to do with formatting though
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

# set which parameters to use. 
# Individual lines can be commented out
col = [
       'Well/XY', 
#       'cell_id', 
#       
       'total_distance', 'net_distance', 'linearity', 'spearmanrsq', 'progressivity',
       'max_speed', 'min_speed', 'avg_speed',
       'MSD_slope', 'hurst_RS', 'nongauss', 'disp_var', 'disp_skew',
       'rw_linearity', 'rw_netdist',

       'rw_kurtosis01', 'rw_kurtosis02', 'rw_kurtosis03', 'rw_kurtosis04', 'rw_kurtosis05',
       'avg_moving_speed01', 'avg_moving_speed02', 'avg_moving_speed03', 'avg_moving_speed04', 'avg_moving_speed05',
       'time_moving01', 'time_moving02', 'time_moving03', 'time_moving04', 'time_moving05',
       'autocorr_1', 'autocorr_2', 'autocorr_3', 'autocorr_4', 'autocorr_5',

       'p_rturn_9_5', 'p_rturn_10_5', 'p_rturn_11_5',
       'mean_theta_9_5', 'min_theta_9_5', 'max_theta_9_5',
       'mean_theta_10_5', 'min_theta_10_5', 'max_theta_10_5',
       'mean_theta_11_5', 'min_theta_11_5', 'max_theta_11_5',

       'rw_kurtosis06', 'rw_kurtosis07', 'rw_kurtosis08', 'rw_kurtosis09', 'rw_kurtosis10',
       'avg_moving_speed06', 'avg_moving_speed07', 'avg_moving_speed08', 'avg_moving_speed09', 'avg_moving_speed10',
       'time_moving06', 'time_moving07', 'time_moving08', 'time_moving09', 'time_moving10',
       'autocorr_6', 'autocorr_7', 'autocorr_8', 'autocorr_9', 'autocorr_10',

       'p_rturn_9_6', 'p_rturn_10_6', 'p_rturn_11_6',
       'mean_theta_9_6', 'min_theta_9_6', 'max_theta_9_6',
       'mean_theta_10_6', 'min_theta_10_6', 'max_theta_10_6',
       'mean_theta_11_6', 'min_theta_11_6', 'max_theta_11_6',
#       
#       'Test_coulmn','Test_coulmn2',
       ]
outdir = outdir.replace('pairwise','pairwise_ALL')
if not os.path.exists(outdir):
    os.makedirs(outdir)



#file_list = [f for f in os.listdir(indir) if f.endswith('Channel1_SpotsStats.csv')]
#file_list = [f for f in os.listdir(indir) if f.endswith('Channel1_SpotsStats.csv') and f.startswith('HMout_Stitch_180802_2Dmig_BSA_CTVi+CTFR_6um_006.tif---')]
#file_list = [f for f in os.listdir(indir) if f.endswith('Channel1_SpotsStats.csv') and f.startswith('HMout_00')]
file_list = [f for f in os.listdir(indir) if f.endswith('Channel1_SpotsStats.csv') and f.startswith('HMout_Stitch_180822_1_BSA_CTVi+CTYw_001')]

# I could rework this to represent dye used or experimental condition
labels = ['Channel1','Channel2']
counter = 0

start = str(datetime.datetime.now().time())[:8]
N=['','']
for file in file_list:
    counter +=1
    Ch1 = file
    Ch2 = file.replace('Channel1','Channel2')
    
    # create figure title (for plot output)
    figtitle = file.replace('Channel1_SpotsStats.csv','')
    figtitle = figtitle.replace('HMout_','')
    figtitle = figtitle.replace('Stitch_','')
    figtitle = figtitle.replace('.tif','')
    figtitle = figtitle.replace('---','')

    pos = str(counter).zfill(2)+r'/'+str(len(file_list))
    print (pos,r'-',figtitle)

    if os.path.exists(indir+Ch2):               
        ###    LOAD AND ORGANIZE DATA
        dfCh1 = pd.read_csv(indir+Ch1,usecols = col)
        dfCh2 = pd.read_csv(indir+Ch2,usecols = col)
        N[0] = 'N=%d'%len(dfCh1)
        N[1] = 'N=%d'%len(dfCh2)
        
        # concatenate dataframes; drop stationary tracks; drop variables with 0 change; normalize data
        df_all = pd.concat( [dfCh1,dfCh2] , ignore_index = True)
        
        # drop stationary tracks (as defined by time_moving01=0) and variable with 0 change
        df_all = df_all[df_all.time_moving01 > 0]                           # drops stationary tracks
        droplist = [x for x in df_all if df_all[x].max() == df_all[x].min()]
        df_all = df_all.drop(droplist,axis=1)                               # avoids crashes in next line and doesn't contribute to variance
        
        # normalize data to ensure equal contribution from each variable
        dataset = df_all.pop('Well/XY')
        df_all = (df_all - df_all.min()) / (df_all.max() - df_all.min())
        
        # drop cell_id as dataset in case I accidentally load it in
        if 'cell_id' in df_all:
            df_all.drop('cell_id',axis=1)
        


        ###    PCA ANALYSIS 
        # Perform PCA on the normalized data and return transformed principal components from sklearn.decomposition
        pca = PCA()     # create pca object
        transformed = pca.fit_transform(df_all.values)
        
        # Calculates variance contribution (in %) of each principal component for axis labeling
        expl_var_ratio = pca.explained_variance_ratio_*100      # multiply by 100 to make it a %
            
            
        # Create PCA plot
        w, h = plt.figaspect(1.)
        pca_fig, pca_ax =plt.subplots(figsize=(w,h))
        
        x=0     # for color picking
        for i in dataset.unique():
            pca_ax.scatter(transformed[:,0][dataset == i], transformed[:,1][dataset == i], 
                        label = str(i), alpha=0.5, s=1, c=colors[x])
            x+=1

        # plot formatting
        # turn legend off if always plotting channel 1 vs channel 2?
        pca_ax.legend(loc='upper center', #bbox_to_anchor=(0.5, 1.05),
              ncol=1, fancybox=True, shadow=False, prop={'size': 4}, framealpha=0.75, 
              labels = N)  # labels = labels ## to get groupnames in legend
        
#        pca_ax.spines['right'].set_visible(False)
#        pca_ax.spines['top'].set_visible(False)
#        pca_ax.set_xlabel('PC1 (variance ' + str(int(expl_var_ratio[0]*100))+ ' %)')
#        pca_ax.set_ylabel('PC2 (variance ' + str(int(expl_var_ratio[1]*100))+ ' %)')
        
        pca_ax.set_xlabel('PC1 (%d%% of variance)'%(expl_var_ratio[0]))
        pca_ax.set_ylabel('PC2 (%d%% of variance)'%(expl_var_ratio[1]))

#        pca_ax.tick_params(axis='both', labelsize=8)
        plt.title(figtitle)

        # Output: show plots and save in outdir as pdf and as png
#        plt.show()
#        pca_fig.savefig(outdir+'pca_'+figtitle+'.pdf',  bbox_inches='tight')
        pca_fig.savefig(outdir+'pca_'+figtitle+'.png',  bbox_inches='tight',dpi=300)
        
        
        ###    tSNE ANALYSIS
        # perform tSNE
        tsne = TSNE(n_components = 2, init = 'pca', random_state= 0)    # create tsne object
        tsne_points = tsne.fit_transform(df_all.values)

        # create tSNE plot
        tsne_fig, tsne_ax = plt.subplots(figsize=(w,h))

        x=0     # for color picking
        for i in dataset.unique():
            tsne_ax.scatter(tsne_points[:,0][dataset == i], tsne_points[:,1][dataset == i], 
                   label = str(i), alpha=0.5, s=1, c=colors[x])
            x+=1
        
        # plot formatting
        plt.title(figtitle)
        tsne_ax.set_yticks([])
        tsne_ax.set_xticks([])
#        tsne_ax.axis('off')     #turn on to show no bounding box at all
        
        # turn legend off if always plotting channel 1 vs channel 2?
#        pca_ax.legend(loc='upper center', #bbox_to_anchor=(0.5, 1.05),
#              ncol=1, fancybox=True, shadow=False, prop={'size': 6}, framealpha=0.75, 
#              labels = N)  # labels = labels ## to get groupnames in legend

        
        # Output: show plots and save in outdir as pdf and as png
#        plt.show()
#        tsne_fig.savefig(outdir+'tsne_'+figtitle+'.pdf',  bbox_inches='tight')
        tsne_fig.savefig(outdir+'tsne_'+figtitle+'.png',  bbox_inches='tight',dpi=300)
        
        plt.close(pca_fig)
        plt.close(tsne_fig)
        
        
      
        
        
        
        
        # for PCA: Calculates contributions of each variables to top 2 components
        PCA_contrib = pd.DataFrame(abs(pca.components_), columns=list(df_all.columns))
        PCA_contrib = PCA_contrib.div(PCA_contrib.sum(axis=1),axis=0)
        with open(outdir+"X_PCAcontrib_"+figtitle+'.csv', "w") as PCA_contrib_file:
            PCA_contrib.to_csv(PCA_contrib_file)
            # would be good to add a column with the weight of each PCA component
            # this is stored in the expl_var_ratio list



end = str(datetime.datetime.now().time())[:8]


with open(outdir+"00_Parameters.txt", "w") as textfile:
    for para in col:
        textfile.write('%s\n'%para)

print(start)
print(end)
print ('all done')


