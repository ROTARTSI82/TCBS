#!venv/bin python
# -*- coding: UTF-8 -*-

"""
A
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='Totally Customizable Battle Simulator',
      version='a21.18.04.26',
      description='A python video game inspired by TABS. See README.md',
      url='https://github.com/ROTARTSI82/TCBS',
      author='Grant Yang',
      author_email='grantthewarhero@gmail.com',
      license='Apache License 2.0',
      packages=['', ],
      install_requires=[
          "pygame",
          "PodSixNet"
      ],
      zip_safe=False)
