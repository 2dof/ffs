#!/usr/bin/env python3
# -----------------------------------------------------------------------
# fuzzy_sets.py
# -----------------------------------------------------------------------
# This file is part of ffs (fuzzy functional system)
# Copyright (C) @2018@ Szydlowski Lukasz
# mailto:szydlowski.lu@gmial.com
#
#This program is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, version 3 or any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program.
# If not, see http://www.gnu.org/licenses/
# ----------------------------------------------------------------------------------------------
__author__ = "Szydlowski Lukasz"
__copyright__ = "Copyright 2018, szydlowski lukasz"
__license__ = "GPL"
__email__ = "szydlowski.lu@gmial.com"
__status__ = "Development"
__version__ = "1.0.0.dev1"


from mfs import *

def tnorm(x,y,norm_type):
    """
    Return "type" tnorm of input x and y.
    Types of tnorm: "min"  : Minimum sum t-norm
    "prod" : Algebic product t-norm
    "eprod": Einstein product tnorm

    :param x:   value 1
    :param y:   value 2
    :param norm_type: "min", "prod", eprod
    :return: "type" tnorm of (x,y)
    """
    z=0
    # ====== T-NORM =============
    if norm_type=="min":          # MINIMUM-SUM T-NORM
        z=min(x,y)
         
    elif (norm_type=="prod"):     #ALGEBRAIC-PRODUCT T-NORM
        z=x*y

    elif (norm_type=="eprod"):    #EINSTEIN - PRODUCT T - NORM
        a=y*x
        z=2-(y+x-a)
        z= a/z

    return z

def snorm(x,y,norm_type):
    """
    Compute "type" s-norm for input data x,y.
    the s-norm types:"max" - maximum: MAX(x,y),
    "prod" - algebric sum: x + y - xy
    "eprod" - einstein sum: (x + y)/ (1 + xy)

    :param x:   input data 1
    :param y:   input data 2
    :param norm_type: "max", "prod" or "eprod" type snorm
    :return: S-Norm of x,y
    """
    z=1
# ====== s-NORM =============
    if norm_type=="max":          # maximum   S-NORM : MAX(A,B)
        z=max(x,y)
    
    elif (norm_type=="prod"):     #ALGEBRAIC-SUM S-NORM : A + B - AB
        z=x+y-x*y
    
    elif (norm_type=="eprod"):    #EINSTEIN - SUM S - NORM : (A + B)/ (1 + AB)
        a=y*x
        z=(x+y)/(1.+a)

    return z

# ====== complement =============
def complement(x,type):
    """
    Compute complement of x accortdign to "type" metrhod:
    "one" - classic complement, "sugeno" - sugeno complement

    :param x:    imput
    :param type:  "one" or "sugeno" type complement
    :return: complement of input x 
    """
    a=1
    y=0.0
    if (type=="one"):         # classic complement
        y=1-x
    elif (type=="sugeno"):
        tmp1 = 1.0/a
        y=(1.0-a*x)*tmp1       # sugeno complement
    
    return y


def defuzzy(y, method):
    """
    Defuzzify membership function with defined method.
    'centroid'  -CENTROID
    'mom'        MEAN OF MAXIMUM (MOM)
    'som'        SHORTEST OF MAXIMUM (SOM)
    'lom'        LARGEST OF MAXIMUM (LOM)
    'bisector'   BISECTOR

    :param y:
    :param method: defuzzy method: 'centroid','mom','som','lom','bisector
    :return: None
    """
    tmp = 0
    out = 0

    if method == 'centroid':  # centroid
        tmp = np.sum(y)
        for i in range(0, len(y)):
            out = out + i * y[i]

        out = out / float(tmp)

    elif method == 'mom':  # MEAN OF MAXIMUM (MOM)
        out = 0
        tmp = y[0]
        tmp1 = 1.
        for i in range(1, len(y)):
            if (y[i] == tmp):
                out += i
                tmp1 += 1.
            elif y[i] > tmp:
                out = i
                tmp = y[i]

        out = out / tmp1

    elif method == 'som':  # SHORTEST OF MAXIMUM (SOM)
        out = 0
        tmp = y[0]
        for i in range(1, len(y)):
            if y[i] == tmp:
                if i < out:
                    out = i

            elif y[i] > tmp:
                tmp = y[i]
                out = i

    elif method == 'lom':  # LARGEST OF MAXIMUM (LOM)
        out = 0
        tmp = y[0]
        for i in range(1, len(y)):
            if y[i] == tmp:
                if i > out:
                    out = i

            elif y[i] > tmp:
                out = i
                tmp = y[i]
                
    elif method == 'bisector':
        out = 0
        tmp=np.sum(y)
        if tmp>0:
            tmp=tmp/2.0
            tmp1=0.0
            for i in range(0,len(y)):
                tmp1+=y[i]
                if tmp1>=tmp:
                    out=i
                    break

    return out

def evaluate(fis,x):
    """
    Compute fuzzy output of fis system for inputs x=[x1,x2...]

    :param fis: fuzzy structure (fism class) of fuzzy system
    :param x:   input vector data
    :return:    fuzzy out
    """
    in_mfcsum= [0] * (fis.Ninputs+1)
            
    for i in range(1,fis.Ninputs+1):
        in_mfcsum[i]=in_mfcsum[i-1]+fis.Nin_mf[i-1]
        
    tmp=[0]*fis.Ninputs 
    tmp2=[0]*fis.NRules
    
    for rule in range (0,fis.NRules):
        for inp in range(0,fis.Ninputs):

            idx=abs(fis.RuleList[rule,inp])
            isgn=np.sign(fis.RuleList[rule,inp])

            if (idx > 0):
                pt1 = idx + in_mfcsum[inp]-1
                tmp[inp] = eval_mf(x[inp],fis.mfpari[pt1][:])
                
                if (isgn <0):      # not 
                     tmp[inp] = complement(tmp[inp],"one")
                     
            elif fis.RuleList[rule,fis.Ninputs+fis.Noutputs]==0: #   OR
                tmp[inp] =0
            else:                   # =1 : AND 
                tmp[inp] =1
    
        # snomr/ T norm
        if fis.RuleList[rule,fis.Ninputs+fis.Noutputs]==0:
            y=tmp[0]
            for i in range(1,fis.Ninputs):    
                y=snorm(tmp[i],y,fis.ORmethod)
            
            tmp2[rule]=y*fis.RuleWeights[rule] 
            
        else:
            #print('AND operator')
            y=tmp[0]
            for i in range(1,fis.Ninputs):    
                y=tnorm(tmp[i],y,fis.ANDmethod)
            
            tmp2[rule]=y*fis.RuleWeights[rule] 
    
    # defuzzyfication-------------------------
    y = [0]*fis.Noutputs
    out_mfcsum = [0] * (fis.Noutputs + 1)

    for i in range(1, fis.Noutputs + 1):
        out_mfcsum[i] = out_mfcsum[i - 1] + fis.Nout_mf[i - 1]
   # - mamdani
    if fis.type=='mamdani':

        for outp in range(0,fis.Noutputs):

            tmp3 = np.zeros((fis.Npts, 2))
            ranges=fis.varRange[fis.Ninputs+outp]
            dx = np.abs(ranges[1]-ranges[0])/ fis.Npts

            for rule in range (0,fis.NRules):

                idx=abs(fis.RuleList[rule, fis.Ninputs+outp])
                isgn=np.sign(fis.RuleList[rule,fis.Ninputs+outp])

                if idx>0:
                    pt1 = idx + out_mfcsum[outp]-1

                    for i in range(0,fis.Npts):
                        tmp3[i,1]=eval_mf(i*dx,fis.mfparo[pt1][:])

                    if isgn<0:
                        for i in range(0,fis.Npts):
                            tmp3[i,1]=complement(tmp3[i,1],"one")

                #implication
                if fis.Implmethod =='min':

                     for i in range(0,fis.Npts):
                            tmp3[i,1]=min(tmp3[i,1],tmp2[rule])

                elif fis.Implmethod =="eprod": #einstein product

                     for i in range(0,fis.Npts):
                            tmp3[i,1]=tnorm(tmp3[i,1],tmp2[rule],"eprod")

               # Aggregation
                if fis.Aggmethod == 'max':
                    for i in range(0,fis.Npts):
                        tmp3[i,0]=max(tmp3[i,0],tmp3[i,1])

                elif  fis.Aggmethod == 'sum''sum':         #  sum

                    for i in range(0,fis.Npts):
                        tmp3[i,0]=tmp3[i,0]+tmp3[i,1]

                elif  fis.Aggmethod == 'eprod':         #   einstein sum

                    for i in range(0,fis.Npts):
                        tmp3[i,0] = snorm(tmp3[i,0],tmp3[i,1],"eprod")

                elif  fis.Aggmethod == 'prod':         #   Algebric sum
                    for i in range(0,fis.Npts):
                        tmp3[i,0] = snorm(tmp3[i,0],tmp3[i,1],"prod")


            y[outp] = dx*defuzzy(tmp3[:,0],fis.Defuzzymethod)-ranges[0]

    elif fis.type == 'tsk':
        for outp in range(0, fis.Noutputs):
            sum1 = 0.0
            sum2 = 0.0
            for rule in range(0, fis.NRules):

                idx = abs(fis.RuleList[rule, fis.Ninputs + outp])
                if ((tmp2[rule]>0) & (idx > 0)):
                    pt1 = idx + out_mfcsum[outp] - 1
                    param = fis.mfparo[pt1][:]
                    gi = param[0]
                    for i in range(0, fis.Ninputs):
                        gi += param[i + 1] * x[i]

                    sum1 += tmp2[rule] * gi
                    sum2 += tmp2[rule]

            y[outp] = sum1 / sum2
          
    return y


def getsurf(fis,Npts,in1=1,in2=2,out=1):
    """
    Generate fuzzy system surface

    :param fis:  fis structure
    :param Npts: No of points
    :param in1: No of input 1
    :param in2: No of input 2
    :param out: No of outpt
    :return: X,Y,Z - x,y cooordinates and z: data surface value
    """
    dx1 = (fis.varRange[in1-1][1]-fis.varRange[in1-1][0])/float(Npts)
    dx2 = (fis.varRange[in2-1][1]-fis.varRange[in2-1][0])/float(Npts)
    Z = np.zeros((Npts+1,Npts+1))
    for i in range(0,Npts+1):
        for j in range(0,Npts+1):
            Z[i, j]=evaluate(fis,[dx1*i,dx2*j])[out-1]

    X = np.array(range(0, Npts + 1)) * dx1
    Y = np.array(range(0, Npts + 1)) * dx2

    return X,Y,Z