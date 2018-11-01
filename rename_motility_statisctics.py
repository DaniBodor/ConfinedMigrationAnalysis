# -*- coding: utf-8 -*-
"""
Created on Thu May 31 14:20:59 2018

@author: dani
"""

# -*- coding: utf-8 -*-
"""
Created on Wed May 30 15:30:36 2018

@author: dani

get subset of timepoints from Sascha's XY-extractor. 
At some point, I should integrate the two into a single script

"""


import os



indir = "./TrackDataNew/XY_data/HM_output/"

file_array = os.listdir(indir)



for name in file_array:
    file = indir+name
    if name.startswith('motility_statistics'):
        name = name[20:]
#    if name.endswith('.csv') == False:
#        name = name +'.csv'
    if name.startswith('HM_'):
        name = name[3:]
#    elif name.startswith('M_'):
#        out = indir+'H'+name
#        os.rename(file,out)

    out = indir+name
    if file != out:
        os.rename(file,out)
