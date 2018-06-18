#!venv/bin python
# -*- coding: UTF-8 -*-

"""
(.../TCBS/data/resources/scripts/funcsAndClasses.py)

"""
import traceback

if False:
    from pygame.locals import *
    # Ignore this code. It makes PyCharm happy
    # Since I call this script via execfile, PyCharm thinks
    # all the variables are undefined and gives me endless warnings :(
    from load import *


class DummySound(object):
    """
    What we pass as a sound object if we can't load the sound
    Has all the methods of a sound object, but all methods do nothing
    """
    def __init__(self):
        pass

    def set_volume(self, volume):
        """
        A method of a sound object; This does nothing

        :type volume: float
        :rtype: None
        """
        pass

    def play(self, looptimes=0):
        """
        A method of a sound object; This does nothing

        :type looptimes: int
        :rtype: None
        """
        pass

    def load(self, loadfile):
        """
        A method of a sound object; This does nothing

        :type loadfile: str
        :rtype: None
        """
        pass


def debug(ltype, msg):
    """
    Only log the message if __debugMode__ is activated

    :type ltype: str
    :type msg: str
    :rtype: None
    """
    if __debugMode__:
        log(ltype, msg)

def log(ltype, msg):
    """
    Writes "[time][ltype]: msg" to "date.log"

    :type ltype: str
    :type msg: str
    :rtype: None
    """
    global __debugMode__, lfstr
    global os, datetime, traceback
    if not os.path.exists("logs"):
        os.mkdir("logs")
    now = datetime.datetime.now()
    with open("logs/"+lfstr, 'a') as logfile:
        msg2 = "[{}] [{}]: {}\n".format(now.time(), ltype, msg)
        logfile.write(msg2)
        if __debugMode__:
            print(msg2.strip("\n"))
        if ltype == "EXCEPTION":
            try:
                if __debugMode__:
                    print(traceback.format_exc())
                logfile.write(traceback.format_exc())
            except Exception:
                pass


def updatecost():
    """
    Update the text sprites

    :rtype: None
    """
    global sndbxRUnits, sndbxBUnits, coinsSpent, coinsLeft
    global redCostTxt, blueCostTxt, battleStartTime
    global redBar, blueBar, multBUnits, multRUnits
    hplist = [0, 0]
    coinsSpent = [0, 0]
    if state in ["sndbx-placeUnits", "sndbx-battle"]:
        for i in sndbxRUnits:
            try:
                coinsSpent[1] += i.cost
                hplist[1] += i.health
            except Exception as e:
                if __debugMode__:
                    raise
                if str(e) not in alreadyHandled:
                    alreadyHandled.append(str(e))
                    log("EXCEPTION", "updatecost() failed: "+str(e))
        for i in sndbxBUnits:
            try:
                coinsSpent[0] += i.cost
                hplist[0] += i.health
            except Exception as e:
                if __debugMode__:
                    raise
                if str(e) not in alreadyHandled:
                    alreadyHandled.append(str(e))
                    log("EXCEPTION", "updatecost() failed: "+str(e))
        try:
            redBar.update(hplist[1], sum(hplist))
            blueBar.update(hplist[0], sum(hplist))
        except:
            pass
        redCostTxt = TxtOrBt(["Red Coins Spent: " + str(coinsSpent[1]), False, [0, 0, 0]], [None, 45])
        blueCostTxt = TxtOrBt(["Blue Coins Spent: " + str(coinsSpent[0]), False, [0, 0, 0]], [None, 45])
        updaterects()
    elif state in ["mult-placeUnits", "mult-battle"]:
        for i in multRUnits:
            try:
                hplist[1] += i.health
            except Exception as e:
                if __debugMode__:
                    raise
                if str(e) not in alreadyHandled:
                    alreadyHandled.append(str(e))
                    log("EXCEPTION", "updatecost() failed: "+str(e))
        for i in multBUnits:
            try:
                hplist[0] += i.health
            except Exception as e:
                if __debugMode__:
                    raise
                if str(e) not in alreadyHandled:
                    alreadyHandled.append(str(e))
                    log("EXCEPTION", "updatecost() failed: "+str(e))
        try:
            redBar.update(hplist[1], sum(hplist))
            blueBar.update(hplist[0], sum(hplist))
        except:
            pass
        redCostTxt = TxtOrBt(["Coins Left: " + str(coinsLeft[1]),
                              False, [0, 0, 0]], [None, 45])
        blueCostTxt = TxtOrBt(["Coins Left: " + str(coinsLeft[0]),
                               False, [0, 0, 0]], [None, 45])
        updaterects()

def take_screenshot():
    """
    Save a .png file of the screen to the screenshots folder

    :rtype: None
    """
    global menuBlip
    global screen
    shutterClick.play()
    filename = str(datetime.datetime.now()) + ".png"
    log("SCREENSHOT", "Screenshot saved as " + filename)
    screen.fill([255, 255, 255])
    if not os.path.exists("screenshots"):
        os.mkdir("screenshots")
    pygame.image.save(screen, "screenshots/" + filename)
    pygame.display.flip()
    pygame.time.wait(1000)


def set_music(filename):
    """
    Set pygame.mixer.music to filename and stop old music
    Checks if filename is loadable

    :type filename: str
    :rtype: None
    """
    global pygame, alreadyHandled
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.set_volume(musicVol)
        pygame.mixer.music.play(-1)
    except Exception as e:
        if not str(e) in alreadyHandled:
            log("EXCEPTION", "Cannot load music: "+str(e))
            alreadyHandled.append(str(e))


def updateselectedunit(movenum):
    """
    Updates selectedUnitTxt sprite, and selectedUnitInt based on state and moveNum

    :type movenum: int
    :rtype: None
    """
    global selectedUnitTxt, state, alreadyHandled
    global sbUnits, mpUnits, mpUnitInt, sbUnitInt
    try:
        if state in ["sndbx-placeUnits", "sndbx-battle"]:
            sbUnitInt += movenum
            if sbUnitInt >= len(sbUnits):
                sbUnitInt = 0
            if sbUnitInt < 0:
                sbUnitInt = len(sbUnits) - 1
            selectedUnitTxt = TxtOrBt([sbUnits[sbUnitInt].name,
                                       False, [0, 0, 0]], [None, 45])
        if state in ["mult-placeUnits", "mult-battle"]:
            mpUnitInt += movenum
            if mpUnitInt >= len(mpUnits):
                mpUnitInt = 0
            if mpUnitInt < 0:
                mpUnitInt = len(mpUnits) - 1
            selectedUnitTxt = TxtOrBt([mpUnits[mpUnitInt].name,
                                       False, [0, 0, 0]], [None, 45])
    except Exception as e:
        if not str(e) in alreadyHandled:
            log("EXCEPTION", "Cannot update selectedUnitTxt: "+str(e))
            alreadyHandled.append(str(e))
        selectedUnitTxt = TxtOrBt(["ERROR", False, [255, 0, 0]], [None, 45])
    updaterects()


def updateoptions():
    """
    Update the text sprites in profile

    :rtype: None
    """
    global options, startBdgtBt, coinRRBt, fpsBt, musicVolBt, effectsVolBt
    global guiScaleBt, langBt, startBdgt, coinRR, desiredFPS, musicVol, fontBt
    global effectsVol, GUIScale, langFile, buttons, mltPlayBt, newUpNote, ceasefireBt
    global startBt, backBt, playBt, joinBt, createBt, serverHelpBt, badVerWarn
    global nextBt, prevBt, clearRedBt, clearBlueBt, readyBt, selectedTeam, serverStr
    global teamSelectBt, optionsBt, langDict, menuBlip, alreadyHandled, onBattleEnd
    global langFont, wait4plyrsTxt, serverTxt, serverMsg, selectedUnitTxt
    global redCostTxt, blueCostTxt, onBattleEndBt, check4updatesBt, check4updates

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
        log("EXCEPTION", "Cannot load language: " + str(e))
    pygame.mixer.music.set_volume(musicVol)
    try:
        menuBlip = pygame.mixer.Sound("resources/sounds/menuBlip.wav")
        menuBlip.set_volume(effectsVol)
    except Exception as e:
        if str(e) not in alreadyHandled:
            log("EXCEPTION", "Cannot load sounds: " + str(e))
            alreadyHandled.append(str(e))
        menuBlip = DummySound()
    buttons = pygame.sprite.Group()
    newUpNote = TxtOrBt(["New Update Detected!", False, [0, 0, 0], [0, 255, 0]], [None, 35])
    newUpNote.rect.topleft = [10, 40]
    badVerWarn = TxtOrBt(["Bad Version Detected!", False, [0, 0, 0], [255, 0, 0]], [None, 35])
    badVerWarn.rect.topleft = [10, 10]

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
    ceasefireBt = TxtOrBt(["CEASEFIRE", False, [0, 0, 0], [255, 0, 0]], [None, 45])
    teamSelectBt = TxtOrBt(["Team: " + selectedTeam.upper(), False, [0, 0, 0],
                            [255, 255, 0]], [None, 45])
    optionsBt = TxtOrBt(["OPTIONS", False, [0, 0, 0], [255, 255, 0]], [None, 55])
    startBdgtBt = TxtOrBt(["Starting Budget: " + str(startBdgt), False, [0, 0, 0],
                           [255, 255, 0]], [None, 40])
    coinRRBt = TxtOrBt(["Coin Regen. Rate: " + str(coinRR), False, [0, 0, 0],
                        [255, 255, 0]], [None, 40])
    fpsBt = TxtOrBt(["Desired FPS: " + str(desiredFPS), False, [0, 0, 0],
                     [255, 255, 0]], [None, 40])
    musicVolBt = TxtOrBt(["Music Volume: " + str(musicVol), False, [0, 0, 0],
                          [255, 255, 0]], [None, 40])
    effectsVolBt = TxtOrBt(["Effects Volume: " + str(effectsVol), False, [0, 0, 0],
                            [255, 255, 0]], [None, 40])
    guiScaleBt = TxtOrBt(["GUI Scale: " + str(GUIScale), False, [0, 0, 0], [255, 255, 0]],
                         [None, 40])
    langBt = TxtOrBt(["Language: " + "".join(langFile.decode('utf-8').split("/")[-1:])[:-5],
                      False, [0, 0, 0], [255, 255, 0]], [None, 40])
    onBattleEndBt = TxtOrBt(["When Battle Ends: " + onBattleEnd, False, [0, 0, 0], [255, 255, 0]],
                            [None, 40])
    check4updatesBt = TxtOrBt(["Check For Updates: " + str(check4updates), False, [0, 0, 0],
                               [255, 255, 0]], [None, 40])
    if langFont is not None:
        fontBt = TxtOrBt([u"Font: " + u"".join(langFont.decode('utf-8').split(u"/")[-1:])[:-4],
                          False, [0, 0, 0], [255, 255, 0]], [None, 40])
    else:
        fontBt = TxtOrBt([u"Font: " + str(langFont), False, [0, 0, 0], [255, 255, 0]], [None, 40])

    wait4plyrsTxt = TxtOrBt(["Waiting for players...", False, [255, 0, 0]], [None, 50])
    if serverStr.strip() == "":
        serverTxt = TxtOrBt(["host:port", False, [0, 0, 0]], [None, 45])
    else:
        serverTxt = TxtOrBt([serverStr, False, [0, 0, 0]], [None, 45], "ignoreTranslations")
    serverMsg = TxtOrBt(["Enter the Host and Port", False, [0, 0, 0]], [None, 45])
    selectedUnitTxt = TxtOrBt(["", False, [0, 0, 0]], [None, 45])
    redCostTxt = TxtOrBt(["Red Coins Spent: 0", False, [0, 0, 0]], [None, 45])
    blueCostTxt = TxtOrBt(["Blue Coins Spent: 0", False, [0, 0, 0]], [None, 45])
    updaterects()
    with open("resources/options.pkl", "wb") as fp:
        pickle.dump(options, fp)


def updaterects():
    """
    Update the rects of all sprites when screen size is adjusted

    :rtype: None
    """
    global startBt, mltPlayBt, backBt, joinBt, serverHelpBt
    global nextBt, playBt, prevBt, nextBt, createBt, clearBlueBt, clearRedBt
    global profileBt, readyBt, teamSelectBt, optionsBt, coinRRBt, startBdgtBt
    global fpsBt, musicVolBt, effectsVolBt, guiScaleBt, langBt, fontBt
    global check4updatesBt, onBattleEndBt, ceasefireBt
    global serverMsg
    global serverTxt, wait4plyrsTxt, selectedUnitTxt
    global redCostTxt, blueCostTxt, redBar, blueBar

    startBt.rect.center = [screen.get_width() / 2, screen.get_height()-20]
    mltPlayBt.rect.center = [screen.get_width() / 2, screen.get_height() / 2+55]
    backBt.rect.bottomleft = [5, screen.get_height()-10]
    playBt.rect.center = [screen.get_width() / 2, screen.get_height() / 2]
    joinBt.rect.bottomright = [screen.get_width() / 2-5, screen.get_height()-5]
    createBt.rect.bottomleft = [screen.get_width() / 2+5, screen.get_height()-5]
    serverHelpBt.rect.topright = [screen.get_width()-5, 5]
    prevBt.rect.topleft = [10, 15]
    nextBt.rect.topright = [screen.get_width()-10, 15]
    clearBlueBt.rect.center = [screen.get_width() / 4, 75]
    clearRedBt.rect.center = [screen.get_width() / 4 * 3, 75]
    readyBt.rect.center = [screen.get_width() / 2, screen.get_height()-20]
    ceasefireBt.rect.center = [screen.get_width() / 2, screen.get_height() - 20]
    teamSelectBt.rect.center = [screen.get_width() / 2, 75]
    optionsBt.rect.center = [screen.get_width() / 2, screen.get_height() / 2+110]
    coinRRBt.rect.topleft = [10, 10]
    startBdgtBt.rect.topleft = [coinRRBt.rect.right+10, 10]
    fpsBt.rect.topleft = [10, 50]
    guiScaleBt.rect.topleft = [fpsBt.rect.right+10, 50]
    musicVolBt.rect.topleft = [10, 100]
    effectsVolBt.rect.topleft = [musicVolBt.rect.right+10, 100]
    langBt.rect.topleft = [10, 150]
    fontBt.rect.topleft = [langBt.rect.right+10, 150]
    onBattleEndBt.rect.topleft = [10, 200]
    check4updatesBt.rect.topleft = [onBattleEndBt.rect.right+10, 200]

    wait4plyrsTxt.rect.topleft = [screen.get_width() / 2-150,
                                  screen.get_height() / 2-50]
    serverTxt.rect.center = [screen.get_width() / 2, screen.get_height()/2]
    serverMsg.rect.center = [screen.get_width() / 2, screen.get_height()/2-45]
    selectedUnitTxt.rect.center = [screen.get_width() / 2, 35]
    redCostTxt.rect.center = [screen.get_width() / 4 * 3, screen.get_height() - 20]
    blueCostTxt.rect.center = [screen.get_width() / 4, screen.get_height() - 20]

    blueBar.rect.topleft = [0, 0]
    redBar.rect.topright = [screen.get_width(), 0]


class Marker(pygame.sprite.Sprite):
    """
    A cursor-tracking sprite
    """
    def __init__(self, visible):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([0, 0])
        if visible:
            self.image = pygame.Surface([10, 10])
        self.rect = self.image.get_rect()
        self.rect.center = pygame.mouse.get_pos()


class BarSprite(pygame.sprite.Sprite):
    """
    A sprite class for sprites such as health bars
    """
    def __init__(self, value, maxval, color):
        global screen
        self.color = color
        self.image = pygame.Surface([int(value/float(maxval)*screen.get_width()), 10])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

    def update(self, value, maxval):
        """
        Update the surface

        :type value: int
        :type maxval: int
        :rtype: None
        """
        global alreadyHandled
        try:
            self.image = pygame.Surface([int(value/float(maxval)*screen.get_width()), 10])
            self.image.fill(self.color)
            self.rect = self.image.get_rect()
            updaterects()
        except (pygame.error, ZeroDivisionError):
            pass


class TxtOrBt(pygame.sprite.Sprite):
    """
    If background color is specified, then it is a button sprite
    and is added to the buttons Group.

    If background color isn't specified, then it is a text sprite.
    """
    def __init__(self, display, font_args, obj_id=()):
        global buttons, langDict
        pygame.sprite.Sprite.__init__(self)
        self.display = display
        try:
            self.isButton = True
            self.noHoverColor = self.display[3]
        except IndexError:
            self.isButton = False
        if obj_id != "ignoreTranslations":
            translist = self.display[0].split(":")
            for index, i in enumerate(translist):
                try:
                    translist[index] = langDict[i]
                except KeyError:
                    pass
            self.display[0] = u":".join(translist)
        self.id = obj_id
        fontsize = font_args[1]
        self.font_args = list(font_args)
        self.font_args[1] = int(self.font_args[1] * GUIScale)
        try:
            self.font_args[0] = langFont
            if "sys" not in self.font_args:
                self.font = pygame.font.Font(*self.font_args)
            else:
                self.font = pygame.font.SysFont(*self.font_args[:-1])
        except Exception as e:
            if not str(e) in alreadyHandled:
                alreadyHandled.append(str(e))
                log("EXCEPTION", "Cannot load font: " + str(e))
            self.font_args[0] = None
            self.font_args[1] = fontsize
            if "sys" not in self.font_args:
                self.font = pygame.font.Font(*self.font_args)
            else:
                self.font = pygame.font.SysFont(*self.font_args[:-1])
        self.image = self.font.render(*self.display)
        self.rect = self.image.get_rect()
        self.rect.center = [0, 0]
        self.hoverColor = [0, 0, 255]
        if self.isButton:
            buttons.add(self)

    def update(self, collisions):
        """
        Turns button blue if cursor is hovering over it
        Turns buttons to normal color otherwise

        :type collisions: list
        :rtype: None
        """
        if self in collisions and self.isButton:
            oldrectcenter = self.rect.center
            self.display[3] = self.hoverColor
            self.image = self.font.render(*self.display)
            self.rect = self.image.get_rect()
            self.rect.center = oldrectcenter
        if self not in collisions and self.isButton:
            oldrectcenter = self.rect.center
            self.display[3] = self.noHoverColor
            self.image = self.font.render(*self.display)
            self.rect = self.image.get_rect()
            self.rect.center = oldrectcenter
