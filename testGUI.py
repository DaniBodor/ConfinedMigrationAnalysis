# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 14:50:16 2018

@author: dani
"""

import tkinter as tk
import os
import itertools


fileDict = {}


def gui():
    master=tk.Tk()
    files=next(os.walk('forms'))[2]
    i=1
    for f in files:
        var = tk.IntVar()
        tk.Checkbutton(master, text=f, variable=var).grid(row=i)
        fileDict[f] = var
        i+=1
    master.mainloop()

gui()
#for (name, var) in fileDict:
#    print(name, var.get())
