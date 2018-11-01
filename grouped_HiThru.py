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
import matplotlib 
import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors as mcolors
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
#import sys
#import skimage.io as io
#from scipy.stats import  mannwhitneyu, mstats
#import math
#import csv
import datetime





plt.ioff()




indir = indir = "./TrackMate_Analysis/XY_data_60/HM_output-move_thresh_1/"
outdir = indir+'HM_Plots_grouped/'


# set speed threshold for analysis (in px/frame)
threshold = 1       # currently unused
# I will probably replace this by only using tracks that have a time_moving01>0

# set colors for output
# https://matplotlib.org/examples/color/named_colors.html
LUT = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)

colors = []
col_names=[
        'firebrick','red',
        'darkgreen','limegreen',
        'dodgerblue','navy',
        'saddlebrown','peru',
        ]

col_names = [
        'cornflowerblue','steelblue',
        'darkorange','peru'
        ]


for x in col_names:
    colors.append(LUT[x])


colors = [
        '#8080ff','#8080ff',
        '#FF8000','#FF8000'
        ]



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
#outdir = outdir.replace('grouped','grouped_Poster')
if not os.path.exists(outdir):
    os.makedirs(outdir)
    
with open(outdir+"00_Parameters.txt", "w") as textfile:
    for para in col:
        textfile.write('%s\n'%para)  

# filenames for 1808 dataset
All_Files = {
      0:'000_TestList',
      1:'180802_2Dmig_BSA_CTVi+CTFR+GreenBeads_6um_007',
      2:'180802_2Dmig_BSA_CTVi+CTFR_6um_006',
      3:'180803_2Dmig_CTVi+CTFR_6um_BSA_',
      4:'180803_2Dmig_CTVi+CTFR_6um_F127',
      5:'180808_2Dmig_CTYW+CTFR+GreenBeadsInPDMS_6um_BSA',
      6:'180808_2Dmig_CTYW+CTFR+GreenBeadsInPDMS_6um_BSA_Scrap1-18',
      7:'180808_2Dmig_CTYW+CTFR_6um_BSA',
      8:'180808_2Dmig_CTYW+CTFR_6um_BSA_Scrap1',
      9:'180809_2Dmig_CTVi+CTFR_6um_BSA',
     10:'180809_2Dmig_CTVi+CTFR_6um_BSA_Scrap1',
     11:'180809_2Dmig_CTYw+CTFR_6um_BSA_',  #GFP4 error where it suddenly speeds up
     12:'180815_2Dmig_CTYw+CTFR_6um_BSA_001',
     13:'180815_2Dmig_CTYw+CTFR_6um_BSA_001_Scrap1',
     14:'180815_H2Bcells_CTFR+CTVi_BSA001',
     15:'180815_H2Bcells_CTFR+CTVi_BSA001.tif-SRRFdriftcorrectedFULL',
     16:'180815_H2Bcells_CTFR+CTVi_BSA001.tif-SRRFdriftcorrectedROI',
     17:'180815_H2Bcells_CTFR+CTVi_BSA002',
     18:'180815_H2Bcells_CTFR+CTYw_BSA',
     19:'180815_H2Bcells_CTFR+CTYw_BSA.tif-SRRFdriftcorrectedFULL',
     20:'180815_H2Bcells_CTFR+CTYw_BSA002',
     21:'180816_WTcells_CTVi+CTYw_BSA',
     22:'180822_1_BSA_CTVi+CTYw_001',
     23:'180822_2_F127_CTVi+CTYw_002',
     24:'180822_3_Fibron_CTVi+CTYw_003',
     25:'180822_4_BSA_CTVi+CTYw_004',
     # more files present in the 60 tp dataset
     26:'180809_2Dmig_CTYw+CTFR_6um_BSA',   #with drift!
     27:'180809_2Dmig_CTYw+CTFR_6um_BSA_NoDrift_1-74',
     28:'180809_2Dmig_CTYw+CTFR_6um_BSA_NoDrift_78-175',
     }

# groups for 1808 dataset
grouped_comparisons = [     # read filenames from above to compare in groups (using both channels sep)
        [1,2],   #1 replicate experiments (except for green beads) - FR vs Vi
        [5,6],   #2 scrapped drift section vs not scrapped
        [7,8],   #3 scrapped 1st tp vs not
        [6,8],   #4 replicate experiments (except for green beads) - FR vs Yw
        [8,13],  #5 replicates on different days - FR vs Yw
        [14,15,16],  #6 drift corrected vs uncorrected
        [18,19],     #7 drift corrected vs uncorrected
        [14,18,20,17],   #8 Vi vs Yw -- uncorrected
        [15,19,20,17],   #9 Vi vs Yw -- drift corrected
        [22,23,24,25],   #10 surface coatings
        [21,22,25],    #11 replicates on different days - Vi vs Yw
        [23,22,25],   #12 BSA (g+b) vs F127 (r)
        [22,25],   #13 BSA replicates
        [3,4],   #14 BSA vs F127; skipped because of pressure-flow in BSA device
        [27,28],  #15 Full movie vs slow part vs fast part
        [23,22],    #16 180822: BSA vs F127
        [4,2],      #16 180802/03: BSA vs F127
        ]


# groupnames for 1808 dataset
groupnames = [
        '180802: 2 replicates (FR + Vi) - beads',   #1 replicate experiments (except for green beads) - FR vs Vi
        '180808: complete vs drifting scrap',   #2 scrapped drift section vs not scrapped
        '180808: complete vs 1st timepoint scrapped',   #3 scrapped 1st tp vs not
        '180808: 2 replicates (FR + Yw) - embedded beads',  #4 replicate experiments (except for green beads) - FR vs Yw
        'Replicates (FR vs Yw): 180808 (r) / -15 (g)',  #5 replicates on different days - FR vs Yw
        '180815: 2 types of drift correction: none (r) / FULL (g) / ROI (b)',  #6 drift corrected vs uncorrected
        '180815: uncorrected vs drift corrected (FULL)',     #7 drift corrected vs uncorrected
        '180815: Vi (r+br) vs Yw (g+bl) - No drift corrections',   #8 Vi vs Yw -- uncorrected
        '180815: Vi (r+br) vs Yw (g+bl)',   #9 Vi vs Yw -- drift corrected
        '180822: surface coatings - BSA (r+br) / F127 (g) / FN (bl)',   #10 surface coatings
        'Replicates (FR vs Vi): 180816 (r) / -22 (g+b)',    #11 replicates on different days - FR vs Vi
        '180822: BSA (g+b) vs F127 (r)',    #12
        '180822: 2 replicates (Vi + Yw)',    #13
        '180803: POS CTRL (BSA with pressure flow vs F127)',    #14
        '180809: slow (30s intv; r) / fast (110s intv; g)',    #15
        '180822: BSA (g) vs F127(r)',    #16
        '180802/03: BSA (g) vs F127(r)',    #17
        ]

#only one of folowing two is used (set the correct if statement below)
include_groups = [1,4,5,9,10,11,12,13,14,15]
first_group = 16    # set to first group to include in analysis




file_list = [f for f in os.listdir(indir) if f.endswith('Channel1_SpotsStats.csv')]
#file_list = [f for f in os.listdir(indir) if f.endswith('Channel1_SpotsStats.csv') and f.startswith('HMout_Stitch_180802_2Dmig_BSA_CTVi+CTFR_6um_006.tif---')]
#file_list = [f for f in os.listdir(indir) if f.endswith('Channel1_SpotsStats.csv') and f.startswith('HMout_00')]
#file_list = list(All_Files.values())

#sys.exit()
# I could rework this to represent dye used or experimental condition
#labels = ['Channel1','Channel2']


counter = max(0,first_group-1)                  
#include_groups = [x-1 for x in include_groups]      # activate to use include_groups / deactiveate to yuse first_group
#counter = 6

for group in grouped_comparisons:
    if group == grouped_comparisons[counter]: #To use this, comment out next 3 lines
#    if counter not in include_groups:
#        counter +=1
#    else:
        ### initialize lists
        filenames,labels = [],[]        #Used for labeling of output files and images,respectively
        df_list,N = [],[]               #Used to store data and number of datapoints, respectively
        
        figtitle = groupnames[counter]
        counter += 1
    
        outfile = str(counter).zfill(2)+'_'+figtitle.replace(': ','-').replace(' ','_').replace('/','-vs-')
        pos = str(counter).zfill(2)+'/'+str(len(grouped_comparisons))
        print (str(datetime.datetime.now().time())[:8],pos+'-'+figtitle)
        for file_index in group:
            curr_file = 'HMout_Stitch_%s.tif---Channel1_SpotsStats.csv'%All_Files[file_index]
            ##### Channel 1
            ###    LOAD AND ORGANIZE DATA
            filenames.append(curr_file)
            df_list.append (pd.read_csv ( indir+curr_file, usecols = col))
            ### create labels for plot output
            labels.append(curr_file.replace('Channel1_SpotsStats.csv','_C1') )
            labels[-1] = labels[-1].replace('HMout_','')
            labels[-1] = labels[-1].replace('Stitch_','')
            labels[-1] = labels[-1].replace('.tif','')
            labels[-1] = labels[-1].replace('---','')
            
            ##### Channel 2
            ###    LOAD AND ORGANIZE DATA
            filenames.append(curr_file.replace('Channel1','Channel2'))
            df_list.append(pd.read_csv(indir+filenames[-1], usecols = col))
            ### create labels for plot output
            labels.append(curr_file.replace('Channel1_SpotsStats.csv','_C2') )
            labels[-1] = labels[-1].replace('HMout_','')
            labels[-1] = labels[-1].replace('Stitch_','')
            labels[-1] = labels[-1].replace('.tif','')
            labels[-1] = labels[-1].replace('---','')


#        ### Try to get averages and proportion of static cells for each group
#        ### haven't finished this and decided to drop it for now
#        ### would be good to get back on it at some point though
#        av,prop_stat = [],[]
##            df_Ch1_Ch2 = df_list[-2:]
#        for sample in df_list:
#            for para in df_list[sample]:
#                try:
#                    av.append(          np.mean(df_list[sample][para])                                  )
#                    prop_stat.append(   sum(df_list[sample]['time_moving01']) / len(df_list[sample])    )
#                except TypeError:
#                    pass
            
            
            
            
        # concatenate dataframes; drop stationary tracks; drop variables with 0 change; normalize data
        df_all = pd.concat( df_list , ignore_index = True)
        
        # drop stationary tracks (as defined by time_moving01 = 0) and 0-change variables
        df_all = df_all[df_all.time_moving01 > 0]                           # drops stationary tracks (how is timemoving-thresh defined?)
        droplist = [x for x in df_all if df_all[x].max() == df_all[x].min()]# finds 0-change variable (i.e. no contribution to variance)
        df_all = df_all.drop(droplist,axis=1)                               # drop 0-change variables to avoid crashes in next line
        
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
        
#        labels = ['BSA_1',"BSA_2",'F127_1','F127_2']
        
        x=0     # for color picking
#        order = [dataset.unique()[0] , dataset.unique()[2] , dataset.unique()[1] , dataset.unique()[3]]
#        order = [0,2,1,3]
#        colors = [colors [0] , colors [2] , colors [1] , colors [3]]
        for i in dataset.unique():
            pca_ax.scatter(transformed[:,0][dataset == i], transformed[:,1][dataset == i], 
                        alpha=0.5, s=1, c=colors[x])#,label = str(i), )
            N.append(len(transformed[dataset == i]))
            labels[x] = labels[x]+' (n=%d)'%N[-1]
#            labels[x] = ' (n=%d)'%N[-1]
            x+=1
    
        # plot formatting
        # turn legend off if always plotting channel 1 vs channel 2
        pca_ax.legend(#loc='upper left', #bbox_to_anchor=(0.5, 1.05),
              ncol=1, fancybox=True, shadow=False, prop={'size': 4}, framealpha=0.75, 
              labels = labels)  # labels = labels ## to get groupnames in legend
        
#        pca_ax.spines['right'].set_visible(False)
#        pca_ax.spines['top'].set_visible(False)
#        pca_ax.set_xlabel('PC1 (variance ' + str(int(expl_var_ratio[0]*100))+ ' %)')
#        pca_ax.set_ylabel('PC2 (variance ' + str(int(expl_var_ratio[1]*100))+ ' %)')
        
        pca_ax.set_xlabel('PC1 (%d%% of variance)'%(expl_var_ratio[0]))
        pca_ax.set_ylabel('PC2 (%d%% of variance)'%(expl_var_ratio[1]))
    
    #        pca_ax.tick_params(axis='both', labelsize=8)
        plt.title(figtitle,fontsize = 10)
    
        # Output: show plots and save in outdir as pdf and as png
    #        plt.show()
    #        pca_fig.savefig(outdir+'pca_'+figtitle+'.pdf',  bbox_inches='tight')
        pca_fig.savefig(outdir+'pca_'+outfile+'.png',  bbox_inches='tight',dpi=300)
        
        
        ###    tSNE ANALYSIS
        # perform tSNE
        tsne = TSNE(n_components = 2, init = 'pca', #random_state= 22,
                    perplexity = 50)#, n_iter = 5000)    # create tsne object
        tsne_points = tsne.fit_transform(df_all.values)
    
        # create tSNE plot
        tsne_fig, tsne_ax = plt.subplots(figsize=(w,h))
    
        x=0     # for color picking
        for i in dataset.unique():
            tsne_ax.scatter(tsne_points[:,0][dataset == i], tsne_points[:,1][dataset == i], 
                   label = str(i), alpha=0.5, s=1, c=colors[x])
            x+=1
        
        # plot formatting
        plt.title(figtitle, fontsize = 10)
        tsne_ax.set_yticks([])
        tsne_ax.set_xticks([])
#        tsne_ax.axis('off')     #turn on to show no bounding box at all
        
        # turn legend off if always plotting channel 1 vs channel 2
#        pca_ax.legend(loc='upper left', #bbox_to_anchor=(0.5, 1.05),
#              ncol=1, fancybox=True, shadow=False, prop={'size': 6}, framealpha=0.75, 
#              labels = N)  # labels = labels ## to get groupnames in legend

    
        # Output: show plots and save in outdir as pdf and as png
#        plt.show()
#        tsne_fig.savefig(outdir+'tsne_'+figtitle+'.pdf',  bbox_inches='tight')
        tsne_fig.savefig(outdir+'tsne_'+outfile+'.png',  bbox_inches='tight',dpi=300)
        
        
        plt.close(pca_fig)
        plt.close(tsne_fig)
        
        
        #### Plots for individual parameters
        
        
        
        
        
        # for PCA: Calculates contributions of each variables to top 2 components
        PCA_contrib = pd.DataFrame(abs(pca.components_), columns=list(df_all.columns))
        PCA_contrib = PCA_contrib.div(PCA_contrib.sum(axis=1),axis=0)
        with open(outdir+"X_PCAcontrib_"+outfile+'.csv', "w") as PCA_contrib_file:
            PCA_contrib.to_csv(PCA_contrib_file)
            # would be good to add a column with the weight of each PCA component
            # this is stored in the expl_var_ratio list
            
        
        
      

print (str(datetime.datetime.now().time())[:8])
print ('script done')
