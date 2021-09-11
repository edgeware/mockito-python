from mockito_test.test_base import *
from mockito import *

class Dog:
  @classmethod
  def bark(cls):
    return "woof!"
  
class Cat:
  @classmethod
  def meow(cls, m):
    return cls.__name__ + " " + str(m)

class Lion(object):
  @classmethod
  def roar(cls):
    return "Rrrrr!"

class ClassMethodsTest(TestBase):   

  def tearDown(self):
    unstub() 

  def testUnstubs(self):     
    when(Dog).bark().thenReturn("miau!")
    unstub()
    self.assertEqual("woof!", Dog.bark())
  
  #TODO decent test case please :) without testing irrelevant implementation details
  def testUnstubShouldPreserveMethodType(self):
    when(Dog).bark().thenReturn("miau!")
    unstub()
    self.assertTrue(isinstance(Dog.__dict__.get("bark"), classmethod))     
  
  def testStubs(self):     
    self.assertEqual("woof!", Dog.bark())
    
    when(Dog).bark().thenReturn("miau!")
    
    self.assertEqual("miau!", Dog.bark())
    
  def testStubsClassesDerivedFromTheObjectClass(self):
    self.assertEqual("Rrrrr!", Lion.roar())
    
    when(Lion).roar().thenReturn("miau!")    
    
    self.assertEqual("miau!", Lion.roar())
    
  def testVerifiesMultipleCallsOnClassmethod(self):     
    when(Dog).bark().thenReturn("miau!")

    Dog.bark()
    Dog.bark()
    
    verify(Dog, times(2)).bark()
    
  def testFailsVerificationOfMultipleCallsOnClassmethod(self):
    when(Dog).bark().thenReturn("miau!")

    Dog.bark()
    
    self.assertRaises(VerificationError, verify(Dog, times(2)).bark)

  def testStubsAndVerifiesClassmethod(self):
    when(Dog).bark().thenReturn("miau!")
    
    self.assertEqual("miau!", Dog.bark())
    
    verify(Dog).bark()
    
  def testPreservesClassArgumentAfterUnstub(self):
    self.assertEqual("Cat foo", Cat.meow("foo"))

    when(Cat).meow("foo").thenReturn("bar")
    
    self.assertEqual("bar", Cat.meow("foo"))
    
    unstub()
    
    self.assertEqual("Cat foo", Cat.meow("foo"))
    
if __name__ == '__main__':
  unittest.main()

