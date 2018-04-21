#!venv/bin python
# -*- coding: UTF-8 -*-

"""
(.../TCBS/resources/scripts/load.py)
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

import datetime
import json
import os
import platform
import sys

start = datetime.datetime.now()

__appName__ = "Totally Customizable Battle Simulator"
__version__ = "a21.18.04.15"
__author__ = "Grant Yang"

# TODO
#
#
#

if False:
    # Ignore this code. It makes PyCharm happy
    # Since I call this script via execfile, PyCharm thinks
    # all the variables are undefined and gives me endless warnings :(
    from __main__ import *
    from CONFIG import *
    from funcsAndClasses import *
    from multiplayer import *

try:
    import pygame
    from pygame.locals import *
except ImportError as e:
    print("pygame not installed. Trying to install and upgrade pygame...")
    import subprocess
    try:
        subprocess.call(["pip", "install", "pygame"])
    except Exception as e:
        print("Cannot install pygame: "+str(e))
    try:
        subprocess.call(["pip", "install", "upgrade", "pygame"])
    except Exception as e:
        print("Cannot upgrade pygame: "+str(e))
    print("Finished! Please try again.")
    sys.exit(0)

majorPyVer = sys.version_info.major
if majorPyVer not in [2, 3]:
    print("Bad python version!")
    print("Expected Python 2 or Python 3")
    print("Got Python "+str(majorPyVer))
    sys.exit("Bad python version!")

psnSuccess = False
if majorPyVer == 2:
    try:
        from PodSixNet.Server import Server
        from PodSixNet.Channel import Channel
        from PodSixNet.Connection import connection, ConnectionListener
        psnSuccess = True
    except Exception as e:
        psnSuccess = False
elif majorPyVer == 3:
    try:
        from PodSixNetPython3.Server import Server
        from PodSixNetPython3.Channel import Channel
        from PodSixNetPython3.Connection import connection, ConnectionListener
        psnSuccess = True
    except Exception as e:
        psnSuccess = False

pygame.init()
screen = pygame.display.set_mode(*screenArgs)
caption = "{} {}".format(__appName__, __version__)
pygame.display.set_caption(caption, caption)
try:
    pygame.display.set_icon(pygame.image.load("resources/icon.png"))
except Exception:
    pass
pygame.key.set_repeat(*keyRR)
pygame.time.set_timer(USEREVENT + 1, 1000)

clock = pygame.time.Clock()
buttons = pygame.sprite.Group()

screen.fill([255, 255, 255])
simpleFont = pygame.font.Font(None, 50)
screen.blit(simpleFont.render("Loading...", False, [255, 0, 0]),
            [screen.get_width()/2-50, screen.get_height()/2-50])
pygame.display.flip()

running = True
state = "menu"
red = 255
green = 255
blue = 255
alreadyHandled = []
serverStr = ""
validChars = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
shiftChars = '~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'
shiftDown = False

if not os.path.exists("logs"):
    os.mkdir("logs")
now = datetime.datetime.now()
with open("logs/"+str(now.date())+".log", 'a') as logfile:
    msg = "====================[{}]====================\n".format(now.ctime())
    logfile.write(msg)
    if __debugMode__:
        print(msg.strip("\n"))

executefile("resources/scripts/funcsAndClasses.py")
if psnSuccess:  # EXPIREMENTAL
    executefile("resources/scripts/multiplayer.py")

try:
    with open(langFile, "r") as fp:
        langDict = json.load(fp)
except Exception as e:
    langDict = {}
    log("EXCEPTION", "Cannot load language: "+str(e))

log("START", "Starting...")
log("DEBUG", "__debugMode__ == "+str(__debugMode__))
pythonver = str(sys.version_info.major)+"."+str(sys.version_info.minor)
pygamever = str(pygame.vernum[0])+"."+str(pygame.vernum[1])
log("VERSIONS", "Got Python {} and Pygame {}".format(pythonver, pygamever))
log("VERSIONS", "Expected Python 2.7 and Pygame 1.9")
badVerDetect = False
badVerWarn = TxtOrBt(["Bad Version Detected!", False, [0, 0, 0], [255, 0, 0]], [None, 35])
badVerWarn.rect.topleft = [10, 10]
if pygamever != "1.9" or pythonver != "2.7":
    log("WARNING", "Bad python/pygame version detected!")
    badVerDetect = True
jsonUrl = "https://sites.google.com/site/rotartsiofficial/python-games/tcbs/TCBSinf.json"
newUpDetect = False
newUpNote = TxtOrBt(["New Update Detected!", False, [0, 0, 0], [0, 255, 0]], [None, 35])
newUpNote.rect.topleft = [10, 40]

try:
    if majorPyVer == 2:
        import urllib2
        jsonSite = urllib2.urlopen(jsonUrl)
        jsonObj = json.load(jsonSite)
    elif majorPyVer == 3:
        import urllib.request
        jsonSite = urllib.request.urlopen(jsonUrl)
        decoder = json.JSONDecoder()
        contents = str(jsonSite.read())
        contents = contents[2:-1]
        contents = contents.replace("\\n", "")
        jsonObj = decoder.decode(contents)

    if jsonObj["version"] != __version__:
        log("VERSIONS", "New app version detected!")
        newUpDetect = True
    else:
        log("VERSIONS", "App version is up to date")

except Exception as e:
    log("EXCEPTION", "Cannot fetch version data: "+str(e))

log("SYSTEM", "platform.platform == "+platform.platform())
log("ENVIRONMENT", "File: "+str(__file__))
log("ENVIRONMENT", "Debug: "+str(__debug__))
log("ENVIRONMENT", "Name: "+str(__name__))
log("ENVIRONMENT", "Package: "+str(__package__))

log("UNITS", "Loading units...")
selectedUnitInt = 0
coinsSpent = [0, 0]
battleStartTime = 0
try:
    rawList = os.listdir('units')
except Exception as e:
    log("EXCEPTION", "Cannot load units: "+str(e))
    rawList = []
unitList = []
for i in rawList:
    try:
        executefile("units/"+i+"/unit.py")
        unitList.append([SandboxUnit, MultiplayerUnit])
        log("UNITS", "%s was successful!" % i)
    except Exception as e:
        if not str(e) in alreadyHandled:
            log("EXCEPTION", "%s failed: %s" % (i, str(e)))
            alreadyHandled.append(str(e))
log("UNITS", "unitList == %s" % str(unitList))
sndbxRUnits = pygame.sprite.Group()
sndbxBUnits = pygame.sprite.Group()

if psnSuccess:
    log("MODULES", "PodSixNet was successfully imported")
else:
    log("EXCEPTION", "PodSixNet cannot be imported")
    log("MULTIPLAYER", "Multiplayer is disabled")

set_music("resources/sounds/menuMusic.wav")
try:
    menuBlip = pygame.mixer.Sound("resources/sounds/menuBlip.wav")
    menuBlip.set_volume(effectsVol)
except Exception as e:
    log("EXCEPTION", "Cannot load sounds: "+str(e))
    menuBlip = DummySound()

if majorPyVer == 3:
    import pickle
    log("PICKLE", "Using 'pickle'")
elif majorPyVer == 2:
    log("PICKLE", "Using 'cPickle'")
    import cPickle as pickle

coinRegenBt = TxtOrBt(["Coin Regen. Rate: {}".format(coinRR),
                       False, [0, 0, 0], [255, 255, 0]], [None, 36])
startBudgetBt = TxtOrBt(["Starting Budget: {}".format(startBdgt),
                         False, [0, 0, 0], [255, 255, 0]], [None, 36])
coinRegenBt.rect.topleft = [5, 5]
startBudgetBt.rect.topleft = [5, 40]


log("FONT", "get_default_font() == "+str(pygame.font.get_default_font()))
cursor = Marker(__debugMode__)
if psnSuccess:
    mltPlayBt = TxtOrBt(["MULTIPLAYER", False, [0, 0, 0], [255, 0, 255]], [None, 50])
    mltPlayBt.rect.center = [screen.get_width()/2, screen.get_height()/2+55]
else:
    mltPlayBt = TxtOrBt(["MULTIPLAYER", False, [255, 0, 0],
                         [127, 127, 127]], [None, 50])
    mltPlayBt.rect.center = [screen.get_width()/2, screen.get_height()/2+55]
    buttons.remove(mltPlayBt)
startBt = TxtOrBt(["START", False, [0, 0, 0], [0, 255, 0]], [None, 45])
backBt = TxtOrBt(["BACK", False, [0, 0, 0], [255, 0, 0]], [None, 40])
playBt = TxtOrBt(["SANDBOX", False, [0, 0, 0], [0, 255, 0]], [None, 55])
joinBt = TxtOrBt(["JOIN", False, [0, 0, 0], [255, 255, 0]], [None, 40])
createBt = TxtOrBt(["CREATE", False, [0, 0, 0], [0, 255, 0]], [None, 40])
serverHelpBt = TxtOrBt(["HELP", False, [0, 0, 0], [255, 255, 0]], [None, 40])
nextBt = TxtOrBt([">", False, [0, 0, 0], [127, 127, 127]], [None, 40])
prevBt = TxtOrBt(["<", False, [0, 0, 0], [127, 127, 127]], [None, 40])
clearBlueBt = TxtOrBt(["CLEAR", False, [0, 0, 0], [255, 0, 0]], [None, 45])
clearRedBt = TxtOrBt(["CLEAR", False, [0, 0, 0], [255, 0, 0]], [None, 45])

wait4plyrsTxt = TxtOrBt(["Waiting for players...", False, [255, 0, 0]], [None, 50])
serverTxt = TxtOrBt(["host:port", False, [0, 0, 0]], [None, 45])
serverMsg = TxtOrBt(["Enter the Host and Port", False, [0, 0, 0]], [None, 45])
selectedUnitTxt = TxtOrBt(["", False, [0, 0, 0]], [None, 45])
redCostTxt = TxtOrBt(["Coins Spent: 0", False, [0, 0, 0]], [None, 45])
blueCostTxt = TxtOrBt(["Coins Spent: 0", False, [0, 0, 0]], [None, 45])

bullets = pygame.sprite.Group()
