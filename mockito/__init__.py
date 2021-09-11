#!/usr/bin/env python
# coding: utf-8

'''Mockito is a Test Spy framework.'''

from __future__ import absolute_import

__copyright__ = "Copyright 2008-2010, Mockito Contributors"
__license__ = "MIT"
__maintainer__ = "Mockito Maintainers"
__email__ = "mockito-python@googlegroups.com"

from mockito.mockito import mock, verify, verifyNoMoreInteractions, verifyZeroInteractions, when, unstub, ArgumentError
from mockito import inorder
from mockito.spying import spy
from mockito.verification import VerificationError

# Imports for compatibility
from mockito.mocking import Mock, StubbingError
from mockito.matchers import any, contains, times # use package import (``from mockito.matchers import any, contains``) instead of ``from mockito import any, contains``
from mockito.verification import never

__all__ = ['mock', 'spy', 'verify', 'verifyNoMoreInteractions', 'verifyZeroInteractions', 'inorder', 'when', 'unstub', 'VerificationError', 'ArgumentError',
           'Mock', # deprecated
           'any', # compatibility
           'contains', # compatibility
           'never', # compatibility
           'times' # deprecated
           ]
