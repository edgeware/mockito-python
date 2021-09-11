from setuptools import setup

setup(name='mockito-edgeware',
      version='0.5.2',
      packages=['mockito', 'mockito_test', 'mockito_util'],
      url='https://github.com/edgeware/mockito-python',
      download_url='http://pypi.edgeware.tv/simple/mockito',
      maintainer='Mockito Maintainers',
      maintainer_email='mockito-python@googlegroups.com',
      license='MIT',
      description='Spying framework',
      long_description=('Mockito is a spying framework based on Java library'
                        'with the same name.'),
      install_requires=['six'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Topic :: Software Development :: Testing',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3'
      ])
