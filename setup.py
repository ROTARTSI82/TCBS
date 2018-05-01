#!venv/bin python
# -*- coding: UTF-8 -*-

"""
(.../TCBS/setup.py)

Installs Totally Customizable Battle Simulator
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='Totally Customizable Battle Simulator',
    version='a21.18.04.29',
    packages=['venv.lib.python2.7.distutils', 'venv.lib.python2.7.encodings', 'venv.lib.python2.7.site-packages.pip',
              'venv.lib.python2.7.site-packages.pip._vendor', 'venv.lib.python2.7.site-packages.pip._vendor.idna',
              'venv.lib.python2.7.site-packages.pip._vendor.pytoml',
              'venv.lib.python2.7.site-packages.pip._vendor.certifi',
              'venv.lib.python2.7.site-packages.pip._vendor.chardet',
              'venv.lib.python2.7.site-packages.pip._vendor.chardet.cli',
              'venv.lib.python2.7.site-packages.pip._vendor.distlib',
              'venv.lib.python2.7.site-packages.pip._vendor.distlib._backport',
              'venv.lib.python2.7.site-packages.pip._vendor.msgpack',
              'venv.lib.python2.7.site-packages.pip._vendor.urllib3',
              'venv.lib.python2.7.site-packages.pip._vendor.urllib3.util',
              'venv.lib.python2.7.site-packages.pip._vendor.urllib3.contrib',
              'venv.lib.python2.7.site-packages.pip._vendor.urllib3.contrib._securetransport',
              'venv.lib.python2.7.site-packages.pip._vendor.urllib3.packages',
              'venv.lib.python2.7.site-packages.pip._vendor.urllib3.packages.backports',
              'venv.lib.python2.7.site-packages.pip._vendor.urllib3.packages.ssl_match_hostname',
              'venv.lib.python2.7.site-packages.pip._vendor.colorama',
              'venv.lib.python2.7.site-packages.pip._vendor.html5lib',
              'venv.lib.python2.7.site-packages.pip._vendor.html5lib._trie',
              'venv.lib.python2.7.site-packages.pip._vendor.html5lib.filters',
              'venv.lib.python2.7.site-packages.pip._vendor.html5lib.treewalkers',
              'venv.lib.python2.7.site-packages.pip._vendor.html5lib.treeadapters',
              'venv.lib.python2.7.site-packages.pip._vendor.html5lib.treebuilders',
              'venv.lib.python2.7.site-packages.pip._vendor.lockfile',
              'venv.lib.python2.7.site-packages.pip._vendor.progress',
              'venv.lib.python2.7.site-packages.pip._vendor.requests',
              'venv.lib.python2.7.site-packages.pip._vendor.packaging',
              'venv.lib.python2.7.site-packages.pip._vendor.cachecontrol',
              'venv.lib.python2.7.site-packages.pip._vendor.cachecontrol.caches',
              'venv.lib.python2.7.site-packages.pip._vendor.webencodings',
              'venv.lib.python2.7.site-packages.pip._vendor.pkg_resources',
              'venv.lib.python2.7.site-packages.pip._internal', 'venv.lib.python2.7.site-packages.pip._internal.req',
              'venv.lib.python2.7.site-packages.pip._internal.vcs',
              'venv.lib.python2.7.site-packages.pip._internal.utils',
              'venv.lib.python2.7.site-packages.pip._internal.models',
              'venv.lib.python2.7.site-packages.pip._internal.commands',
              'venv.lib.python2.7.site-packages.pip._internal.operations', 'venv.lib.python2.7.site-packages.wheel',
              'venv.lib.python2.7.site-packages.wheel.tool', 'venv.lib.python2.7.site-packages.wheel.signatures',
              'venv.lib.python2.7.site-packages.pygame', 'venv.lib.python2.7.site-packages.pygame.docs',
              'venv.lib.python2.7.site-packages.pygame.gp2x', 'venv.lib.python2.7.site-packages.pygame.tests',
              'venv.lib.python2.7.site-packages.pygame.tests.test_utils',
              'venv.lib.python2.7.site-packages.pygame.tests.run_tests__tests',
              'venv.lib.python2.7.site-packages.pygame.tests.run_tests__tests.all_ok',
              'venv.lib.python2.7.site-packages.pygame.tests.run_tests__tests.exclude',
              'venv.lib.python2.7.site-packages.pygame.tests.run_tests__tests.timeout',
              'venv.lib.python2.7.site-packages.pygame.tests.run_tests__tests.failures1',
              'venv.lib.python2.7.site-packages.pygame.tests.run_tests__tests.everything',
              'venv.lib.python2.7.site-packages.pygame.tests.run_tests__tests.incomplete',
              'venv.lib.python2.7.site-packages.pygame.tests.run_tests__tests.print_stderr',
              'venv.lib.python2.7.site-packages.pygame.tests.run_tests__tests.print_stdout',
              'venv.lib.python2.7.site-packages.pygame.tests.run_tests__tests.infinite_loop',
              'venv.lib.python2.7.site-packages.pygame.tests.run_tests__tests.incomplete_todo',
              'venv.lib.python2.7.site-packages.pygame.threads', 'venv.lib.python2.7.site-packages.pygame.examples',
              'venv.lib.python2.7.site-packages.altgraph', 'venv.lib.python2.7.site-packages.macholib',
              'venv.lib.python2.7.site-packages.PodSixNet', 'venv.lib.python2.7.site-packages.setuptools',
              'venv.lib.python2.7.site-packages.setuptools.extern',
              'venv.lib.python2.7.site-packages.setuptools._vendor',
              'venv.lib.python2.7.site-packages.setuptools._vendor.packaging',
              'venv.lib.python2.7.site-packages.setuptools.command', 'venv.lib.python2.7.site-packages.modulegraph',
              'venv.lib.python2.7.site-packages.pkg_resources', 'venv.lib.python2.7.site-packages.pkg_resources.extern',
              'venv.lib.python2.7.site-packages.pkg_resources._vendor',
              'venv.lib.python2.7.site-packages.pkg_resources._vendor.packaging',
              'venv.lib.python2.7.site-packages.PodSixNetPython3'],
    url='https://github.com/ROTARTSI82/TCBS',
    license='Apache License 2.0',
    author='Grant Yang',
    author_email='rotartsi0482@gmail.com',
    description='A python video game inspired by TABS. See README.md'
)
