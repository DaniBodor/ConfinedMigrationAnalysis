# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 14:33:09 2018

@author: dani

Takes trackmate data files and extracts x- and y-coordinates for heteromotility input
31 Aug 2018 version seems stable
"""

import pandas as pd
import csv
import itertools
import os
from random import randint
from random import seed as rseed
import numpy as np
import datetime


### set length of output data
# any tracks shorter than this will be scrapped
# any tracks longer than this will use a random segment of set length
# this script will also output a csv with the (complete) length of all tracks in file,
#                               which can be used to check what a good setting for below would be
outLength = 60
#set random seed for integer generation to make track segment generation reproducible between runs
rseed(22)

input_dir = './TrackMate_Analysis/'
Length_outfile = input_dir+'_trackLengths.csv'
XY_outdir = input_dir+"XY_data_%d/"%(outLength)

if not os.path.exists(XY_outdir):
    os.makedirs(XY_outdir)

start = str(datetime.datetime.now().time())[:8]

LenDict = {}


file_array = [f for f in os.listdir(input_dir) if (f.endswith('SpotsStats.csv') and not f.startswith('_'))]
#file_array = [f for f in os.listdir(input_dir) if (f.endswith('csv') and f.startswith('Stitch_180802_2Dmig_BSA_CTVi+CTFR_6um_006.tif --- '))]
#file_array = [f for f in os.listdir(input_dir) if (f.endswith('csv') and f.startswith('000'))]
#file_array = [f for f in os.listdir(input_dir) if (f.endswith('.csv') and not f.startswith('_'))]

counter = 0
for filename in file_array:
    X_outfile = XY_outdir+filename.replace('.csv','_x.csv').replace(' ','')
    Y_outfile = XY_outdir+filename.replace('.csv','_y.csv').replace(' ','')
    
    print(filename)
    try:
        input_df = pd.read_csv(input_dir + filename, usecols = ['TRACK_ID', 'FRAME', 'POSITION_X', 'POSITION_Y'])
    
        # Remove centroids without an assigned track and sort for track id
        if input_df.TRACK_ID.dtype != 'int64':
            input_df = input_df[input_df.TRACK_ID != 'None'] 
            input_df.TRACK_ID = input_df.TRACK_ID.apply(pd.to_numeric)
        input_df = input_df.sort_values(['TRACK_ID', 'FRAME'])
        
        # create list of unique track numbers and initialize lists/dictionaries for data storage
        tracklist=input_df['TRACK_ID'].unique().tolist()
        LenList = []
        xDict = {}
        yDict = {}
        
        # find data per track
        for track in tracklist:
#          if counter <11:
            trackdf = input_df.loc[input_df['TRACK_ID'] == track]
#            print(track,'',end='')
            
            
            ## rest of for loop needs testing!!!
            ## not sure how best to test, probably fabricate tracks of 120 tps with info that represents potential errors:
            ## 1) split track record
            ## 2) track with missing point in middle
            ## 3) of different lengths, etc

            # scrap split tracks (= dividing cells?)
            # solving by disallowing track splitting no good, because that will cause 1 long and 1 short track
            trackdf = trackdf.drop_duplicates(subset = 'FRAME',keep=False)
            # next, keep only longest uninterupted track
            # ideally all uninterrupted tracks >outLength, but this is good enough I guess
            frames = np.array(trackdf['FRAME'])
            longest_unint_track = max(np.split(frames, np.where(np.diff(frames) != 1)[0]+1), key=len).tolist() 
            # create length list
#            trackMax = max(longest_unint_track)
#            trackMin = min(longest_unint_track)
            Length = len(longest_unint_track)
            LenList.append(Length)
            
            
            
            # create x- and y- coordinates for each position in each track
            if Length >= outLength:
                first_tp = randint(0, Length - outLength) + min(longest_unint_track)
                last_tp = first_tp + outLength
#                print (first_tp)
                x_track = trackdf['POSITION_X'] [ (trackdf['FRAME']>=first_tp) & (trackdf['FRAME']<last_tp) ]
                x_maxdiff = x_track.max()-x_track.min()
                y_track = trackdf['POSITION_Y'] [ (trackdf['FRAME']>=first_tp) & (trackdf['FRAME']<last_tp) ]
                y_maxdiff = y_track.max()-y_track.min()
                
                
                # 0 total displacement in either x or y crashes heteromotility
                # not sure why, but some (few) tracks have only outLength-1 entries, these crash heteromotility too
                # potentially due to track linking with missing point
                if x_maxdiff > 0 and y_maxdiff > 0 :
                    xDict[track] = x_track
                    yDict[track] = y_track
#                    counter +=1
        
            
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


end = str(datetime.datetime.now().time())[:8]

print(start)
print(end)
print ('finished script with no errors')