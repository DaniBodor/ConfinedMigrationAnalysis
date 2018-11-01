# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 14:45:43 2018

@author: dani
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from matplotlib import colors as mcolors


pixelsize = 1.2874  #in micron
timestep = 0.5      #in minutes


indir = "./TrackMate_Analysis/XY_data_60/HM_output-move_thresh_1/"
outdir = 'ViolinPlots_pairwise/'
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

file_list = [f for f in os.listdir(indir) if f.endswith('Channel1_SpotsStats.csv')]
#file_list = [f for f in os.listdir(indir) if f.endswith('Channel1_SpotsStats.csv') and f.startswith('HMout_Stitch_180802_2Dmig_BSA_CTVi+CTFR_6um_006.tif---')]
#file_list = [f for f in os.listdir(indir) if f.endswith('Channel1_SpotsStats.csv') and f.startswith('HMout_00')]

# I could rework this to represent dye used or experimental condition
labels = ['Channel1','Channel2']
skip = ['Well/XY','cell_id',' ']


def pw_viol_plot(all_data):
    '''
    create pair-wise violin plots for individual channels of same device
    '''
    palette = ['#8080ff','#FF8000']
    if 'CTF' in savename:
        palette[0] = col_dict['CTF']
        if 'CTV' in savename:
            palette[1] = col_dict['CTV']
    if 'CTY' in savename:
        palette[1] = col_dict['CTY']
        if 'CTV' in savename:
            palette[0] = col_dict['CTV']
    
    for i, para in enumerate(all_data):
        if not para in skip:
#            if i in [7,10,18,49]:       #turn off to plot all
                plt.figure()
                if para.endswith('distance'):
                    all_data[para] = all_data[para] * pixelsize
                elif 'speed' in para:
                    all_data[para] = all_data[para] * pixelsize/timestep
                fig = sns.violinplot( 
                        data = all_data,
                        y = para,
                        x = ' ',
                        hue = 'Well/XY',
                        split = True,
                        palette = palette,      #['#8080ff','#FF8000'],
                        legend = True,
                        cut = 0,
    #                    bw = 0.2,
                        )
                
                fig.spines['right'].set_visible(False)
                fig.spines['top'].set_visible(False)
                plt.tick_params(
                    axis='y',          # changes apply to the x-axis
                    which='both',      # both major and minor ticks are affected
                    top=False,      # ticks along the bottom edge are off
                    bottom=False,         # ticks along the top edge are off
                    labelbottom=False, # labels along the bottom edge are off
                    )
                
                fig.legend_.remove()
                    # replace by numbers of samples as fig legend
                fig.set_title(savename)

                
#                fig.figure.savefig(savedir+'%02d_%s_%s.png'%(i,para,savename),
                fig.figure.savefig(indir+outdir+'%02d_%s_%s.png'%(i,para,savename),       #only for tester, replace with previous line for real thing
                                   bbox_inches='tight',dpi=300,
                                   bbox = False
                                   )
                
                
    #            plt.show()
            
                plt.close()

#sns.violinplot([F127_df['net_distance']])

#plt.show()
                
for i, file in enumerate(file_list):
    Ch1 = pd.read_csv ( indir+file)
    Ch2 = pd.read_csv ( indir+file.replace('Channel1','Channel2') )
    all_data = pd.concat([Ch1,Ch2])

    all_data.loc[all_data['Well/XY'].str.contains('Channel1'),'Well/XY'] = 'Channel 1'
    all_data.loc[all_data['Well/XY'].str.contains('Channel2'),'Well/XY'] = 'Channel 2'
    all_data[' '] = ' '
    
    savename = file[13:-30]
#    savedir = indir+outdir+savename+'/'
#    if not os.path.exists(savedir):
#        os.makedirs(savedir)
    
    pw_viol_plot(all_data)