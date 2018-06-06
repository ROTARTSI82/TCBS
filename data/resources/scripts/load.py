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
import glob
import types

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

executefile("resources/scripts/funcsAndClasses.py")
executefile("resources/scripts/multiplayer.py")

pygame.init()
screen = pygame.display.set_mode(*screenArgs)
caption = "{} {}".format(__appName__, __version__)
pygame.display.set_caption(caption, caption)
try:
    pygame.display.set_icon(pygame.image.load("resources/images/icon.png"))
except Exception:
    log("EXCEPTION", "Failed to set icon"+str(e))
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
vCoinRR = coinRR
vStartBdgt = startBdgt
alreadyHandled = []
serverStr = ""
validChars = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
shiftChars = '~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'
shiftDown = False

lfstr = str(datetime.datetime.now()) + ".log"
if not os.path.exists("logs"):
    os.mkdir("logs")
now = datetime.datetime.now()
with open("logs/"+lfstr, 'a') as logfile:
    msg = "====================[{}]====================\n".format(now.ctime())
    logfile.write(msg)
    if __debugMode__:
        print(msg.strip("\n"))

if majorPyVer == 3:
    import pickle
    log("PICKLE", "Using 'pickle'")
elif majorPyVer == 2:
    log("PICKLE", "Using 'cPickle'")
    import cPickle as pickle
try:
    with open("resources/options.pkl", "rb") as fp:
        options = pickle.load(fp)
    log("OPTIONS", "Got from options.pkl: "+str(options))
    assert type(options['srtBdgt']) == int
    assert type(options['coinRR']) == int
    assert type(options['fps']) == int
    assert type(options['music']) == float
    assert type(options['effects']) == float
    assert type(options['scale']) == float
    assert type(options['lang']) in types.StringTypes
    assert type(options['font']) in types.StringTypes or options['font'] is None
    assert type(options['check4updates']) == bool
    assert type(options['battleEnd']) == str
except (IOError, KeyError, AssertionError) as e:
    log("EXCEPTION", "Cannot load options: "+str(e))
    log("OPTIONS", "Loading defaults...")
    options = {"srtBdgt": 100, "coinRR": 100, "fps": 60,
               "music": 0.5, "effects": 0.5, "scale": 1.0,
               "lang": u"resources/lang/english.json",
               "font": None, "check4updates": True,
               "battleEnd": "Do nothing"}
startBdgt = options['srtBdgt']
coinRR = options['coinRR']
desiredFPS = options['fps']
musicVol = options['music']
effectsVol = options['effects']
GUIScale = options['scale']
langFile = options['lang']
langFont = options['font']
onBattleEnd = options['battleEnd']
check4updates = options['check4updates']
try:
    with open(langFile, "r") as fp:
        langDict = json.load(fp)
except Exception as e:
    langDict = {}
    log("EXCEPTION", "Cannot load language: "+str(e))
langIndex = 0
fontIndex = 0
langList = glob.glob("resources/lang/*.json")
fontList = pygame.font.get_fonts() + glob.glob("resources/fonts/*.ttf")

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
    assert check4updates
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
sbUnitInt = 0
mpUnitInt = 0
coinsSpent = [0, 0]
coinsLeft = [0, 0]
selectedTeam = "blue"
try:
    rawList = os.listdir('units')
except Exception as e:
    log("EXCEPTION", "Cannot load units: "+str(e))
    rawList = []
sbUnits = []
mpUnits = []
for i in rawList:
    try:
        executefile("units/"+i+"/unit.py")
        assert inspect.isclass(SandboxUnit)
        assert inspect.isclass(MultiplayerUnit)
        assert inspect.ismethod(MultiplayerUnit._pack)
        serializable.register(MultiplayerUnit)
        sbUnits.append(SandboxUnit)
        mpUnits.append(MultiplayerUnit)
        log("UNITS", "%s was added" % i)
    except Exception as e:
        if __debugMode__ and os.path.isdir("units/"+i):
            raise
        log("UNITS", "%s failed: %s" % (i, str(e)))
sndbxRUnits = pygame.sprite.Group()
sndbxBUnits = pygame.sprite.Group()
oldRUnits = pygame.sprite.Group()
oldBUnits = pygame.sprite.Group()
multRUnits = pygame.sprite.Group()
multBUnits = pygame.sprite.Group()
multBDict = {}
multRDict = {}
nextRID = 0
nextBID = 0

set_music("resources/sounds/menuMusic.mp3")
set_background("resources/images/sky.png")
try:
    menuBlip = pygame.mixer.Sound("resources/sounds/menuBlip.wav")
    menuBlip.set_volume(effectsVol)
    shutterClick = pygame.mixer.Sound("resources/sounds/shutterClick.wav")
    shutterClick.set_volume(effectsVol)
except Exception as e:
    log("EXCEPTION", "Cannot load sounds: "+str(e))
    menuBlip = DummySound()
    shutterClick = DummySound()

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
clearBlueBt = TxtOrBt(["CLEAR BLUE", False, [0, 0, 0], [255, 0, 0]], [None, 45])
clearRedBt = TxtOrBt(["CLEAR RED", False, [0, 0, 0], [255, 0, 0]], [None, 45])
readyBt = TxtOrBt(["READY", False, [0, 0, 0], [0, 255, 0]], [None, 45])
teamSelectBt = TxtOrBt(["Team: "+selectedTeam.upper(), False, [0, 0, 0],
                        [255, 255, 0]], [None, 45])
optionsBt = TxtOrBt(["OPTIONS", False, [0, 0, 0], [255, 255, 0]], [None, 55])
startBdgtBt = TxtOrBt(["Starting Budget: "+str(startBdgt), False, [0, 0, 0],
                       [255, 255, 0]], [None, 40])
coinRRBt = TxtOrBt(["Coin Regen. Rate: "+str(coinRR), False, [0, 0, 0],
                    [255, 255, 0]], [None, 40])
fpsBt = TxtOrBt(["Desired FPS: "+str(desiredFPS), False, [0, 0, 0],
                 [255, 255, 0]], [None, 40])
musicVolBt = TxtOrBt(["Music Volume: "+str(musicVol), False, [0, 0, 0],
                      [255, 255, 0]], [None, 40])
effectsVolBt = TxtOrBt(["Effects Volume: "+str(effectsVol), False, [0, 0, 0],
                        [255, 255, 0]], [None, 40])
guiScaleBt = TxtOrBt(["GUI Scale: "+str(GUIScale), False, [0, 0, 0], [255, 255, 0]],
                     [None, 40])
langBt = TxtOrBt(["Language: "+"".join(langFile.decode('utf-8').split("/")[-1:])[:-5],
                  False, [0, 0, 0], [255, 255, 0]], [None, 40])
onBattleEndBt = TxtOrBt(["When Battle Ends: "+onBattleEnd, False, [0, 0, 0], [255, 255, 0]],
                        [None, 40])
check4updatesBt = TxtOrBt(["Check For Updates: "+str(check4updates), False, [0, 0, 0],
                           [255, 255, 0]], [None, 40])
if langFont is not None:
    fontBt = TxtOrBt([u"Font: " + u"".join(langFont.decode('utf-8').split(u"/")[-1:])[:-4],
                      False, [0, 0, 0], [255, 255, 0]], [None, 40])
else:
    fontBt = TxtOrBt([u"Font: " + str(langFont), False, [0, 0, 0], [255, 255, 0]], [None, 40])

wait4plyrsTxt = TxtOrBt(["Waiting for players...", False, [255, 0, 0]], [None, 50])
serverTxt = TxtOrBt(["host:port", False, [0, 0, 0]], [None, 45])
serverMsg = TxtOrBt(["Enter the Host and Port", False, [0, 0, 0]], [None, 45])
selectedUnitTxt = TxtOrBt(["", False, [0, 0, 0]], [None, 45])
redCostTxt = TxtOrBt(["Coins Spent: 0", False, [0, 0, 0]], [None, 45])
blueCostTxt = TxtOrBt(["Coins Spent: 0", False, [0, 0, 0]], [None, 45])

redBar = BarSprite(1, 2, [255, 0, 0])
blueBar = BarSprite(1, 2, [0, 0, 255])
bullets = pygame.sprite.Group()
