#!venv/bin python
# -*- coding: UTF-8 -*-

"""
(.../TCBS/CONFIG.py)
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

__appName__ = "Totally Customizable Battle Simulator"
__version__ = "a21.18.04.14"
__author__ = "Grant Yang"

import os
import pygame
from pygame.locals import *

# Starting Budget in Multiplayer
startBdgt = 10000  # How many coins you start with
# Coin Regeneration Rate in Multiplayer
coinRR = 100  # How many coins you get for every second after the battle starts
# What your name is in Multiplayer
try:
    nickname = os.getlogin()
except Exception as e:
    nickname = "PLAYER"
# Key Repeat Rate = (Delay Before Repeat, Repeat Interval)
keyRR = (650, 100)
# Arguments passed to pygame.display.set_mode
# See https://www.pygame.org/docs/ref/display.html#pygame.display.set_mode
# AND https://www.pygame.org/docs/ref/display.html#pygame.display.list_modes
screenArgs = ([640, 480], RESIZABLE)
# A float between 0.0 and 1.0
musicVol = 0.5  # The volume of the music
effectsVol = 0.5  # The volume of sound effects
# If __debugMode__ is enabled, TCBS will print logs,
# show FPS, show cursor-tracking sprite, and not send crash reports
__debugMode__ = True
# Controls. See https://www.pygame.org/docs/ref/key.html
screenshotKey = K_F1
copyKey = K_F2
pasteKey = K_F3
endBattleKey = K_ESCAPE
# What language file to load and in what font
langFont = "resources/fonts/Quivira.ttf"
langList = [u"resources/lang/deutsche.json", u"resources/lang/english.json",
            u"resources/lang/español.json", u"resources/lang/français.json",
            u"resources/lang/javanese.json", u"resources/lang/português.json",
            u"resources/lang/tiếng_việt.json", u"resources/lang/türk.json",
            u"resources/lang/русский.json"]
langFile = langList[1]
# Fontsizes are multiplied by GUI Scale in case you want to change the fontsize
GUIScale = 0.6875
