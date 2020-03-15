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


def mapRuleTable(Table,mfout_name):
    
    """mfout_name=['NB','NM','NS','ZE','PS','PM','PB']
    
    Table=[['NB','NS','PS','PB','PB','PB','PB'],
               ['NB','NM','ZE','PM','PM','PB','PB'],
               ['NB','NM','NS','PS','PM','PB','PB'],
               ['NB','NM','NS','ZE','PS','PM','PB'],
               ['NB','NB','NM','NS','PS','PM','PB'],
               ['NB','NB','NM','NM','ZE','PM','PB'],
               ['NB','NB','NB','NB','NS','PM','PB']]
     
     
     RuleTable=mapRuleTable(Table,mfout_name)
     """          
                
    nr,nc=np.array(Table).shape 
    
    RuleTable=np.zeros((nr,nc)).astype(int)
    l=0
    for k in range(0,len(mfout_name)):
        
        for i in range(0,nr):
            for j in range(0,nc):
                if Table[i][j]==mfout_name[k]:
                    RuleTable[i][j]=k+1
                    l+=1
    return RuleTable 
              

class fuzzyPID:
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
#    **type**            string           ='mamdani' or 'tsk' : type of fuzzy system
    **Ninputs**         Int              Number of inputs
    **Noutputs**        Int              Number of outputs
    **varName**         string           list, store of variable names
    **varRange**        [float,float]    store of variable physical range
#    **ORmethod**        string           default:'max' other: 'prod' 'eprod
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
#    **Npts**            Int              No of points resolution for defuzzyfication proces
    =================   ==============   ========================================================


    """
    def __init__(self, RuleTable =(np.zeros(0)).astype(int),):
        """
        Initialize fuzzy data structure for fuzzy system
        """
        self.type = 'mamdani'                    # 'mamdani' or 'tsk'
#        self.ORmethod = 'max'               # OR method Snorms: 'max', 'prod' 'eprod'
#        self.ANDmethod = 'min'              # AND method Tnorms: ,'min' 
#        self.Implmethod = 'min'             # Implication method: tnorm eprod
#        self.Aggmethod = 'max'              # Aggregation Method:'sum','eprod' , 'prod'
#        self.Defuzzymethod = 'centroid'     # or 'mom', 'som', 'lom', 'bisector'    
        
        self.gi=[1]*2
        self.go=1
        self.RuleTable =RuleTable
        if RuleTable.ndim>1:
            nr,nc=self.RuleTable.shape  
        else:
            nr,nc=1,0
        
        #self.RuleList =(np.zeros(nr*nc)).astype(int)
        self.NRules = nr*nc

        #self.RuleWeights=[1.0]*self.NRules
        self.Ninputs  = 0                  # (int)
        self.Noutputs = 0                  # (int)
        self.varName  = []  # list of variablee names
        self.varRange = []  # list of variables range
        self.Nin_mf  = [0] * self.Ninputs
        self.Nout_mf = [0] * self.Noutputs

        self.in_mfcsum = [0]
        self.out_mfcsum =[0]

        if self.Ninputs > 0:
            for i in range(self.Ninputs):
                self.addvar('in', 'in'+str(i+1),[0,100])
        if self.Noutputs > 0:
            for i in range(self.Noutputs):
                self.addvar('out', 'out' + str(i + 1), [0, 100])

        self.mfnames_in  = ['A1']
        self.mfnames_out = ['y1']

        self.mfpari = np.zeros((1, 5))  # [type,param1,param2,param3,param3

        #if self.type =='mamdani':
        self.mfparo=np.zeros((1,5)) #[type,param1,param2,param3,param3
        #elif self.type =='tsk':
        #    if self.Ninputs<=5:
        #        self.mfparo = np.zeros((1, 5))  # [type,param1,param2,param3,param3
        #    else:
        #        self.mfparo = np.zeros((1, self.Ninputs))  # [type,param1,param2,param3,param3

        #self.Npts =100
        
    def addvar(self,type,name,range):
        """
        Add wariable (input or output) to the fuzzy system

        :param type: 'in' or 'out'
        :type type: string
        :param name: name od variable
        :type name: string
        :param range: [min,max] ragne value of variable
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
            #self.RuleList = np.insert(self.RuleList, self.Ninputs-1, values=0, axis=1)
            self.Nin_mf.append(0)
        elif(type=='out'):

            self.varName.insert(self.Ninputs+self.Noutputs, name)
            self.varRange.insert(self.Ninputs+self.Noutputs, range)
            self.Noutputs += 1
            #self.RuleList = np.insert(self.RuleList, self.Ninputs+self.Noutputs - 1, values=0, axis=1)
            self.Nout_mf.append(0)
        else:
             print('error')
             
    def addmf(self,var_type,var_index,namemf,typemf,parammf ):
        """
        Add membership function to fuzzy structute

        :param var_type:  "in" or "out" type variable
        :param var_index: Number od added mf
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
            
            self.in_mfcsum= [0] * (self.Ninputs+1)
            for i in range(1,self.Ninputs+1):
                self.in_mfcsum[i]=self.in_mfcsum[i-1]+self.Nin_mf[i-1]
                
            idx=self.in_mfcsum[var_index]-1
            
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
        
            self.out_mfcsum= [0] * (self.Noutputs+1)
            for i in range(1,self.Noutputs+1):
                self.out_mfcsum[i]=self.out_mfcsum[i-1]+self.Nout_mf[i-1]

            idx=self.out_mfcsum[var_index]-1

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

    def delmf(self, var_type, var_index, mf_index):
        """
        Delete membership function from fuzzy system

        :param var_type:  variable type: input("in") or output("out")
        :param var_index: No. of variable
        :param mf_index:  No. of mf
        :type type:      string
        :type var_index: Int
        :type mf_index:  Int

        """
        if var_type == "in":

            idx = self.in_mfcsum[var_index - 1] + mf_index - 1

            if idx == 0 & self.in_mfcsum[-1] == 1:

                self.mfpari = np.zeros(1, 5)
                self.mfnames_in[0] = 'none'
                self.Nin_mf[0] = 0

            else:
                self.mfpari = np.delete(self.mfpari, (idx), axis=0)
                self.mfnames_int = np.delete(self.mfnames_in, idx, axis=0)
                self.Nin_mf[var_index - 1] -= 1

        elif var_type == "out":

            idx = self.out_mfcsum[var_index - 1] + mf_index - 1

            if idx == 0 & self.out_mfcsum[-1] == 1:

                self.mfparo = np.zeros(1, 5)
                self.mfnames_out[0] = 'none'
                self.Nout_mf[0] = 0
            else:
                self.mfparo = np.delete(self.mfparo, (idx), axis=0)
                self.mfnames_out = np.delete(self.mfnames_out, idx, axis=0)
                self.Nout_mf[var_index - 1] -= 1

    def addruleTable(self, RuleTable,mfout_name=[],var_range=[],setmf=False):
        """ Add rule to fuzzy structure.

        :param rule:   rule
        :param weight: weightinh param
        :type rule:     list od Int
        :type weight:   double
        """
#        Rulelist = np.zeros(Nin_mf[0] * Nin_mf[1] * Nin_mf[2] * Nin_mf[3]).astype(int)
#
#        for j in range(0, Nin_mf[1]):  # y columns
#            for i in range(0, Nin_mf[0]):  # x rows
#               idx = i + j * Nin_mf[0]
#               if Ninputs >= 3:
#                    idx += Nin_mf[0] * Nin_mf[1]
#                if Ninputs == 4:
#                    idx += Nin_mf[0] * Nin_mf[1] * Nin_mf[2]
#
#                Rulelist[idx] = RuleTable[i, j]
#                print([idx, RuleTable[i, j]])

        
        nr,nc=0,0
        self.RuleTable =np.array(RuleTable).astype(int)
        if RuleTable.ndim>1:
            nr,nc=self.RuleTable.shape
        else:
            nr,nc=1,0

        self.NRules=nr*nc
        
        
        if len(var_range)==3:
            
           addvar(self,'in','x1',mfrange[0])
           addvar(self,'in','x2',mfrange[1])
           addvar(self,'out','y1',mfrange[2])
           
           

    def evaluate(self,x):
        # evaluate
        valbuf=np.zeros(2*self.Ninputs)       
        idxbuf=np.zeros(2*self.Ninputs).astype(int)   

        for n in range(0, self.Ninputs):
            for inp in range(0,Nin_mf[n]):
                idx = inp + self.in_mfcsum[n]
                
                val = eval_mf(x[n],self.mfpari[idx][:])
                print([n,inp,val])
                
                if val > 0:
                    idxbuf[n] = inp
                    valbuf[n] = val
                     
                    if inp<Nin_mf[n]:
                       val = eval_mf(x[n],self.mfpari[idx+1][:])
                       print([n,inp+1,val])
                       valbuf[n+self.Ninputs]=val
                       idxbuf[n+self.Ninputs]=inp+1
                     
                    break
    
        idx =[0]*self.Ninputs
        minV=[0]*(2**self.Ninputs)
        mfidx=[0]*(2**self.Ninputs)
        Ruleidx=[0]*(2**self.Ninputs)
        for mask in range(0,2**self.Ninputs):
            minval=1.0          
            for j in range(0,self.Ninputs):                
                if (mask &(1<<j)) >0: #check_bit(mask,j):
                    minval=min(minval,valbuf[j+self.Ninputs]) 
                    idx[j] = idxbuf[j+self.Ninputs]
                else:
                    minval=min(minval,valbuf[j]) 
                    idx[j] = idxbuf[j]
            
            Ruleidx[mask]=idx[0]+idx[1]*self.Nin_mf[1]
            
            minV[mask]=minval
            mfidx[mask]=self.RuleTable[idx[0],idx[1]]-1
          #  print([mask,'idx ',Ruleidx[mask],self.RuleList[Ruleidx[mask]]],[idx[0],idx[1]], self.RuleTable[idx[0],idx[1]])
            
            
        sum_a=0.0
        sum_c=0.0
        for i in range(0,2**self.Ninputs):
            mfparo=self.mfparo[mfidx[i]][1:4] 
            h=minV[i]
            xc=(mfparo[0]+mfparo[1]+mfparo[2])/3.
            area=(mfparo[2]-mfparo[0])*h/2.
            sum_a+=area 
            sum_c+=(area*xc)  
            
        out= sum_c/sum_a

        return out



#def check_bit(val,pos):
#
#    return (val &(1<<pos)) >0

if __name__ == "__main__":


#    RuleTable=[[5,5,5,4,3],
#               [5,5,4,3,2],
#               [5,4,3,2,1],
#               [4,3,2,1,1],
#               [3,2,1,1,1]]
#==========================================
    from fuzzy import *
    from mfs import eval_mf
    fis1 = fuzzyPID()
    
    fis1.addvar('in','x1',[0.,3.0])
    fis1.addvar('in','x2',[0.,3.0])
    fis1.addvar('out','y1',[0.,3.0])        
    fis1.addmf('in',1,'A1','trimf',[-1,0,1,0])
    fis1.addmf('in',1,'A2','trimf',[0,1,2,0])
    fis1.addmf('in',1,'A3','trimf',[1,2,3,0])    
    fis1.addmf('in',2,'B1','trimf',[-1,0,1,0])
    fis1.addmf('in',2,'B2','trimf',[0,1,2,0])
    fis1.addmf('in',2,'B3','trimf',[1,2,3,0]) 

    fis1.addmf('out',1,'C1','trimf',[-1,0,1,0])
    fis1.addmf('out',1,'C2','trimf',[0,1,2,0])
    fis1.addmf('out',1,'C3','trimf',[1,2,3,0]) 
    
    Ninputs=2
    Nin_mf=[3,3]
    
    RuleTable=[[3,3,2],
               [3,2,1],
               [2,1,1]]
               
    RuleTable=np.array(RuleTable).astype(int)
    fis1.addruleTable(RuleTable)
    
    x=[1.5,0.5]
    y=fis1.evaluate(x)
    
    print(y)
#    
#    mfout_name=['NB','NM','NS','ZE','PS','PM','PB']
#    
#    Table=[['NB','NS','PS','PB','PB','PB','PB'],
#              ['NB','NM','ZE','PM','PM','PB','PB'],
#              ['NB','NM','NS','PS','PM','PB','PB'],
#              ['NB','NM','NS','ZE','PS','PM','PB'],
#              ['NB','NB','NM','NS','PS','PM','PB'],
#              ['NB','NB','NM','NM','ZE','PM','PB'],
#              ['NB','NB','NB','NB','NS','PM','PB']]
#
#    var_range=[[0,3],[0,3],[0,3]]                
#        
#    RuleTable=mapRuleTable(Table,mfout_name)   
#    nr,nc=RuleTable.shape
#    range_mf=var_range[0]
#    
#    drange=(range_mf[1]-range_mf[0])/float(nr-1)
#    
#    mf_param=np.array([range_mf[0]-drange,range_mf[0],range_mf[0]+drange])    
#    
#    for i in range(0,nr):
#        mf_params=mf_param+i*drange
#        print(mf_params)


