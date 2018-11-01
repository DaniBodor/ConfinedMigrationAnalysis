# -*- coding: utf-8 -*-
"""
Created on Wed May 30 18:51:49 2018

@author: dani

Run heteromotility on an entire folder

I have updated 2 things in heteromotility package from how it was downloaded to better fit my needs:
1) replaced heteromotilty output filename to something shorter 
    in heteromotility.py, check_flags definition, lines 136 & 138
2) scrapped empty lines between each entry in the output files (Python 2.7 to 3.5 conversion bug)
    in hmio.py, added newline arg to line 90
    line 90 now reads >> with open(output_file_path, 'w',newline='') as out_file:
this could be relevant if heteromotility updates come out...


Also, I believe that it's possible to just run heteromotility.py from here or whatever.
Should check this (according to github site)
Current script takes ~1-1.5 minutes / file
I wonder how much (if at all) faster it is by calling .py file rather than subprocess

31 Aug 2018 version seems stable
"""

import os
import subprocess as sp
import datetime
#import re

move_thresh = 1     # set to number or 'def'

indir = "./TrackMate_Analysis/XY_data_60/"
indir = 'Z:/GFP4/180927/TrackMate_Analysis/XY_data_60/'
outdir = 'HM_output-move_thresh_%s/'%move_thresh
if not os.path.exists(indir+outdir):
    os.makedirs(indir+outdir)

file_array = os.listdir(indir)
outdir_files = os.listdir(indir+outdir)

#ditch = ['Stitch_' , '.tif' , '---' , '_SpotsStats']
#
#
#def scrap_filename(string,ditch_list):
#    '''
#    scraps each instance in string of each string entry of ditch_list
#    '''
#    rep = {ditch_list[i]: '' for i in range(len(ditch))}
#    rep = dict((re.escape(k), v) for k, v in rep.items())
#    pattern = re.compile("|".join(rep.keys()))
#    out = pattern.sub(lambda m: rep[re.escape(m.group(0))], string)
#    return out


done_count = len(outdir_files)
skip_count = 0
error_count = 0
fail_list = []
move_thresh = str(move_thresh)


start = str(datetime.datetime.now().time())[:8]


for name in file_array:
    if 1==0:        # replace by line below if I want to skip files already processed
#    if 'HMout_'+name[:-6]+'.csv' in outdir_files:
#        print ('already processed: '+name)
        q=0
    elif name.endswith('_x.csv'):

        x = indir[2:]+name
        y = x.replace('_x.csv','_y.csv')
        
        if os.path.exists(y):
            print (str(datetime.datetime.now().time())[:8])
            
            base_name = name[:-6]
            
            print ('current data: ' + base_name)
            if move_thresh == 'def':
                print  ( 'heteromotility.exe',indir[2:]+outdir,'--tracksX',x,'--tracksY',y,'--output_suffix',base_name )
            else:
                print  ( 'heteromotility.exe',indir[2:]+outdir,'--tracksX',x,'--tracksY',y,'--output_suffix',base_name,'--move_thresh',move_thresh)
            
            # this statement isn't catching my errors (I think because it's python exceptions, not bash errors)
            # but at least it's running heteromotility ok
            try:
                if move_thresh == 'def':
                    sp.call(['heteromotility.exe',indir[2:]+outdir,'--tracksX',x,'--tracksY',y,'--output_suffix',base_name])
                else:
                    sp.call(['heteromotility.exe',indir[2:]+outdir,'--tracksX',x,'--tracksY',y,'--output_suffix',base_name,'--move_thresh',move_thresh])
                
                done_count+=1
                print('--- done '+str(done_count))
            except sp.CalledProcessError as error:
                print(error.message)
                print('not saved '+str(error_count))
                fail_list.append(base_name)
                
        else:
            print (y + "does'nt exist")
            print('--- skipped')
            skip_count+1
            
print('started at  ',start)
print('finished at ',str(datetime.datetime.now().time())[:8])

print ('all done')