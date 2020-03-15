#!/usr/bin/env python3
# -----------------------------------------------------------------------
# fuzzy.py
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
from mfs import mftypes


class fism:
    """
    Class object storing settings and configuration parameters (data attributes)
    for Fuzzy Mamdani or Tagaki-Sugeno type Fuzzy system.\n
    By default initialization mamdani type fuzzy is set with settings:\n
    **ANDmethod:** Tnorm 'min'\n
    **ORmethod:**  Snorm 'max'\n
    **Implication method:** Tnorm 'min'\n
    **Aggregation method:**  'max'\n
    **Deffuzyfication method:** 'centroid'\n

    .. note:: fism in ver.1.0.0 is only fuzzy structure container. Fuzzy Inference Process is implemented by evaluate(fis,x) from fuzzy_sets.py.

    =================   ==============   ========================================================
    Atributes           format           Description
    =================   ==============   ========================================================
    **type**            string           ='mamdani' or 'tsk' : type of fuzzy system
    **Ninputs**         Int              Number of inputs
    **Noutputs**        Int              Number of outputs
    **varName**         string           list, store of variable names
    **varRange**        [float,float]    store of variable physical range
    **ORmethod**        string           default:'max' other: 'prod' 'eprod
    **ANDmethod**       string           default 'min' , other: ,'prod' , eprod'
    **Implmethod**      string           Implication method, default: 'min' . other:'tnorm eprod'
    **Aggmethod**       string           Aggregation Method, default: 'max'
    **Defuzzymethod**   string           Defuzzyfication Method, defalult: 'centroid'
    **RuleList**        2D int array     store rules (Array Nrules x(Ninputs+Noutputs+1
    **RuleWeights**     1D float array   list of Rule's weights
    **mfnames_in**      string list      list, names of input's mf
    **mfnames_out**     string           list, names of output's mf
    **mfpari**          2D float array   array list of inputs mf types and parameters
    **mfparo**          2D float array   array list of outrputs mf types and parameters
    **Nin_mf**          Int list         list, Numbenr of inputs mf  [N_mf in1, N_mf in2...]
    **Nout_mf**         Int list         list, Numbenr of inputs mf  [N_mf out1, N_mf out2...]
    **Npts**            Int              No of points resolution for defuzzyfication process
    =================   ==============   ========================================================

    **Example initialization**

    .. code-block:: python

        from fuzzy  import *
        from fuzzy_sets import *

        fis1 = fism()               # empty mamdani fuzzy structure
        fis2 = fism('mamdani',2,1)  # 2 input, 1 output mamdani fuzzy structure

    """
    def __init__(self, type ='mamdani', Ninputs =0 ,Noutputs = 0):
        """
        Initialize fuzzy data structure for fuzzy system
        """
        self.type = type                    # 'mamdani' or 'tsk'
        self.ORmethod = 'max'               # OR method Snorms: 'max', 'prod' 'eprod'
        self.ANDmethod = 'min'              # AND method Tnorms: ,'min' ,'prod' , eprod'
        self.Implmethod = 'min'             # Implication method: tnorm eprod
        self.Aggmethod = 'max'              # Aggregation Method:'sum','eprod' , 'prod'
        self.Defuzzymethod = 'centroid'     # or 'mom', 'som', 'lom', 'bisector'
        self.NRules =0
        self.RuleList =(np.zeros((1,0 +0+1))).astype(int)
        self.RuleWeights=[1.0]*self.NRules

        self.Ninputs    =0                  # (int)
        self.Noutputs   =0                  # (int)
        self.varName = []  # list of variablee names
        self.varRange = []  # list of variables range

        self.Nin_mf = [0]*self.Ninputs
        self.Nout_mf = [0] * self.Noutputs

        if Ninputs>0:
            for i in range(Ninputs):
                self.addvar('in', 'in'+str(i+1),[0,100])
        if Noutputs > 0:
            for i in range(Noutputs):
                self.addvar('out', 'out' + str(i + 1), [0, 100])

        self.mfnames_in = ['A1']
        self.mfnames_out = ['y1']

        self.mfpari = np.zeros((1, 5))  # [type,param1,param2,param3,param3

        if self.type =='mamdani':
            self.mfparo=np.zeros((1,5)) #[type,param1,param2,param3,param3
        elif self.type =='tsk':
            if self.Ninputs<=5:
                self.mfparo = np.zeros((1, 5))  # [type,param1,param2,param3,param3
            else:
                self.mfparo = np.zeros((1, self.Ninputs))  # [type,param1,param2,param3,param3

        self.Npts =100


    def addvar(self,type,name,range):
        """
        Add variable (input or output) to the fuzzy system

        :param type: 'in' or 'out'
        :type type: string
        :param name: name of variable
        :type name: string
        :param range: [min,max] range value of variable
        :type tange: [double,double]

        **Example**

        .. code-block:: python

            fis1.addvar('in','x1',[0.,3.0])
            fis1.addvar('in','x2',[0.,3.0])
            fis1.addvar('out','y1',[0.,3.0])

        """
        if (type=='in'):
            self.varName.insert(self.Ninputs,name)
            self.varRange.insert(self.Ninputs,range)
            self.Ninputs += 1
            self.RuleList = np.insert(self.RuleList, self.Ninputs-1, values=0, axis=1)
            self.Nin_mf.append(0)
        elif(type=='out'):

            self.varName.insert(self.Ninputs+self.Noutputs, name)
            self.varRange.insert(self.Ninputs+self.Noutputs, range)
            self.Noutputs += 1
            self.RuleList = np.insert(self.RuleList, self.Ninputs+self.Noutputs - 1, values=0, axis=1)
            self.Nout_mf.append(0)
        else:
             print('error')


    def delvar(self, var_type, idx):
        """
        Delete variable from fism structure

        :param var_type: "in" or "out" type variable
        :param idx: No of variable
        :type var_type: string
        :type idx: Int
        """

        if (var_type == 'in'):
            print('delete input')
            self.varName.pop(idx-1)
            self.varRange.pop(idx-1)
            self.RuleList = np.delete(self.RuleList, idx - 1, axis=1)
            self.Ninputs -= 1

        elif (var_type == 'out'):
            print('delete output')
            self.varName.pop(self.Ninputs+idx -1)
            self.varRange.pop(self.Ninputs+idx -1)
        else:
            print('error')

#    def editvar(self, type, idx):
#        # TODO implement this method
#        print(' sdd rule/rules to the fis')


    def addmf(self,var_type,var_index,namemf,typemf,parammf ):
        """
        Add membership function (mf) to fuzzy structure

        :param var_type:  "in" or "out" type variable
        :param var_index: Number of added mf
        :param namemf:    name of membership function
        :param typemf:    type of mf: 'trimf','trapmf','gaussmf','gauss2mf','gbellmf','sigmf','singleton'
        :param parammf:   [param 1, param2, param 3, param 4]
        :type var_type:   string
        :type var_index:  int
        :type namemf:     string
        :type typemf:     string
        :type parammf:    string

        """
        if var_type =="in":                         #  #  TODO add names and add in_mfcsum to fis structure
            self.Nin_mf[var_index-1]+=1
            
            in_mfcsum= [0] * (self.Ninputs+1)
            for i in range(1,self.Ninputs+1):
                in_mfcsum[i]=in_mfcsum[i-1]+self.Nin_mf[i-1]
                
            idx=in_mfcsum[var_index]-1  
            
            if idx==0:
                param =np.insert(parammf, 0, values=mftypes.index(typemf), axis=0)
                self.mfpari[0:]=param
                self.mfnames_in[0]=namemf
            else:
                param =np.insert(parammf, 0, values=mftypes.index(typemf), axis=0)
                self.mfpari = np.insert(self.mfpari, idx, values=param, axis=0)
                self.mfnames_in=np.insert(self.mfnames_in, idx, values=namemf, axis=0)
            
        elif var_type =="out":                              #  #  TODO add names and add in_mfcsum to fis structure
            self.Nout_mf [var_index-1]+=1
        
            out_mfcsum= [0] * (self.Noutputs+1)
            for i in range(1,self.Noutputs+1):
                out_mfcsum[i]=out_mfcsum[i-1]+self.Nout_mf[i-1] 

            idx=out_mfcsum[var_index]-1 

            if idx==0:
                if self.type=='mamdani':
                    param =np.insert(parammf, 0, values=mftypes.index(typemf), axis=0)
                    self.mfparo[0:] = param
                else:
                    param = np.insert(parammf, -1, values=0, axis=0)
                    self.mfparo[0:]=param
                    self.mfnames_out = np.insert(self.mfnames_out, idx, values=namemf, axis=0)

                self.mfnames_out[0]=namemf

            else:
                if self.type == 'mamdani':
                    param =np.insert(parammf, 0, values=mftypes.index(typemf), axis=0)
                    self.mfparo = np.insert(self.mfparo, idx, values=param, axis=0)
                else:
                    param = np.insert(parammf, -1, values=0, axis=0)
                    self.mfparo = np.insert(self.mfparo, idx, values=param, axis=0)

                self.mfnames_out=np.insert(self.mfnames_out, idx, values=namemf, axis=0)


    def delmf(self, var_type,var_index,mf_index):
        """
        Delete membership function from fuzzy system

        :param var_type:  variable type: input("in") or output("out")
        :param var_index: No. of variable
        :param mf_index:  No. of mf
        :type type:      string
        :type var_index: Int
        :type mf_index:  Int

        """
        if var_type =="in":                         
                   
            in_mfcsum= [0] * (self.Ninputs+1)
            
            for i in range(1,self.Ninputs+1):
                in_mfcsum[i]=in_mfcsum[i-1]+self.Nin_mf[i-1]
                
            idx=in_mfcsum[var_index-1]+mf_index-1
            
            if idx==0 & in_mfcsum[-1]==1 :
                
               self.mfpari=np.zeros(1,5) 
               self.mfnames_in[0]='none'
               self.Nin_mf[0]=0  
               
            else:
               self.mfpari=np.delete(self.mfpari, (idx), axis=0)
               self.mfnames_int=np.delete(self.mfnames_in,idx, axis=0)
               self.Nin_mf[var_index-1]-=1
            
        elif var_type =="out":

            out_mfcsum= [0] * (self.Noutputs+1)
            
            for i in range(1,self.Noutputs+1):
                out_mfcsum[i]=out_mfcsum[i-1]+self.Nout_mf[i-1]

            idx = out_mfcsum[var_index - 1] + mf_index - 1

            if idx==0 & out_mfcsum[-1]==1 :
                
               self.mfparo=np.zeros(1,5)   
               self.mfnames_out[0]='none'
               self.Nout_mf[0]=0  
            else:
               self.mfparo=np.delete(self.mfparo, (idx), axis=0)     
               self.mfnames_out=np.delete(self.mfnames_out,idx, axis=0) 
               self.Nout_mf[var_index-1]-=1
        

    def setmf(self, var_type,var_index,mf_index,typemf,parammf):
        """
        Set new parameters for members ship function (mf) for input/output

        :param var_type:  variable type: input("in") or output("out")
        :param var_index: index of variable
        :param mf_idx:    No of mf function
        :param typemf:    type of mf
        :param parammf:   list [1x4] of mf parameters
        :type var_type:  string
        :type var_index: Int
        :type mf_idx:    Int
        :type typemf:    string
        :type parammf:   list of doubles

        """
        if var_type =="in":
            in_mfcsum= [0] * (self.Ninputs+1)
            
            for i in range(1,self.Ninputs+1):
                in_mfcsum[i]=in_mfcsum[i-1]+self.Nin_mf[i-1]

            idx = in_mfcsum[var_index - 1] + mf_index - 1
            param = np.insert(parammf, 0, values=mftypes.index(typemf), axis=0)
            self.mfpari[idx:]=param


        elif var_type =="out":  
            out_mfcsum= [0] * (self.Noutputs+1)
            
            for i in range(1,self.Noutputs+1):
                out_mfcsum[i]=out_mfcsum[i-1]+self.Nout_mf[i-1]

            idx = out_mfcsum[var_index - 1] + mf_index - 1
            param = np.insert(parammf, 0, values=mftypes.index(typemf), axis=0)
            self.mfparo[idx:] = param
        
        print('edit mf ')

    def getmf(self, var_type,var_index):
        """
        Return list of membership function of input or output

        :param var_type:  variable type: 'in' or 'out'
        :param var_index: index of variable 1...
        :type var_type:   string
        :type var_index:  Int
        :return:  mf list ie mf_list[i]=[name_i,type, params], i=0..Nmf-1
        """
        Nmf= self.Nin_mf[var_index-1] if var_type == "in" else self.Nout_mf[var_index-1]
        mf_list = [0] *Nmf
        print(self.Ninputs)
        if var_type =="in":

            in_mfcsum= [0] * (self.Ninputs+1)
            for i in range(1,self.Ninputs+1):
                in_mfcsum[i]=in_mfcsum[i-1]+self.Nin_mf[i-1]
            print(in_mfcsum)
            idx=in_mfcsum[var_index-1]
            for i in range(0,Nmf):
                mf_list[i]=[self.mfnames_in[idx+i],mftypes[int(self.mfpari[idx+i][0])],self.mfpari[idx+i][0:-1]]

     
        else:
            for i in range(0,Nmf):
                mf_list[i]=[self.mfnames_out[i],mftypes[int(self.mfparo[i][0])],self.mfpari[i][0:-1]]

        return mf_list

    def addrule(self, rule,weight):
        """ Add rule to fuzzy structure.

        :param rule:   rule
        :param weight: weighting parameter
        :type rule:     list of Int
        :type weight:   double
        """
        rule=np.array(rule).astype(int)
        rows=rule.ndim 
        cols=rule.shape[-1]  
        
        if self.NRules ==0:
           self.RuleList=np.array([rule])
           self.RuleWeights=np.array([weight])
           self.NRules=rows
        else:   
           self.RuleList =np.vstack((self.RuleList,np.array(rule).astype(int)))
           self.RuleWeights=np.hstack((self.RuleWeights,np.array(weight)))
           self.NRules+=1

    def delrule(self, ruleNo):
        """
        Delete rule from fuzzy structure

        :param ruleNo: Rule's number
        :type ruleNo: Int

        """
        print('delete rule')
        if self.NRules > 0 & ruleNo<=self.NRules :
            self.NRules=self.NRules-1
            self.RuleList=np.delete(self.RuleList, (ruleNo-1), axis=0)
            self.RuleWeights = np.delete(self.RuleWeights, (ruleNo-1), axis=0)

if __name__ == '__main__':
    print('fuzzy functions system')