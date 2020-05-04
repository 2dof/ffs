# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 21:00:41 2020

@author: user
"""

# add parent folder (with ffs modules)  to path
import sys 
sys.path.append("..")

# ======================= import module ======================================                 
import numpy as np
from fuzzy  import *
from fuzzy_sets import * 

from matplotlib.pylab import *
import matplotlib.pyplot as plt
plt.rcParams['lines.linewidth'] = 0.5
plt.rcParams['lines.markersize'] = 2
plt.rcParams["savefig.facecolor"]='white'
plt.rcParams["figure.facecolor"]='white'
plt.rcParams["axes.facecolor"]='white'
plt.ion()

# ======================= build Fuzzy ======================================
# lets create mamdaani fuzzy system with 2 inputs and 1 output and default settings:
# OR methog: 'max' , AND method: 'min'
# Implication method:  'min'  (minimum)
# Aggregation Method:  'max'  (maxsimum)   
# Defuzzyfication Method: 'centroid' (center of gravity)
fis1=fism('mamdani')     # or   fis1=fism()  -> by default mamdani fuzzy system

# add inputs and aoutputs:  input 1 named 'x1' and varianle range from 0 to 2.0
#                           input 2 named 'x3' and varianle range from 0 to 2.0 
#                           output  named 'y1' and varianle range from 0 to 2.0
fis1.addvar('in','x1',[0.,2.0])                
fis1.addvar('in','x2',[0.,2.0])
fis1.addvar('out','y1',[0.,2.0])


# add 3 triangular mf functions to imput 1 
fis1.addmf('in',1,'A1','trimf',[-1,0,1,0])
fis1.addmf('in',1,'A2','trimf',[0,1,2,0])
fis1.addmf('in',1,'A3','trimf',[1,2,3,0])

# add 3 triangular mf functions to imput 2 
fis1.addmf('in',2,'B1','trimf',[-1,0,1,0])
fis1.addmf('in',2,'B2','trimf',[0,1,2,0])
fis1.addmf('in',2,'B3','trimf',[1,2,3,0])

# add 3 triangular mf functions to output 1
fis1.addmf('out',1,'C1','trimf',[-1,0,1,0])
fis1.addmf('out',1,'C2','trimf',[0,1,2,0])
fis1.addmf('out',1,'C3','trimf',[1,2,3,0])

# ======================= plot mfs ======================================
# lets plot membership functions of fis1 system.   
# first lets import dedicated plot functuon from plot_fis class and then
from plot_fis import plot_mfs  

plt.figure(1)
subplot(221);  cla(); plot_mfs(fis1,'in',1)  
subplot(222);  cla(); plot_mfs(fis1,'in',2)      
subplot(212);  cla();plot_mfs(fis1,'out',1)  

# ======================= Add Rules ======================================
# Rule are added as coded list of integers of length (N_inpust+ Noutputs +1]
 
#  for example:
#       Rule: If x1 is A1 AND x2 B2 then output is  C3  
#      coded Rule : R=[1,  2, 3, 1]
#   R[0]=1 means first  (A1) mf of input x1
#   R[1]=2 means second (B2) mf of input x2
#   R[2]=3 means third (C3) mf of  output 1
#   R[3]=1 means AND operator,  for OR oerator will be 0 
#
# examples: if x1 is A2, thed output is C1  -> [a, 0, 1, 1]  , zero means there is no x2 in rule 
#           if x2 is A1 OR x2 is B1 then output is C2  -> [1, 1, 2, 0]  

# lets add Rules to our fuzzy system 
R1=[1,1,1,1]            # Rule 1:  if x1 is A1 and x2 is B1 then y is C1   
R2=[2,2,2,1]            # Rule 2:  if x1 is A2 and x2 is B2 then y is C2  
R3=[3,3,3,1]            # Rule 3:  if x1 is A3 and x2 is B3 then y is C3  

# add rules to fuzzy sytem
fis1.addrule(R1,1.0)        # add rules to the fis1 , weighting parameter  = 1.0
fis1.addrule(R2,1.0)
fis1.addrule(R3,1.0)

# ======================= evaluate (run) fuzzy ================================ 
# test our fuzzy system 
x1 = 0.5 
x2 = 0.5
y1 = evaluate(fis1,[x1, x2])
print(f'fuzzy input:[{x1}, {x2}] output = {y1}')

# compute out of range 
y1 = evaluate(fis1,[-0.5, -0.5])
print ('test for inputs out of range: evaluate(fis1,[-0.5, -0.5]) =', y1)
print('fis1.outOfRange =',fis1.outOfRange)

# compute when no Rule is fired
# for example when   x1=0,5, x2=2 so A1 and B3 is activated, there is no rule for this condition
y1 = evaluate(fis1,[0, 2])          
print ('test for no rule activated: evaluate(fis1,[0.5, 2]) =', y1)
print('fis1.NoRuleFired =',fis1.NoRuleFired)
 


# ======================= plot surface ======================================
# plot fuzzy surface 
#  import lib plot lim for surface plot
from mpl_toolkits.mplot3d.axes3d import Axes3D 
from matplotlib import cm

# get surfase and generate meshgrid
X,Y,Z=getsurf(fis1,25)
X, Y = np.meshgrid(X, Y)


# set up a figure twice as wide as it is tall
fig = plt.figure(4)
ax =  fig.gca(projection='3d')
ax.plot_surface(X, Y, Z, cmap=cm.jet, rstride=1, cstride=1)
ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.title('fuzzy surface')


#========================Add rest of Rules=====================================

fis1.addrule([3, 1, 2, 1],1.0)       # Rule 4
fis1.addrule([1, 3, 2, 1],1.0)       # Rule 5 
#fis1.addrule([2, 1, 1, 1],1.0)       # Rule 6 
#fis1.addrule([1, 2, 1, 1],1.0)       # Rule 7  
#fis1.addrule([2, 3, 3, 1],1.0)       # Rule 8
#fis1.addrule([3, 2, 3, 1],1.0)       # Rule 9


# ====================changing deffuzyfication methon ========================== 
#fis1.Defuzzymethod = 'mom'     # or 'mom', 'som', 'lom', 'bisector'
#fis1.ANDmethod = 'eprod'              # AND method Tnorms: ,'min' ,'prod' , eprod'


X,Y,Z=getsurf(fis1,25)
X, Y = np.meshgrid(X, Y)

# set up a figure twice as wide as it is tall
fig = plt.figure(5); plt.cla()
ax =  fig.gca(projection='3d')
ax.plot_surface(X, Y, Z, cmap=cm.jet, rstride=1, cstride=1)
ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.title('fuzzy surface ')

 
#=======================================================================
 
plt.title('fuzzy surface ')
 