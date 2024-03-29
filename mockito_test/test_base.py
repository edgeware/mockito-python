#!/usr/bin/env python
# coding: utf-8

import unittest

class TestBase(unittest.TestCase):
  
  def __init__(self, *args, **kwargs):
    unittest.TestCase.__init__(self, *args, **kwargs)
    
  def assertRaisesMessage(self, message, callable, *params):
    try:
      if (params):
        callable(params)
      else:
        callable()        
      self.fail('Exception with message "%s" expected, but never raised' % (message))
    except Exception as e:
      # TODO: self.fail() raises AssertionError which is caught here and error message becomes hardly understadable 
      self.assertEqual(message, str(e))    

main = unittest.main
