# -*- coding: utf-8 -*-
"""
Created on Wed May 30 18:51:49 2018

@author: dani

Run heteromotility on an entire folder

"""

import os
import subprocess as sp

indir = "./2D_migr_test/"
outdir = 'HM_output'
if os.path.isdir(indir+outdir)==0:
    os.mkdir(indir+outdir)

file_array = os.listdir(indir)
count = 0



for name in file_array:
    if name.endswith('csv'):
        count += 1
#        print(name,count)
    #    if name.endswith(".csv_out.csv"):
    #        A = name[0:2]+'_'+name[-26:-24]+'_'+name[-13]+'.csv'
    #        print (A)
    #        file = indir+name
    #        A = indir+A
    #        os.rename(file,A)
    #    print (count)
        
        if count%2 == 1:
            x = indir[2:]+name
        else:
            y = indir[2:]+name
            
            if x[:-5] == y[:-5]:
                
                suffix = name[20:22]+'_'+str(int(count/2))
#                print(suffix)
#                sys.exit()
                
                print ('current data: ' + suffix)
                print('heteromotility.exe',indir[2:]+outdir+'/','--tracksX',x,'--tracksY',y,'--output_suffix',suffix)
                sp.call(['heteromotility.exe',indir[2:]+outdir+'/','--tracksX',x,'--tracksY',y,'--output_suffix',suffix])
                print('--- done')
            else:
                print ('skipped incorrectly paired files:')
                print(x)
                print(y)
                print('---')



#print(x,y,suffix)

#os.system('"C:\\Users\\dani\\Anaconda3\\Scripts\\heteromotility.exe"',indir+'output/','--tracksX',x,'--tracksY',y,'----output_suffix',suffix)
#hm_exe="C:\\Users\\dani\\Anaconda3\\Scripts\\heteromotility.exe"
#sp.call([hm_exe,indir+'output/','--tracksX',x,'--tracksY',y,'----output_suffix',suffix])


#sp.call(['heteromotility.exe',indir[2:]+'output/','--tracksX',x,'--tracksY',y,'--output_suffix',suffix])
#os.system(hm_exe)

#print('heteromotility.exe',indir[2:]+'output/','--tracksX',x,'--tracksY',y,'--output_suffix',suffix)

#sp.call(["heteromotility.exe"])