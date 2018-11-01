# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 14:45:43 2018

@author: dani


change t-test to 
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from matplotlib import colors as mcolors
#import numpy as np
from scipy import stats



subplotnumber = 2


pixelsize = 1.2874  #in micron
timestep = 0.5      #in minutes



#indir = "./TrackMate_Analysis/XY_data_test/test/"
indir = "./TrackMate_Analysis/XY_data_60/HM_output-move_thresh_1/ForPairwiseComp/"
outdir = 'ViolinPlots_pairwise_labmeeting/'
    ### turn on line 173: curr_ax.set_xlabel('n=%d, i=%d'%(n,i),size = 6)
if not os.path.exists(indir+outdir):
    os.makedirs(indir+outdir)


LUT = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
# https://matplotlib.org/examples/color/named_colors.html

colors = []



col_names = [
        'dodgerblue',
        'orange',
        ]

col_dict = {
        'CTF':'m',    #CellTrace Far red; always first acquired (in 1808)
        'CTV':'b',           #CellTrace Violet
        'CTY':'gold',           #CellTrace Yellow; always last acquired (in 1808)
        }

for x in col_names:
    colors.append(LUT[x])


#files = []
#names  = ['BSA','F127']
#
savenumber = 1
#file_list = [f for f in os.listdir(indir) if f.endswith('Channel1_SpotsStats.csv')]
#file_list = [f for f in os.listdir(indir) if f.endswith('Channel1_SpotsStats.csv') and f.startswith('HMout_Stitch_180802_2Dmig_BSA_CTVi+CTFR_6um_006')]
file_list = [f for f in os.listdir(indir) if f.endswith('Channel1_SpotsStats.csv') and f.startswith('HMout_Stitch_180822_1_BSA_CTVi+CTYw_001')]
#file_list = [f for f in os.listdir(indir) if f.endswith('Channel1_SpotsStats.csv') and f.startswith('HMout_00')]

# I could rework this to represent dye used or experimental condition
labels = ['Channel1','Channel2']
skip = ['Well/XY','cell_id',' ']
incl = ['total_distance','MSD_slope','nongauss','rw_kurtosis01']



for n, file in enumerate(file_list):
    Ch1 = pd.read_csv ( indir+file)
    Ch2 = pd.read_csv ( indir+file.replace('Channel1','Channel2') )
    all_data = pd.concat([Ch1,Ch2])

    all_data.loc[all_data['Well/XY'].str.contains('Channel1'),'Well/XY'] = 'Channel 1'
    all_data.loc[all_data['Well/XY'].str.contains('Channel2'),'Well/XY'] = 'Channel 2'
    all_data[' '] = ' '
    
    savename = file[13:-30]

    
    '''
    moved inside this loop instead of separate function
    create pair-wise violin plots for individual channels of same device
    '''
    palette = ['#8080ff','#FF8000']
    if 'CTF' in file:
        palette[0] = col_dict['CTF']
        if 'CTV' in file:
            palette[1] = col_dict['CTV']
    if 'CTY' in file:
        palette[1] = col_dict['CTY']
        if 'CTV' in file:
            palette[0] = col_dict['CTV']
    
    if n == 0:
        f,axes = [None]*len(all_data.columns) , [None]*len(all_data.columns)

    for i, para in enumerate(all_data):
        if not para in skip:
#            if i in [7,10,18,49]:       #use this or line below or turn off both to plot all
#            if para in incl:           #use this or line above or turn off both to plot all
                
                # adjusting pixel units to real units (um and um/min)
                if para.endswith('distance'):
                    all_data[para] = all_data[para] * pixelsize
                elif 'speed' in para:
                    all_data[para] = all_data[para] * pixelsize/timestep
                    
                    
                # t-test
                Ch1 = all_data[all_data['Well/XY']=='Channel 1'][para]
                Ch2 = all_data[all_data['Well/XY']=='Channel 2'][para]
                p = stats.ttest_ind(Ch1,Ch2)[1]
#                p = stats.mannwhitneyu(Ch1,Ch2, alternative='two-sided')[1]
#                p = stats.ks_2samp(Ch1,Ch2)[1]
                if(p>0.05):
                    sign = 'ns'
                elif(p>0.01):
                    sign = '*'
                elif(p>0.001):
                    sign = '**'
                else:
                    sign = '***'
                sign = sign+'\np = %.1e'%p
                
                # initiate figures
#                plt.figure(i)
#                print (n,i,len(all_data))
                q = n % subplotnumber
                if q == 0:
                    f[i],axes[i] = plt.subplots(1,subplotnumber,sharey=True)
                curr_ax = axes[i][q]
                

                # plot data in violin plot
                sns.violinplot(
                        data = all_data,
                        y = para,
                        x = ' ',
                        hue = 'Well/XY',
                        split = True,
                        palette = palette,      #['#8080ff','#FF8000'],
                        legend = True,
                        cut = 0,
                        ax = curr_ax,
                        )
                
                # formatting
                curr_ax.spines['right'].set_visible(False)
                curr_ax.spines['top'].set_visible(False)
                curr_ax.tick_params(
                    axis='x',          # changes apply to the x-axis
                    which='both',      # both major and minor ticks are affected
                    top=False,      # ticks along the bottom edge are off
                    bottom=True,         # ticks along the top edge are off
                    labelbottom=False, # labels along the bottom edge are off
                    direction = 'inout', 
                    width = 1, length = 2,
                    )
                curr_ax.tick_params(
                    axis='y',          # changes apply to the x-axis
                    labelsize = 8,
                    )
                curr_ax.legend_.remove()
                    # replace by numbers of samples as fig legend

                ### label x axis (only off for labmeeting version)                    
#                curr_ax.set_xlabel('n=%d, i=%d'%(n,i),size = 6)
                curr_ax.text(0.5,1,sign,ha='center', fontsize = 8, transform=curr_ax.transAxes)

#                curr_ax.set_xlabel(savename,size = 6)
#                curr_ax.labelszie
                if q>0:
                    curr_ax.yaxis.set_visible(False)
                    curr_ax.spines['left'].set_visible(False)
                else:
                    curr_ax.yaxis.label.set_size(fontsize = 12)

                
#            fig.figure.savefig(savedir+'%02d_%s_%s.png'%(i,para,savename),
                if (n == len(file_list)-1) or (q == subplotnumber-1):
                    while os.path.exists(indir+outdir+'%02d_%s_set%d.png'%(i,para,savenumber)):
                        savenumber+=1
                    f[i].subplots_adjust(wspace=0, hspace=0)
                    f[i].savefig(indir+outdir+'%02d_%s_set%d.png'%(i,para,savenumber),       #only for tester, replace with previous line for real thing
                       bbox_inches='tight',dpi=300,
                       bbox = False
                       )
                    plt.close(f[i])
                    
                
                
#                plt.show()
            
