from mockito_test.test_base import *
from mockito import *
from mockito.invocation import InvocationError

class Dog(object):
    def waggle(self):
        return "Wuff!"
    
    def bark(self, sound):
        return "%s!" % sound
    
    def do_default_bark(self):
        return self.bark('Wau')
    
class InstanceMethodsTest(TestBase):
    def tearDown(self):
        unstub()

    def testUnstubAnInstanceMethod(self):
        original_method = Dog.waggle
        when(Dog).waggle().thenReturn('Nope!')
        
        unstub()

        rex = Dog()
        self.assertEqual('Wuff!', rex.waggle())
        self.assertEqual(original_method, Dog.waggle)
        
    def testStubAnInstanceMethod(self):
        when(Dog).waggle().thenReturn('Boing!')

        rex = Dog()
        self.assertEqual('Boing!', rex.waggle())
        
    def testStubsAnInstanceMethodWithAnArgument(self):
        when(Dog).bark('Miau').thenReturn('Wuff')
        
        rex = Dog()
        self.assertEqual('Wuff', rex.bark('Miau'))
        #self.assertEquals('Wuff', rex.bark('Wuff'))
        
    def testInvocateAStubbedMethodFromAnotherMethod(self):
        when(Dog).bark('Wau').thenReturn('Wuff')
        
        rex = Dog()
        self.assertEqual('Wuff', rex.do_default_bark())
        verify(Dog).bark('Wau')
        
    def testYouCantStubAnUnknownMethodInStrictMode(self):
        try:
            when(Dog).barks('Wau').thenReturn('Wuff')
            self.fail('Stubbing an unknown method should have thrown a exception')
        except InvocationError:
            pass
        
    def testCallingAStubbedMethodWithUnexpectedArgumentsShouldReturnNone(self):
        when(Dog).bark('Miau').thenReturn('Wuff')        
        rex = Dog()
        self.assertEqual(None, rex.bark('Shhh'))
        
        
    def testStubInstancesInsteadOfClasses(self):
        rex = Dog()
        when(rex).bark('Miau').thenReturn('Wuff')
        
        self.assertEqual('Wuff', rex.bark('Miau'))
        verify(rex, times=1).bark(any())

        max = Dog()
        self.assertEqual('Miau!', max.bark('Miau'))
        
        
if __name__ == '__main__':
    unittest.main()
