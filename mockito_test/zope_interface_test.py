from mockito_test.test_base import *
from mockito import mock, when, verify, times, any, StubbingError

try:
  from zope import interface as zi
except ImportError:
  zi = None

if zi is not None:
  class ITest(zi.Interface):
    def simple(a, b, c):
      pass
    def simple_with_names_params(a, b, c, d=None):
      pass

  class ISuper(ITest):
    def complex(d):
      pass

  class IWithGet(zi.Interface):
    def get(a):
      pass
    def names():
      pass

  class ZopeInterfaceStubbingTest(TestBase):
    def testWithConflictingNames(self):
      theMock = mock(IWithGet)
      when(theMock).get('d').thenReturn(0)
      when(theMock).names().thenReturn(0)

    def testTooFewRequiredArguments(self):
      theMock = mock(ITest)
      try:
        when(theMock).simple('d', 'e').thenReturn(0)
      except StubbingError:
        pass
      else:
        self.assertFalse(True, "error not raised")

    def testTooManyRequiredArguments(self):
      theMock = mock(ITest)
      try:
        when(theMock).simple('d', 'e', 'f', 'g').thenReturn(0)
      except StubbingError:
        pass
      else:
        self.assertFalse(True, "error not raised")

    def testNamedParam(self):
      theMock = mock(ITest)
      when(theMock).simple_with_names_params('d', 'e', any(), d=1).thenReturn(0)

    def testBadNamedParam(self):
      theMock = mock(ITest)
      try:
        when(theMock).simple_with_names_params('d', 'e', 'f', d=1, e=1).thenReturn(0)
      except StubbingError:
        pass
      else:
        self.assertFalse(True, "error not raised")

    def testInheritedInterface(self):
      theMock = mock(ISuper)
      when(theMock).simple('a', 'b', 'c').thenReturn(0)
      when(theMock).complex('d').thenReturn(0)


if __name__ == '__main__':
  unittest.main()
