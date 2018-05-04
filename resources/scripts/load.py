#!venv/bin python
# -*- coding: UTF-8 -*-

"""
(.../TCBS/resources/scripts/load.py)

"""

import datetime
import json
import os
import platform
import sys
import inspect

start = datetime.datetime.now()

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
    from mainloop import *

import pygame
from pygame.locals import *

majorPyVer = sys.version_info.major
if majorPyVer not in [2, 3]:
    print("Bad python version!")
    print("Expected Python 2 or Python 3")
    print("Got Python "+str(majorPyVer))
    sys.exit("Bad python version!")

if majorPyVer == 2:
    from PodSixNet.Server import Server
    from PodSixNet.Channel import Channel
    from PodSixNet.Connection import connection, ConnectionListener
    from PodSixNet.rencode import serializable
elif majorPyVer == 3:
    from PodSixNetPython3.Server import Server
    from PodSixNetPython3.Channel import Channel
    from PodSixNetPython3.Connection import connection, ConnectionListener
    from PodSixNetPython3.rencode import serializable

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
try:
    rawList = os.listdir('units')
except Exception as e:
    log("EXCEPTION", "Cannot load units: "+str(e))
    rawList = []
unitList = []
for i in rawList:
    try:
        executefile("units/"+i+"/unit.py")
        assert inspect.isclass(SandboxUnit), "SandboxUnit isn't class"
        assert inspect.isclass(MultiplayerUnit), "MultiplayerUnit isn't class"
        assert inspect.ismethod(MultiplayerUnit._pack), "MultiplayerUnit._pack isn't method"
        serializable.register(MultiplayerUnit)
        unitList.append([SandboxUnit, MultiplayerUnit])
        log("UNITS", "%s was successful!" % i)
    except Exception as e:
        if not str(e) in alreadyHandled:
            log("EXCEPTION", "%s failed: %s" % (i, str(e)))
            alreadyHandled.append(str(e))
log("UNITS", "unitList == %s" % str(unitList))
sndbxRUnits = pygame.sprite.Group()
sndbxBUnits = pygame.sprite.Group()

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

try:
    with open("resources/profile.pkl", "rb") as fp:
        myProfile = pickle.load(fp)
    assert type(myProfile['time-played']) == datetime.timedelta, "time-played isn't timedelta"
    assert type(myProfile['mult-wins']) == int, "mult-wins isn't int"
    assert type(myProfile['mult-losses']) == int, "mult-losses isn't int"
    assert type(myProfile['mult-matches']) == int, "mult-matches isn't int"
    log("PROFILE", "Got from profile.pkl: "+str(myProfile))
except IOError as e:
    log("EXCEPTION", "Cannot load profile: "+str(e))
    log("PROFILE", "Loading defaults...")
    myProfile = {"time-played": datetime.timedelta(), "mult-wins": 0,
                 "mult-losses": 0, "mult-matches": 0}

log("FONT", "get_default_font() == "+str(pygame.font.get_default_font()))
cursor = Marker(__debugMode__)

mltPlayBt = TxtOrBt(["MULTIPLAYER", False, [0, 0, 0], [255, 0, 255]], [None, 50])
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
profileBt = TxtOrBt(["PROFILE", False, [0, 0, 0], [255, 255, 0]], [None, 45])

wait4plyrsTxt = TxtOrBt(["Waiting for players...", False, [255, 0, 0]], [None, 50])
serverTxt = TxtOrBt(["host:port", False, [0, 0, 0]], [None, 45])
serverMsg = TxtOrBt(["Enter the Host and Port", False, [0, 0, 0]], [None, 45])
selectedUnitTxt = TxtOrBt(["", False, [0, 0, 0]], [None, 45])
redCostTxt = TxtOrBt(["Coins Spent: 0", False, [0, 0, 0]], [None, 45])
blueCostTxt = TxtOrBt(["Coins Spent: 0", False, [0, 0, 0]], [None, 45])

redBar = BarSprite(1, 2, [255, 0, 0])
blueBar = BarSprite(1, 2, [0, 0, 255])
bullets = pygame.sprite.Group()
