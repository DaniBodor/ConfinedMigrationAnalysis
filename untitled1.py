# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 14:45:43 2018

@author: dani
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



indir  = './'
outdir = './'

files = []
names  = ['BSA','F127']

BSA_df =  (pd.read_csv ( indir+'_Poster_%s_data.csv'%names[0]))
F127_df = (pd.read_csv ( indir+'_Poster_%s_data.csv'%names[1]))

#for para in BSA_df:
BSA  = sns.load_dataset(indir+'_Poster_%s_data.csv'%names[0])
F127 = sns.load_dataset(indir+'_Poster_%s_data.csv'%names[1])
    
g = sns.violinplot(data=BSA)

plt.show()