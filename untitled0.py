# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 13:13:30 2018

@author: dani
"""


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from matplotlib import colors as mcolors

iris = sns.load_dataset('iris')


f1,ax1 = plt.subplots(1,2)
sns.barplot(x='sepal_length', y='species', data=iris,ax=ax1[0])

f2,ax2 = plt.subplots(1,2)
sns.barplot(x='sepal_width', y='species', data=iris,ax=ax2[0])


sns.barplot(x='sepal_width', y='species', data=iris,ax=ax1[1])

sns.barplot(x='sepal_length', y='species', data=iris,ax=ax2[1])



#
#for i in range(2):
#    for j in range(2):
#        plt.figure(i)
#        f,ax = plt.subplots(1,2)
#        sns.barplot(x='sepal_length', y='species', data=iris,ax=ax[j])
#        sns.barplot(x='sepal_width', y='species', data=iris,ax=ax[j])
#
#    
