# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 14:23:13 2020

@author: "Szydlowski Lukasz"
"""
__author__ = "Szydlowski Lukasz"
__copyright__ = "Copyright 2020, szydlowski lukasz"
__license__ = "GPL"
__email__ = "szydlowski.lu@gmail.com"
__status__ = "Development"
__version__ = "1.0.1"



import matplotlib.pyplot as plt
plt.rcParams['lines.linewidth'] = 1
plt.rcParams['lines.markersize'] = 2
plt.rcParams["savefig.facecolor"]='white'
plt.rcParams["figure.facecolor"]='white'
plt.rcParams["axes.facecolor"]='white'
plt.ion()

from fuzzy  import *
from fuzzy_sets import * 
import numpy as np
import mfs

def plot_mfs(fis,var_type,No):


    mfs_list = fis.getmf(var_type,No)
    
    if (var_type == 'in'):
       N = fis.Nin_mf[No-1] 
    else: 
       N=fis.Nout_mf[No-1] 
   
    
    for i in range(0,N):
        if (mfs_list[i][1] =='trimf'):
            X = mfs_list[i][2][1:]
            Y = np.array([0,1,0])
            xs=X[1]
        elif (mfs_list[i][1] =='trapmf'):
            X = mfs_list[i][2][1:]
            Y = np.array([0,1,1,0])
            xs=X[1]+(X[2]-X[1])/2
        elif (mfs_list[i][1] =='singleton'):
            xo=mfs_list[i][2][1]
            print('x0',xo)
            X=np.array([xo,xo])
            Y=np.array([0,1])
            xs=xo
        else:
            print('------------')
            Npts=101
            dx1 = np.abs(fis.varRange[No-1][1]-fis.varRange[No-1][0])/float(Npts)
            X= np.array(range(0, Npts + 1)) * dx1+fis.varRange[No-1][0]
            Y= np.zeros([len(X)])
            param=mfs_list[i][2]
            xs =param[2]
            for k in range(0,len(X)):
                Y[k]=mfs.eval_mf(X[k],param)
       
        print(xs)
        plt.plot(X,Y); plt.text(xs, 1.,mfs_list[i][0], fontsize=10)
        
   
    plt.ylabel(var_type+' '+str(No))    
    plt.grid(True) 
    plt.ylim(-0.1, 1.2) 