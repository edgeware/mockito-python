from mockito_test.test_base import *
from mockito import * 
from mockito.invocation import InvocationError
import os

class ModuleFunctionsTest(TestBase):
  def tearDown(self):
    unstub() 

  def testUnstubs(self):     
    when(os.path).exists("test").thenReturn(True)
    unstub()
    self.assertEqual(False, os.path.exists("test"))
      
  def testStubs(self):
    when(os.path).exists("test").thenReturn(True)
    
    self.assertEqual(True, os.path.exists("test"))

  def testStubsConsecutiveCalls(self):     
    when(os.path).exists("test").thenReturn(False).thenReturn(True)
    
    self.assertEqual(False, os.path.exists("test"))
    self.assertEqual(True, os.path.exists("test"))

  def testStubsMultipleClasses(self):
    when(os.path).exists("test").thenReturn(True)
    when(os.path).dirname(any(str)).thenReturn("mocked")

    self.assertEqual(True, os.path.exists("test"))
    self.assertEqual("mocked", os.path.dirname("whoah!"))     

  def testVerifiesSuccesfully(self):     
    when(os.path).exists("test").thenReturn(True)
    
    os.path.exists("test")
    
    verify(os.path).exists("test")
    
  def testFailsVerification(self):
    when(os.path).exists("test").thenReturn(True)

    self.assertRaises(VerificationError, verify(os.path).exists, "test")

  def testFailsOnNumberOfCalls(self):
    when(os.path).exists("test").thenReturn(True)

    os.path.exists("test")
    
    self.assertRaises(VerificationError, verify(os.path, times(2)).exists, "test")

  def testStubsTwiceAndUnstubs(self):
    when(os.path).exists("test").thenReturn(False)
    when(os.path).exists("test").thenReturn(True)
    
    self.assertEqual(True, os.path.exists("test"))
    
    unstub()
    
    self.assertEqual(False, os.path.exists("test"))
    
  def testStubsTwiceWithDifferentArguments(self):
    when(os.path).exists("Foo").thenReturn(False)
    when(os.path).exists("Bar").thenReturn(True)
    
    self.assertEqual(False, os.path.exists("Foo"))
    self.assertEqual(True, os.path.exists("Bar"))
    
  def testShouldThrowIfWeStubAFunctionNotDefinedInTheModule(self):  
    self.assertRaises(InvocationError, lambda:when(os).walk_the_line().thenReturn(None))  
      

if __name__ == '__main__':
  unittest.main()
