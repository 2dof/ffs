
#from __future__ import absolute_import
import sys, os


import numpy as np
from mfs import *
from fuzzy_sets import *
from fuzzy import *
import unittest

class TestMFS(unittest.TestCase):
    def setUp(self):
        pass

    def test_trimf(self):
        param=[-1,0,1]
        self.assertEqual(trimf(-1, param), 0)
        self.assertEqual(trimf(-0.5, param), 0.5)
        self.assertEqual(trimf(0, param), 1)
        self.assertEqual(trimf(1, param), 0)

    def test_trapmf(self):
        param = [-1, 0, 1, 2]
        self.assertEqual(trapmf(-1, param), 0.)
        self.assertEqual(trapmf(-0.5, param), 0.5)
        self.assertEqual(trapmf(0.5, param), 1)
        self.assertEqual(trapmf(1.5, param), 0.5)
        self.assertEqual(trapmf(2, param), 0.)

    def test_gaussmf(self):
        param = [1, 0]
        value=gaussmf(-0.5, param)
        self.assertEqual(gaussmf(0,param),1)

    def test_gauss2mf(self):
        param = [1, 0, 2,2]
        self.assertAlmostEqual(gauss2mf(-0.5, param), 0.88249, places=3)
        self.assertEqual(gauss2mf(0, param), 1)
        self.assertEqual(gauss2mf(1, param), 1)
        self.assertEqual(gauss2mf(2, param), 1)
        value = gauss2mf(2.5, param)
        self.assertAlmostEqual(gauss2mf(2.5, param), 0.9692, places=3)

    def test_gbellmf(self):
        param = [2, 4, 6]
        self.assertEqual(gbellmf(4, param), 0.5)
        self.assertEqual(gbellmf(6, param),1)
        self.assertEqual(gbellmf(8, param), 0.5)

    def test_sigmf(self):
        param = [1, 3]
        val=sigmf(10, param)
        self.assertEqual(sigmf(3, param),0.5)
        self.assertAlmostEqual(sigmf(10, param), 0.999, places=3)

    def test_singleton(self):
        param = [1]
        #val=singleton(1, param)
        self.assertEqual(singletonmf(0.99, param),0)
        self.assertEqual(singletonmf(1, param), 1)
        self.assertEqual(singletonmf(1.1, param),0)

    def test_singleton(self):

        #mftypes = ['trimf', 'trapmf', 'gaussmf', 'gauss2mf', 'gbellmf', 'sigmf', 'singleton']
        params=[mftypes.index('trimf')]+[-1, 0, 1]
        self.assertEqual(eval_mf(-1,params), 0)

        params = [mftypes.index('trapmf')] + [-1, 0, 1, 2]
        self.assertEqual(eval_mf(-1, params), 0)


class TestFUZZY_SETS(unittest.TestCase):
    def setUp(self):
        pass

    def test_tnorm(self):
        print("test t-nomr method")
        self.assertEqual(tnorm(1,2,'min'),1)
        self.assertEqual(tnorm(1,2,'prod'),2)
        self.assertEqual(tnorm(1,2,'eprod'), 2)

    def test_snom(self):
        print("test s-nomr method")
        self.assertEqual(snorm(1,2,'max'),2)
        self.assertEqual(snorm(1,2,'prod'),1)
        self.assertEqual(snorm(1,2,'eprod'), 1)

    def test_complement(self):
        #print("test complement method")
        self.assertEqual(complement(0.3, 'one'), 0.7)
        self.assertEqual(complement(0.3, 'sugeno'), 0.7)

    def test_defuzzy(self):
       # print("test defuzzyfucation method")
        y=[0, 0.5, 1, 1, 0.5, 0]

        x1 = defuzzy(y, 'centroid')
        x2 = defuzzy(y, 'mom')
        x3 = defuzzy(y, 'som')
        x4 = defuzzy(y, 'lom')
        x5 = defuzzy(y, 'bisector')
        #print([x1,x2,x3,x4,x5])
        self.assertEqual(x1,2.5)
        self.assertEqual(x2,2.5)
        self.assertEqual(x3,2)
        self.assertEqual(x4,3)

class TestFUZZY(unittest.TestCase):


    def setUp(self):
        fis1 = fism()
        fis1.addvar('in', 'x1', [0., 3.0])
        fis1.addvar('in', 'x2', [0., 3.0])
        fis1.addvar('out', 'y1', [0., 3.0])

        fis1.addmf('in', 1, 'A1', 'trimf', [-1, 0, 1, 0])
        fis1.addmf('in', 1, 'A2', 'trimf', [0, 1, 2, 0])
        fis1.addmf('in', 1, 'A3', 'trimf', [1, 2, 3, 0])

        fis1.addmf('in', 2, 'B1', 'trimf', [-1, 0, 1, 0])
        fis1.addmf('in', 2, 'B2', 'trimf', [0, 1, 2, 0])
        fis1.addmf('in', 2, 'B3', 'trimf', [1, 2, 3, 0])

        fis1.addmf('out', 1, 'C1', 'trimf', [-1, 0, 1, 0])
        fis1.addmf('out', 1, 'C2', 'trimf', [0, 1, 2, 0])
        fis1.addmf('out', 1, 'C3', 'trimf', [1, 2, 3, 0])
        self.fis1=fis1
        pass

    def test_addvar(self):

        self.assertEqual(self.fis1.Ninputs,2)
        self.assertEqual(self.fis1.Noutputs, 1)


if __name__ == '__main__':
    print('test run')
    unittest.main()

#python -m unittest test_fuzzy.py