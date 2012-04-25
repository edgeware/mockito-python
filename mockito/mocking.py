#!/usr/bin/env python
# coding: utf-8

import inspect
import invocation
from mock_registry import mock_registry
from types import FunctionType, MethodType
import warnings

try:
  from zope import interface as zi
except ImportError:
  zi = None

__copyright__ = "Copyright 2008-2010, Mockito Contributors"
__license__ = "MIT"
__maintainer__ = "Mockito Maintainers"
__email__ = "mockito-python@googlegroups.com"

__all__ = ['mock', 'Mock']


class StubbingError(Exception): pass

class _Dummy(object): pass

class TestDouble(object): pass

CO_VARARGS = 4
CO_VARKEYWORDS = 8

def fromFunction(func, imlevel=0):
  """Return signature of function."""
  # Copyright (c) 2001, 2002 Zope Foundation and Contributors.
  # All Rights Reserved.
  signature = {}
  defaults = func.func_defaults or ()
  code = func.func_code
  # Number of positional arguments
  na = code.co_argcount-imlevel
  names = code.co_varnames[imlevel:]
  opt = {}
  # Number of required arguments
  nr = na-len(defaults)
  if nr < 0:
    defaults=defaults[-nr:]
    nr = 0

  # Determine the optional arguments.
  opt.update(dict(zip(names[nr:], defaults)))

  signature['positional'] = names[:na]
  signature['required'] = names[:nr]
  signature['optional'] = opt

  argno = na

  # Determine the function's variable argument's name (i.e. *args)
  if code.co_flags & CO_VARARGS:
    signature['varargs'] = names[argno]
    argno = argno + 1
  else:
    signature['varargs'] = None

  # Determine the function's keyword argument's name (i.e. **kw)
  if code.co_flags & CO_VARKEYWORDS:
    signature['kwargs'] = names[argno]
  else:
    signature['kwargs'] = None

  return signature

def fromMethod(meth):
  # Copyright (c) 2001, 2002 Zope Foundation and Contributors.
  # All Rights Reserved.
  func = meth.im_func
  return fromFunction(func, imlevel=1)

import inspect

class mock(TestDouble):
  def __init__(self, mocked_obj=None, strict=True, chainable=False):
    self.invocations = []
    self.stubbed_invocations = []
    self.original_methods = []
    self.stubbing = None
    self.verification = None
    if mocked_obj is None:
        mocked_obj = _Dummy()
        strict = False
    self.mocked_obj = mocked_obj
    self.strict = strict
    self.stubbing_real_object = False
    if zi is not None:
      self.zi = isinstance(mocked_obj, zi.interface.InterfaceClass)
    else:
      self.zi = False
    self.chainable = chainable

    mock_registry.register(self)
  
  def __getattr__(self, method_name):
    if self.stubbing is not None:
      return invocation.StubbedInvocation(self, method_name)
    
    if self.verification is not None:
      return invocation.VerifiableInvocation(self, method_name)
      
    return invocation.RememberedInvocation(self, method_name)
  
  def remember(self, invocation):
    if self.strict:
      self.__verify_method_stub(invocation)

    self.invocations.insert(0, invocation)

  def __verify_method_signature(self, invocation, sig, name):
    #meth = self.mocked_obj[invocation.method_name]
    #sig = meth.getSignatureInfo()
    if len(sig['required']) > len(invocation.params):
      raise StubbingError(
        "%s takes %d required args, but stubbed with %d" % (
          name,
          len(sig['required']),
          len(invocation.params)))
    if len(sig['positional']) < len(invocation.params):
      if not sig['varargs']:
        raise StubbingError(
          "%s takes %d positional args, but stubbed with %d" % (
            name,
            len(sig['positional']),
            len(invocation.params)))
    for name in invocation.named_params:
      if not name in sig['optional'] and not sig['kwargs']:
        raise StubbingError(
          "invocation with unknown kwargs %s" % (
            name,))

  def __verify_method_stub(self, invocation):
    if self.zi:
      meth = self.mocked_obj.get(invocation.method_name)
      self.__verify_method_signature(invocation, meth.getSignatureInfo(),
          '%s.%s' % (self.mocked_obj.__name__, invocation.method_name))
    elif inspect.isclass(self.mocked_obj):
      meth = self.get_method(invocation.method_name)
      if isinstance(meth, FunctionType):
        signature = fromFunction(meth, imlevel=1)
        self.__verify_method_signature(invocation, signature,
           '%s.%s' % (self.mocked_obj.__name__, invocation.method_name))
      elif meth is None:
        if self.strict:
          raise StubbingError("invocation of missing method %s" % (
              invocation.method_name))
    else:
      meth = self.get_method(invocation.method_name)
      if meth is None:
        # Work around that for instances __dict__ may not be in place.
        meth = getattr(self.mocked_obj, invocation.method_name, None)
      if isinstance(meth, FunctionType):
        signature = fromFunction(meth)
        self.__verify_method_signature(invocation, signature,
                                       meth.__name__)
      elif isinstance(meth, MethodType):
        signature = fromMethod(meth)
        self.__verify_method_signature(invocation, signature,
                                       meth.__name__)

  def finish_stubbing(self, stubbed_invocation):
    if self.strict:
      self.__verify_method_stub(stubbed_invocation)
    self.stubbed_invocations.insert(0, stubbed_invocation)
    self.stubbing = None
    
  def expect_stubbing(self):
    self.stubbing = True
    
  def pull_verification(self):
    v = self.verification
    self.verification = None
    return v

  def has_method(self, method_name):
    if self.zi:
      def search(c):
        if method_name in c.names():
          return True
        else:
          for base in c.__bases__:
            if search(base):
              return True
        return False
      return search(self.mocked_obj)
    return hasattr(self.mocked_obj, method_name)
    
  def get_method(self, method_name):
    return self.mocked_obj.__dict__.get(method_name)

  def set_method(self, method_name, new_method):
    setattr(self.mocked_obj, method_name, new_method)
    
  def replace_method(self, method_name, original_method):
    
    def new_mocked_method(*args, **kwargs): 
      # we throw away the first argument, if it's either self or cls  
      if inspect.isclass(self.mocked_obj) and not isinstance(original_method, staticmethod): 
          args = args[1:]
      call = self.__getattr__(method_name) # that is: invocation.RememberedInvocation(self, method_name)
      return call(*args, **kwargs)
      
    if isinstance(original_method, staticmethod):
      new_mocked_method = staticmethod(new_mocked_method)  
    elif isinstance(original_method, classmethod): 
      new_mocked_method = classmethod(new_mocked_method)  
    
    self.set_method(method_name, new_mocked_method)
    
  def stub(self, method_name):
    original_method = self.get_method(method_name)
    original = (method_name, original_method)
    self.original_methods.append(original)

    # If we're trying to stub real object(not a generated mock), then we should patch object to use our mock method.
    # TODO: Polymorphism was invented long time ago. Refactor this.
    if self.stubbing_real_object:
      self.replace_method(method_name, original_method)

  def unstub(self):  
    while self.original_methods:  
      method_name, original_method = self.original_methods.pop()      
      self.set_method(method_name, original_method)
       
def Mock(*args, **kwargs):
  '''A ``mock``() alias.
  
  Alias for compatibility. To be removed in version 1.0.
  '''
  warnings.warn("\n`Mock()` is deprecated, please use `mock()` (lower 'm') instead.", DeprecationWarning)
  return mock(*args, **kwargs)
