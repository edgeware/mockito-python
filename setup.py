import sys

from setuptools import setup

extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True

setup(name='mockito-edgeware',
      version='0.5.1',
      packages=['mockito', 'mockito_test', 'mockito_util'],
      url='https://github.com/edgeware/mockito-python',
      download_url='http://pypi.edgeware.tv/simple/mockito',
      maintainer='Mockito Maintainers',
      maintainer_email='mockito-python@googlegroups.com',
      license='MIT',
      description='Spying framework',
      long_description=('Mockito is a spying framework based on Java library'
                        'with the same name.'),
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Topic :: Software Development :: Testing',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3'
      ],
      test_suite='nose.collector',
      py_modules=['distribute_setup'],
      setup_requires=['nose'],
      **extra)
