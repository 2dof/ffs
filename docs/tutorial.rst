Tutorial
========

.. contents:: Table of Contents
.. section-numbering::




--------------------------------
Exmaple1: Mamdani Fuzzy System 
--------------------------------

Lets create mamdaani fuzzy system with 2 inputs and 1 output and default settings:
OR methog: 'max' , AND method: 'min'
Implication method:  'min'  (minimum)
Aggregation Method:  'max'  (maxsimum)   
Defuzzyfication Method: 'centroid' (center of gravity)

Imputs and outputs name and ranges:  input 1 named 'x1' and varianle range from 0 to 2.0
                                     input 2 named 'x3' and varianle range from 0 to 2.0 
                                     output  named 'y1' and varianle range from 0 to 2.0
.. code-block:: python

      fis1=fism('mamdani')
       
      # add inputs and outputs to fizzy
      fis1.addvar('in','x1',[0.,2.0])
      fis1.addvar('in','x2',[0.,2.0])
      fis1.addvar('out','y1',[0.,2.0])


For each inputs and otput we add 3 mfs trangular membership functions: 

.. code-block:: python

      fis1.addmf('in',1,'A1','trimf',[-1,0,1,0])
      fis1.addmf('in',1,'A2','trimf',[0,1,2,0])
      fis1.addmf('in',1,'A3','trimf',[1,2,3,0])
      
      fis1.addmf('in',2,'B1','trimf',[-1,0,1,0])
      fis1.addmf('in',2,'B2','trimf',[0,1,2,0])
      fis1.addmf('in',2,'B3','trimf',[1,2,3,0])
      
      fis1.addmf('out',1,'C1','trimf',[-1,0,1,0])
      fis1.addmf('out',1,'C2','trimf',[0,1,2,0])
      fis1.addmf('out',1,'C3','trimf',[1,2,3,0])

Lets plot membership functions of fis1 system.   
First lets import dedicated plot functuon from plot_fis class then
plot mfs:

.. code-block:: python

      from plot_fis import plot_mfs  
      
      figure(1)
      subplot(221);  cla()
      plot_mfs(fis1,'in',1)  
      subplot(222);  cla()
      plot_mfs(fis1,'in',2)      
      subplot(212);  cla()      
      plot_mfs(fis1,'out',1)  


.. figure:: images/mf_plot_mamdani.png
   :width: 800
   :align: center
   :alt:  mfs plot  

**Adding Rules**

Rule are added as coded list of integers of length (N_inpust+ Noutputs +1]
 
for example:
Rule: If x1 is A1 AND x2 B2 then output is  C3  
| coded Rule : R=[1,  2, 3, 1]

| R[0]=1 means first  (A1) mf of input x1
| R[1]=2 means second (B2) mf of input x2
| R[2]=3 means third (C3) mf of  output 1
| R[3]=1 means AND operator,  for OR oerator will be 0 

examples: 
| if x1 is A2, thed output is C1  -> [a, 0, 1, 1]  , zero means there is no x2 in rule 
| if x2 is A1 OR x2 is B1 then output is C2  -> [1, 1, 2, 0]  

Lets add Rules to our fuzzy system 

.. code-block:: python

      R1=[1,1,1,1]            # Rule 1:  if x1 is A1 and x2 is B1 then y is C1   
      R2=[2,2,2,1]            # Rule 2:  if x1 is A2 and x2 is B2 then y is C2  
      R3=[3,3,3,1]            # Rule 3:  if x1 is A3 and x2 is B3 then y is C3  
      
      fis1.addrule(R1,1.0)        # add rules to the fis1 , weighting parameter  = 1.0
      fis1.addrule(R2,1.0)
      fis1.addrule(R3,1.0)



**Evaluate fuzzy system**

.. code-block:: python

      x1 = 0.5 
      x2 = 0.5
      y1 = evaluate(fis1,[x1, x2])
      print(f'fuzzy input:[{x1}, {x2}] output = {y1}')

-------------------------------------------
Exmaple2: TSK Fuzzy System (in preparation) 
-------------------------------------------

<in preparation>