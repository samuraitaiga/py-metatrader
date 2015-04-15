# coding: utf-8
'''
Created on 2015/02/20

@author: samuraitaiga
'''
version = '0.0.1'

from distutils.core import setup

setup(name='metatrader',
      version=version,
      description="MetaTrader4 Libraries easily backtest and optimization from python",
#       long_description=open('README.rst').read() + '\n\n' + open('CHANGES.rst').read(),
      classifiers=[
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: Microsoft :: Windows',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Software Development :: Libraries',
      ],
      keywords='MetaTrader mt4 mql',
      author='samuraitaiga',
      author_email='samuraitaiga@gmail.com',
#       url='http://urllib3.readthedocs.org/',
      license='MIT',
      packages=['metatrader',
                ],
      install_requires=['beautifulsoup4'],
#       tests_require=[
          # These are a less-specific subset of dev-requirements.txt, for the
          # convenience of distro package maintainers.
#           'nose',
#       ],
#       test_suite='test',
      )