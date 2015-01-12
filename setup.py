#!/usr/bin/env python
from setuptools import setup
# from setuptools import find_packages
# find_packages

# under windows, run
# python.exe setup.py bdist --format msi
# to create a windows installer

version_short = '0.1'
version_long = '0.1.0'

if __name__ == '__main__':
    setup(name='allconf',
          version=version_long,
          description='XML configuration management',
          author='Maximilian Weigand',
          author_email='mweigand@geo.uni-bonn.de',
          url='http://www.geo.uni-bonn.de/~mweigand',
          package_dir={'': 'lib'},
          packages=['allconf', ],
          scripts=['scripts/ac_update_xml.py'],
          install_requires=['numpy', ]
          )
