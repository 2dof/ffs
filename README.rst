Fuzzy Functional System
=======================
Functional Fuzzy System (ffs) is intended to be a very simple library for modeling fuzzy system for
Mamdani and Sugeno inference.

.. note::
I use this simple library for R&D fuzzy control and process simulation based on Python.
I'm used to working with fuzzy tolboxes from Matlab and Scilab(sciFLT) so i tried to keep similar convention.

API docs: https://2dof.github.io/ffs/ 

Project Summary
===============

Actual status
----------------
:Version: 1.0.0 dev1
:Status:    developing

Done:
+++++
* Implemented basic fuzzy inference engine and fuzzy class structure for only 'AND' or 'OR' logic in user-defined rules
* TSK for linear inference 

To Do:
++++++
* Docs, Examples
* Add siplified Fuzzy models ( Rule Table Arrays, Lookup Tables) for Fuzzy Control modeling and simulation 
* Add self organizing, adataptaion mechanisms 
* Implementet supprot for 'AND' and 'OR' logic user defined rules, and linguistic Rules definition
* GUI for building fuzzy inference systems and viewing and analyzing result
* Code optimization and refractoring (port to Cython)
* support for normalized parameters and values (integer based computation)
