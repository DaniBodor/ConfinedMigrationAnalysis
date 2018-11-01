#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Splitting ImageJ spot statistics csv into two tables with x and y coordinates of spots
Only considering full length tracks
"""

import pandas as pd
#import numpy as np
from os import listdir
#import sys
import os


timepoints = 120 # number of frames to use per sample
section = 'end' # options are: 'begin' / 'middle' / 'end'


input_dir = './'

#file_array = ["CTRL-001_SpotStats.csv","CK666-002_SpotStats.csv","CK666-003_SpotStats.csv","EGTA-004_SpotStats.csv"]
#file_array = ["CTRL-010","EGTA-011"]
#filename = "CTRL-000_SpotStats.csv"

file_array = [f for f in listdir(input_dir) if f.endswith('csv')]

#print(file_array)
#
#sys.exit()

# Read in *filename* with columns: track id, time and x and y coordinates
# of centroids


for filename in file_array:

    print ('Reading ' + input_dir + filename)
    df = pd.read_csv(input_dir + filename, usecols = ['TRACK_ID', 'POSITION_T', 'POSITION_X', 'POSITION_Y'])

    
    # Remove centroids without an assigned track and sort for track id
    if df.TRACK_ID.dtype != 'int64':
        df = df[df.TRACK_ID != 'None'] 
        df.TRACK_ID = df.TRACK_ID.apply(pd.to_numeric)
    df = df.sort_values(['TRACK_ID', 'POSITION_T'])

    
    print("OK")
    output_dir = input_dir+"XY_data/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Extract x coordinates, delete rows with NaN values and save to csv
    x_df = df.pivot( index = 'TRACK_ID' , columns= 'POSITION_T', values='POSITION_X')
    y_df = df.pivot( index = 'TRACK_ID' , columns= 'POSITION_T', values='POSITION_Y')
    x_df_clear = x_df[x_df>0][y_df[x_df>0]>0].dropna()
    x_df_clear.to_csv(output_dir + filename.replace('.csv', '') +'_x.csv',header = False, index = False,newline='')
    # added newline arg above, not sure if that will make it crash....
    
    
    
    print ("Wrote " + filename.replace('.csv', '') +'_x.csv' + ' to ' + output_dir)
    # Extract y coordinates, delete rows with NaN values and save to csv
    
    
    y_df_clear = y_df[x_df>0][y_df[x_df>0]>0].dropna()
    
    y_df_clear.to_csv(output_dir + filename.replace('.csv', '') +'_y.csv', header= False, index = False)
    print ("Wrote " + filename.replace('.csv', '') +'_y.csv' + ' to ' + output_dir)
#    sys.exit()
    