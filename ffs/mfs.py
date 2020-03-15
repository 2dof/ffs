#!/usr/bin/env python3
# coding=utf-8
# -----------------------------------------------------------------------
# mfs.py
# -----------------Copyrights and license ------------------------------------------------------
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

import numpy as np


mftypes=['trimf','trapmf','gaussmf','gauss2mf','gbellmf','sigmf','singleton']

def trimf(xn,param):
    """
    Compute value of triangular membership function
    :math:`f(x_n,a,b,c)=max(min((x-a)/(b-a),(c-x)/(c-b)),0)`.

    :param xn: input value
    :param param: [1x3] vector: param[0]=a,param[1]=b,param[2]=c
    :type xn: float
    :type param: float
    :return: value of triangular mf
    :rtype: float
    """
    return max(min((xn-param[0])/(param[1]-param[0]),(param[2]-xn)/(param[2]-param[1])),0)


def trapmf(xn,param):
    """
    Trapezoidal membership function
    compute value of trapezoidal shape function.
    trapezoid is described by parameters: :math:`a<=b <=c <= d`

    :param xn: input value
    :param param: ([1x4] vector) Trapezoid parameters: param=[a,b,c,d]
    :type xn: float
    :type param: float
    :return: value of Trapezoid mf
    :rtype: float
    """
    a = param[0]
    b = param[1]
    c = param[2]
    d = param[3]
    y=0
    if ((xn < a)|(xn > d)):
        y=0
    elif (xn < b):
        y=(xn-a)/(b-a)
        
    elif ((xn>=b)&(xn<=c)):
        y=1
    else:
        y=(d-xn)/(d-c)
    
    return y

def gaussmf(xn,param):
    """
    Compute gaussian function membership
    return value  of symmetric Gaussian function
    :math:`gaussmf(x,[\sigma,c])= e^{\\frac{-(x-c)^2}{2\sigma^2}}`

    :param xn:  input sample
    :param param: [1x2] vector  = [sigma value, expected value]
    :type xn: float
    :type param: float
    :return: return value  of symmetric Gaussian function
    :rtype: float
    """
    sigma=param[0]
    c=param[1]
    if (sigma==0):
        sigma=1
        
    tmp1=-(xn-c)**2
    tmp2=2.0*(sigma**2)
    
    return np.exp(tmp1/tmp2)
    
def gauss2mf(xn,param):
    """
    Compute nonsymmetric gaussian function membership
    return value  of nonsymmetric Gaussian function depends of param=[σ1, c1,σ2, c2]

    :param xn: input sample
    :param param: [sigma1, const.1,sigma 2, const.2]
    :type xn: float
    :type param: float
    :return: value of nonsymmetric Gaussian function
    :rtype: float
    """
    sigma1=param[0]
    c1=param[1]
    sigma2=param[2]
    c2=param[3]
    
    if xn<=c1:
        tmp1=-(xn-c1)**2
        tmp2=2.0*sigma1**2    
        
    elif xn>=c2:
        tmp1=-(xn-c2)**2
        tmp2=2.0*sigma2**2
    else:
         tmp1=0.0
         tmp2=1.0
    
    return np.exp(tmp1/tmp2)


def gbellmf(xn,param): # TODO description
<<<<<<< HEAD
    """ 
        Generalized bell-shaped membership function
        retur value of Generalized bell-shaped function:
        :math: `f(x,a,b,c) = gbellmf[x,[a,b,c]] = 1/(1+(abs((x−c)/a))^2b)`.
        :param xn:      input value,
        :param param: [a,b,c],
        :type xn:         float,
        :type param:    float,
        :return:           value of Generalized bell-shaped,
        :rtype:            float,
    """ 
=======
    """
    Generalized bell-shaped membership function
    retur value of Generalized bell-shaped function:
    :math:`f(x,a,b,c)= gbellmf[x,[a,b,c]] = 1/(1+(abs((x−c)/a))^2b)`.

    :param xn: input value
    :param param: [a,b,c]
    :type xn: float
    :type param: float
    :return: value of Generalized bell-shaped
    :rtype: float

    """
>>>>>>> 326973819667aec49e1336fb0f350bfa151a3155
    a = param[0]
    b = param[1]
    c = param[2]
    
    tmp1 = np.abs((xn-c)/float(a))
    tmp2 =tmp1**(2*b)

    return 1/(1+tmp2)
    

def sigmf(xn,param): # TODO description
    """
    Sigmoidal membership function

    :math: 'f(x,[a,c]) = sigmf[x,[a,c]] = 1/(1+exp(-a(x−c)))'

    :param xn: input value
    :param param: =[a,c]
    :type xn: float
    :type param: float
    :return: value of sigmoidal function
    :rtype: float

    """
    a = param[0]
    c = param[1]
    tmp1=np.exp(-a*(xn-c))
    return 1/(1+tmp1)   
    
    
def singletonmf(xn,param):
    """
    singleton function

    :param xn:  input value
    :param param: [x0]
    :return:
    """

    a = param[0]
    y=0
    if (xn==a):
        y=1

    return y 
    
    

def eval_mf(xn,params):
    """
    Return value of mf function for input xn.
    type, and parameters of mf stored in params vector where:
    params=[mf code, mf params] :
    mf code: 0='trimf',1='trapmf',3='gaussmf',4='gauss2mf',5='gbellmf',6='sigmf',7='singleton']

    :param xn: input value
    :param params: [mf code, mf params]
    :type xn: float
    :type params: vector
    :return:  value of mf an xn
    """
    mf_type=params[0]
    y = 0.0
    
    if mf_type==0 :   # 'trimf'
        y=trimf(xn,params[1:])

    elif mf_type == 1:                         # trapmf
        y = trapmf(xn, params[1:])        #

    elif mf_type == 2:                         # gaussmf
        y = gaussmf(xn, params[1:])      #

    elif mf_type == 3:                         # gauss2mf
        y = gauss2mf(xn, params[1:])    #

    elif mf_type == 4:                         # gbellmf
        y = gbellmf(xn, params[1:])        #

    elif mf_type == 5:                         # sigmf
        y = sigmf(xn, params[1:])          #

    elif mf_type == 6:  # singletonmf
        y = singletonmf(xn, params[1:])
    else:
        y=0

    return y