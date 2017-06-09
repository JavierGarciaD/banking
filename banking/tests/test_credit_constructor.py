'''
Created on 8/06/2017

@author: spectre
'''
#import unittest
from credit.constructor import *
import pytest
# 
# class Test_Prueba(unittest.TestCase):
#     def test_my_function(self):
#         assert Prueba(2, 1).my_function() == 3
# if __name__ == "__main__":
#     # import sys;sys.argv = ['', 'Test.testName']
#     unittest.main()


def test_my_function():
    assert Prueba(2, 1).my_function() == 3



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    pytest.main()
    test_my_function()