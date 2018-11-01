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




indir = "./"
outdir = 'ViolinPlots_Vert/'
if not os.path.exists(indir+outdir):
    os.makedirs(indir+outdir)


LUT = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
# https://matplotlib.org/examples/color/named_colors.html

colors = []

pixelsize = 1.2874  #in micron
timestep = 0.5      #in minutes

col_names = [
        'dodgerblue',
        'orange',
        ]

for x in col_names:
    colors.append(LUT[x])


#files = []
#names  = ['BSA','F127']
#
#BSA_df =  (pd.read_csv ( indir+'_Poster_%s_data.csv'%names[0]))
#F127_df = (pd.read_csv ( indir+'_Poster_%s_data.csv'%names[1]))
all_data = pd.read_csv ( indir+'180802+3_BSA_vs_F127.csv')
all_data = pd.read_csv ( indir+'180802+3_BSA_vs_F127_mt1.csv')


#for para in BSA_df:
#BSA  = sns.load_dataset(BSA_df)
#F127 = sns.load_dataset(F127_df)

skip = ['Coating',' ','cell_id']

for i, para in enumerate(all_data):
    if not para in skip:
#        if i in [7,10,18,49]:       #turn off to plot all
            plt.figure()
            if para.endswith('distance'):
                all_data[para] = all_data[para] * pixelsize
            elif 'speed' in para:
                all_data[para] = all_data[para] * pixelsize/timestep
            fig = sns.violinplot( 
                    data = all_data,
                    y=para,
                    x = ' ',
                    hue = 'Coating',
                    split = True,
                    palette = ['#8080ff','#FF8000'],
                    legend = False,
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
                labelbottom=False) # labels along the bottom edge are off
            
            fig.legend_.remove()
            
            fig.figure.savefig(outdir+'%02d_%s.png'%(i,para),
                               bbox_inches='tight',dpi=300,
                               bbox = False
                               )
            
            
#            plt.show()
        
            plt.close()

#sns.violinplot([F127_df['net_distance']])

#plt.show()