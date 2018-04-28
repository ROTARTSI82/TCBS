#!venv/bin/env python
# -*- coding: UTF-8 -*-

"""
(.../TCBS/__main__.py)
------------------------------------------------------------------------
TOTALLY CUSTOMIZABLE BATTLE SIMULATOR a21.18.04.14
------------------------------------------------------------------------
By Grant Yang

Totally Customizable Battle Simulator is a multiplayer 
strategy videogame. You can design and program your 
own soldiers and make them fight against your
friend's soldiers. It is inspired by Totally Accurate
Battle Simulator by Landfall and uses Pygame 1.9 and
Python 2.7. TCBS uses PodSixNet written by chr15m (Chris McCormick).

SEE README.md FOR MORE DETAILS
"""
import os
import sys

__appName__ = "Totally Customizable Battle Simulator"
__version__ = "a21.18.04.15"
__author__ = "Grant Yang"

def executefile(filepath, globalsdict=globals(), localsdict=locals()):
    """
    Since Python3 doesn't have execfile, we use this instead

    :type filepath: str
    :type globalsdict: dict
    :type localsdict: dict
    :rtype: None
    """
    with open(filepath, "r") as fp:
        code = compile(fp.read(), filepath, 'exec')
        exec (code, globalsdict, localsdict)


executefile("CONFIG.py")
try:
    executefile("venv/bin/activate_this.py", dict(__file__=os.getcwd()+"venv/bin/activate_this.py"))
    sys.path.append(os.getcwd()+"/venv/lib/python2.7/site-packages")
except IOError:
    sys.path.append(os.getcwd()+"/resources/packages")

# TODO
# Add translations for "CLEAR"
#
#

try:
    executefile("resources/scripts/load.py")
    executefile("resources/scripts/mainloop.py")
except Exception as e:
    executefile("resources/scripts/handleCrash.py")
