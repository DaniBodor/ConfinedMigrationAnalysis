# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 14:33:09 2018

@author: dani

Takes trackmate data files and extracts x- and y-coordinates for heteromotility input
31 Aug 2018 version seems stable
"""

import pandas as pd
#from os import listdir
import csv
import itertools
import os
from random import randint
from random import seed as rseed


### set length of output data
# any tracks shorter than this will be scrapped
# any tracks longer than this will use a random segment of set length
# this script will also output a csv with the (complete) length of all tracks in file,
#                               which can be used to check what a good setting for below would be
outLength = 120
#set random seed for integer generation to make track segment generation reproducible between runs
rseed(22)

input_dir = './TrackMate_Analysis/'
Length_outfile = input_dir+'_trackLengths.csv'
XY_outdir = input_dir+"XY_data/"

if not os.path.exists(XY_outdir):
    os.makedirs(XY_outdir)



LenDict = {}


file_array = [f for f in os.listdir(input_dir) if (f.endswith('SpotsStats.csv') and not f.startswith('_'))]
#file_array = [f for f in os.listdir(input_dir) if (f.endswith('csv') and f.startswith('Stitch_180802_2Dmig_BSA_CTVi+CTFR_6um_006.tif --- '))]
#file_array = [f for f in os.listdir(input_dir) if (f.endswith('csv') and f.startswith('000'))]

for filename in file_array:
    X_outfile = XY_outdir+filename.replace('.csv','_x.csv').replace(' ','')
    Y_outfile = XY_outdir+filename.replace('.csv','_y.csv').replace(' ','')
    
    print(filename)
    try:
        df = pd.read_csv(input_dir + filename, usecols = ['TRACK_ID', 'POSITION_T', 'POSITION_X', 'POSITION_Y'])
    
        # Remove centroids without an assigned track and sort for track id
        if df.TRACK_ID.dtype != 'int64':
            df = df[df.TRACK_ID != 'None'] 
            df.TRACK_ID = df.TRACK_ID.apply(pd.to_numeric)
        df = df.sort_values(['TRACK_ID', 'POSITION_T'])
        
        # create list of unique track numbers and initialize lists/dictionaries for data storage
        tracklist=df['TRACK_ID'].unique().tolist()
        LenList = []
        xDict = {}
        yDict = {}
        
        # find data per track
        for track in tracklist:
            trackdf = df.loc[df['TRACK_ID'] == track]
            # create length lists per track
            trackMax = trackdf['POSITION_T'].max()
            trackMin = trackdf['POSITION_T'].min()
            Length = trackMax - trackMin
            LenList.append(Length)
        
            # create x- and y- coordinates for each position in each track
            if Length >= outLength:
                first_tp = randint(0,Length - outLength)
                last_tp = first_tp + outLength
#                print (first_tp)
                x_track = trackdf['POSITION_X'] [first_tp : last_tp]
                x_maxdiff = x_track.max()-x_track.min()
                y_track = trackdf['POSITION_Y'] [first_tp : last_tp]
                y_maxdiff = y_track.max()-y_track.min()
                
                # 0 total displacement in either x or y crashes heteromotility
                if x_maxdiff > 0 and y_maxdiff > 0 and len(x_track)==120 and len(y_track)==120:
                    xDict[track] = x_track
                    yDict[track] = y_track
        
        # skip if no tracks (of sufficient length) were found
        if len(LenList) > 0:
            # write length data to dictionary    
            LenDict[filename] = LenList
    
            # write x- and y-data to csv
            with open(X_outfile, 'w',newline='') as X_outfile:
                w = csv.writer(X_outfile)
                for key,value in xDict.items():
                    w.writerow([*round(value,3)])
            with open(Y_outfile, 'w',newline='') as Y_outfile:
                w = csv.writer(Y_outfile)
                for key,value in yDict.items():
                    w.writerow([*round(value,3)])

    except pd.io.common.EmptyDataError:
        print ('----' + filename + ' is empty; skipping')
        pass


# write length data to csv
with open(Length_outfile, 'w',newline='') as L_outfile:
    w = csv.writer(L_outfile)
    w.writerow(LenDict.keys())
    w.writerows(itertools.zip_longest(*LenDict.values()))



print ('finished script with no errors')