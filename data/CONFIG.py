#!venv/bin python
# -*- coding: UTF-8 -*-

"""
(.../TCBS/CONFIG.py)

"""

__appName__ = "Totally Customizable Battle Simulator"
__version__ = "a21.18.04.15"
__author__ = "Grant Yang"

from pygame.locals import *

# Key Repeat Rate = (Delay Before Repeat, Repeat Interval)
keyRR = (650, 100)
# Arguments passed to pygame.display.set_mode
# See https://www.pygame.org/docs/ref/display.html#pygame.display.set_mode
# AND https://www.pygame.org/docs/ref/display.html#pygame.display.list_modes
screenArgs = ([800, 600], RESIZABLE)
# If __debugMode__ is enabled, TCBS will print logs,
# show FPS, show cursor-tracking sprite, show ping times, etc
__debugMode__ = False
# Controls. See https://www.pygame.org/docs/ref/key.html
screenshotKey = K_F1
copyKey = K_F2
pasteKey = K_F3
endBattleKey = K_ESCAPE
