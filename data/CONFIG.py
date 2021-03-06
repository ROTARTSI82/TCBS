#!venv/bin python
# -*- coding: UTF-8 -*-

"""
(.../TCBS/data/CONFIG.py)

"""

from pygame.locals import *

# Key Repeat Rate = (Delay Before Repeat, Repeat Interval)
keyRR = (650, 100)
# Arguments passed to pygame.display.set_mode
# See https://www.pygame.org/docs/ref/display.html#pygame.display.set_mode
# AND https://www.pygame.org/docs/ref/display.html#pygame.display.list_modes
screenArgs = ([800, 600], RESIZABLE)
origRes = (1200, 900)
# If __debugMode__ is enabled, TCBS will print logs,
# show FPS, show cursor-tracking sprite, show ping times, etc
__debugMode__ = True
# Controls. See https://www.pygame.org/docs/ref/key.html
screenshotKey = K_F1
copyKey = K_F2
pasteKey = K_F3
endBattleKey = K_ESCAPE
clearRedKey = K_r
clearBlueKey = K_b
toggleTeamKey = K_t
nextUnitKey = K_e
prevUnitKey = K_q
startKey = K_SPACE
# Background colors in the RGB format.
# RGBA, CMY, HSVA, HSLA, and I1I2I3 are not supported.
sky_blue = (160, 210, 255)
grass_green = (155, 205, 50)
# Change rates and clamp ranges of certain options.
optionAttr = {
    "srtBdgt": {
        "cr": 50,
        "max": float("inf"),
        "min": 0},
    "coinRR": {
        "cr": 50,
        "max": float("inf"),
        "min": float("-inf")},
    "fps": {
        "cr": 15,
        "max": float("inf"),
        "min": 0},
    "music": {
        "cr": 0.0625,
        "max": 1,
        "min": 0},
    "effects": {
        "cr": 0.0625,
        "max": 1,
        "min": 0},
    "scale": {
        "cr": 0.0625,
        "max": float("inf"),
        "min": 0}
}
# Antialias text.
antialias = True
# Button customization
hoverOP = "{} * 1.125"
