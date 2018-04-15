#!venv/bin/env python
# -*- coding: UTF-8 -*-

"""
(.../TCBS/__main__.py)
------------------------------------------------------------------------
TOTALLY CUSTOMIZABLE BATTLE SIMULATOR i21.18.03.31
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
executefile("venv/bin/activate_this.py", dict(__file__=os.getcwd()+"venv/bin/activate_this.py"))
sys.path.append(os.getcwd()+"/venv/lib/python2.7/site-packages")

__appName__ = "Totally Customizable Battle Simulator"
__version__ = "a21.18.04.14"
__author__ = "Grant Yang"

# TODO
#
#
#

try:
    executefile("resources/scripts/load.py")
    executefile("resources/scripts/mainloop.py")
except Exception as e:
    executefile("resources/scripts/handleCrash.py")
