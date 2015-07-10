from mockito_test.test_base import *
from mockito import mock, when, verify, times, any, StubbingError

class Class:

  def abc(a, b, c):
    pass


class StrictStubbingTest(TestBase):

  def testCallWithMissingArguments(self):
      theMock = mock(Class)
      try:
        theMock.abc('a')
      except StubbingError:
        pass
      else:
        self.assertFalse(True, "error not raised")

  def testCallMissingFunction(self):
      theMock = mock(Class)
      try:
        theMock.who()
      except StubbingError:
        pass
      else:
        self.assertFalse(True, "error not raised")

if __name__ == '__main__':
  unittest.main()
