Tutorial
========

Exmaple1: Mamdani Fuzzy System 
------------------------------
<introdution>


.. code-block:: python

      fis1=fism('mamdani')
       
      # add inputs and outputs to fizzy
      fis1.addvar('in','x1',[0.,2.0])
      fis1.addvar('in','x2',[0.,2.0])
      fis1.addvar('out','y1',[0.,2.0])


<desctiption, addingg membership functions>

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


<desctiption, insert plots of ms >

.. figure:: images/mf_plot.png
   :width: 400
   :align: center
   :alt: mf plot  


Adding rules

.. code-block:: python

      R1=[1,1,1,1]     
      R2=[2,2,2,1]
      R3=[3,3,3,1]
      
      fis1.addrule(R1,1.)
      fis1.addrule(R2,1.)
      fis1.addrule(R3,1.)