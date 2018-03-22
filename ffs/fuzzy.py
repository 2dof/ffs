#!/usr/bin/env python3
# -----------------------------------------------------------------------
# fuzzy.py
# -----------------Copyrights and license ------------------------------------------------------

# This file is part of ffs (fuzzy functional system)
# Copyright (C) @2018@ Lukasz Szydlowski
# mailto:lukas.sz@wp.pl
#
#This program is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, version 3 or any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program.
# If not, see http://www.gnu.org/licenses/
# ----------------------------------------------------------------------------------------------
#import math
#import fractions
import numpy as np
from mfs import mftypes

__version__ = "1.0.0"

class fism:
    """ Fuzzy data structure. fism store konfiguration and settings of fuzzy system.
    """
    
    # Constructor
    def __init__(self, type ='mamdani', Ninputs =0 ,Noutputs = 0):
        """Initialize fuzzy data structure for fuzzy system.

        :param type:
        :param Ninputs:
        :param Noutputs:
        """
        self.type = type                    # type = mamdani , sugeno
        self.Ninputs    = Ninputs              # (int)
        self.Noutputs = Noutputs            # (int)
        self.varName = []                   # list of variablee names
        self.varRange = []                  # list of variables range
        self.ORmethod = 'max'               # OR method
        self.ANDmethod = 'min'              # AND method
        self.Implmethod = 'min'             # Implication method
        self.Aggmethod = 'max'              # Aggregation Method:
        self.Defuzzymethod = 'centroid'     # or 'mom', 'som', 'lom', 'bisector'

        self.Nin_mf = [0]*self.Ninputs
        self.Nout_mf = [0] * self.Noutputs

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

        self.NRules =0
        self.RuleList =(np.zeros((1,Ninputs +Noutputs+1))).astype(int)
        self.RuleWeights=[1.0]*self.NRules

        # add row to ther end
        #insert(a, len(a), np.zeros((1, 4)), axis=0)

    def addvar(self,type,name,range):
        """Add wariable ( input or output) to the fuzzy system
        :param type: 'in' or 'out'
        :type type: string
        :param name:
        :type name: string
        :param range:
        :type tange: [double,double]
        :returns: None
        
        
        .. warning:: text
        .. note:: blabla
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
        """Delete variable from fis system
        :param var_type:    "in" or "out" type variable
        :param idx:     No of variable     
        :type var_type:     string
        :type idx:      Int

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
        """Add membership function to fuzzy structute
        :param var_type:      input("in") or output("out")
        :param var_index: Number od added mf
        :param namemf:    name of membership function
        :param typemf:    type of mf: 'trimf','trapmf','gaussmf','gauss2mf','gbellmf','sigmf','singleton'
        :param parammf:   [param 1, param2, param 3, param 4]
        :type var_type:   string
        :type var_index:  int
        :type namemf:     string
        :type typemf:     string
        :type parammf:    string
        :return: None
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
        """ Delete membership function from fuzzy system
        :param type:
        :param var_index:
        :param mf_index):
        :type type:      string
        :type var_index: Int
        :type mf_index:  Idx
        :return:
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
            
        elif var_type =="out":                               #  TODO add names and add in_mfcsum to fis structure


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
        """Set new parameters for members ship function for input/output
        :param var_type:  variable type: 'in' or 'out'
        :param var_index: index of variable
        :param mf_idx:    No of mf function
        :param typemf:    type of mf
        :param parammf:   list [1x4] of mf parameters
        :type var_type:  string
        :type var_index: Int
        :type mf_idx:    Int
        :type typemf:    string
        :type parammf:   list of doubles
        :return: None
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
        """ Return list of mf function of varianle
        :param var_type:  variable type: 'in' or 'out'
        :param var_index: index of variable
        :type var_type:   string
        :type var_index:  Int
        :return:  mf list
        """
        # TODO implement this method

    def addrule(self, rule,weight):
        """ Add rule to fuzzy structure.
        :param rule:  rule list
        :param weight: double
        :type rule     list od Int
        :type weight   double
        :return: None
        """
        rule=np.array(rule).astype(int)
        rows=rule.ndim 
        cols=rule.shape[-1]  
        
        if self.NRules ==0:
           self.RuleList=rule
           self.RuleWeights=np.array(weight)
           self.NRules=rows
        else:   
           self.RuleList =np.vstack((self.RuleList,np.array(rule).astype(int)))
           self.RuleWeights=np.hstack((self.RuleWeights,np.array(weight)))
           self.NRules+=1



    def delrule(self, ruleNo):
        """Delete rule from fuzzy structure
        :param ruleNo: No of rule
        :type ruleNo: Int
        :return:
        """
        print('delete rule')
        if self.NRules > 0 & ruleNo<=self.NRules :
            self.NRules=self.NRules-1
            self.RuleList=np.delete(self.RuleList, (ruleNo-1), axis=0)
            self.RuleWeights = np.delete(self.RuleWeights, (ruleNo-1), axis=0)

if __name__ == '__main__':
    print('fuzzy functions system')