#!venv/bin python
# -*- coding: UTF-8 -*-

"""
(.../TCBS/resources/scripts/funcsAndClasses.py)

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


def log(ltype, msg):
    """
    Writes "[time][ltype]: msg" to "date.log"

    :type ltype: str
    :type msg: str
    :rtype: None
    """
    global __debugMode__
    global os, datetime, traceback
    if not os.path.exists("logs"):
        os.mkdir("logs")
    now = datetime.datetime.now()
    with open("logs/"+str(now.date())+".log", 'a') as logfile:
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
    global sndbxRUnits, sndbxBUnits, coinsSpent
    global redCostTxt, blueCostTxt, battleStartTime
    coinsSpent = [0, 0]
    for i in sndbxRUnits:
        coinsSpent[1] += i.cost
    for i in sndbxBUnits:
        coinsSpent[0] += i.cost
    redCostTxt = TxtOrBt(["Coins Spent: " + str(coinsSpent[1]), False, [0, 0, 0]], [None, 45])
    blueCostTxt = TxtOrBt(["Coins Spent: " + str(coinsSpent[0]), False, [0, 0, 0]], [None, 45])
    updaterects()


def take_screenshot():
    """
    Save a .png file of the screen to the screenshots folder

    :rtype: None
    """
    global menuBlip
    global screen
    menuBlip.play()
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
    global selectedUnitInt, selectedUnitTxt, unitList, state, alreadyHandled
    try:
        selectedUnitInt += movenum
        if selectedUnitInt >= len(unitList):
            selectedUnitInt = 0
        if selectedUnitInt < 0:
            selectedUnitInt = len(unitList)-1
        if state == "sndbx-placeUnits":
            selectedUnitTxt = TxtOrBt([unitList[selectedUnitInt][0].name,
                                       False, [0, 0, 0]], [None, 45])
        if state == "mult-placeUnits":
            selectedUnitTxt = TxtOrBt([unitList[selectedUnitInt][1].name,
                                       False, [0, 0, 0]], [None, 45])
    except Exception as e:
        if not str(e) in alreadyHandled:
            log("EXCEPTION", "Cannot update selectedUnitTxt: "+str(e))
            alreadyHandled.append(str(e))
        selectedUnitTxt = TxtOrBt(["ERROR", False, [255, 0, 0]], [None, 45])
    selectedUnitTxt.rect.center = [screen.get_width()/2, 30]


def updateprofile():
    """
    Update the text sprites in profile

    :rtype: None
    """
    global profileHeading, profileWon, myProfile, profileLost
    global profileMatches, start, pickle, profileTimePlayed

    profileHeading = TxtOrBt([nickname + "'s Profile", False, [0, 0, 0]], [None, 55])
    profileWon = TxtOrBt(["Matches Won: " + str(myProfile['mult-wins']),
                          False, [0, 0, 0]], [None, 40])
    profileLost = TxtOrBt(["Matches Lost: " + str(myProfile['mult-losses']),
                           False, [0, 0, 0]], [None, 40])
    profileMatches = TxtOrBt(["Matches Played: " + str(myProfile['mult-matches']),
                              False, [0, 0, 0]], [None, 40])
    profileTimePlayed = TxtOrBt(["Time Played: " + str(myProfile['time-played']),
                                 False, [0, 0, 0]], [None, 40])

    profileHeading.rect.center = [screen.get_width() / 2, 40]
    profileMatches.rect.center = [screen.get_width() / 2, 70]
    profileWon.rect.center = [screen.get_width() / 2, 100]
    profileLost.rect.center = [screen.get_width() / 2, 130]
    profileTimePlayed.rect.center = [screen.get_width() / 2, 200]

    upend = datetime.datetime.now()
    myProfile['time-played'] += (upend - start)
    with open("resources/profile.pkl", "wb") as fp:
        pickle.dump(myProfile, fp)


def updaterects():
    """
    Update the rects of all sprites when screen size is adjusted

    :rtype: None
    """
    global startBt, mltPlayBt, backBt, joinBt, serverHelpBt
    global nextBt, playBt, prevBt, nextBt, createBt, clearBlueBt, clearRedBt
    global profileBt
    global serverMsg
    global serverTxt, wait4plyrsTxt, selectedUnitTxt
    global redCostTxt, blueCostTxt, profileHeading, profileLost, profileWon
    global profileMatches

    startBt.rect.center = [screen.get_width()/2, screen.get_height()-20]
    mltPlayBt.rect.center = [screen.get_width()/2, screen.get_height()/2+55]
    backBt.rect.bottomleft = [5, screen.get_height()-5]
    playBt.rect.center = [screen.get_width()/2, screen.get_height()/2]
    joinBt.rect.bottomright = [screen.get_width()/2-5, screen.get_height()-5]
    createBt.rect.bottomleft = [screen.get_width()/2+5, screen.get_height()-5]
    serverHelpBt.rect.topright = [screen.get_width()-5, 5]
    prevBt.rect.topleft = [10, 10]
    nextBt.rect.topright = [screen.get_width()-10, 10]
    clearBlueBt.rect.center = [screen.get_width() / 4, 75]
    clearRedBt.rect.center = [screen.get_width() / 4 * 3, 75]
    profileBt.rect.topleft = [5, 5]

    wait4plyrsTxt.rect.topleft = [screen.get_width()/2-150,
                                  screen.get_height()/2-50]
    serverTxt.rect.center = [screen.get_width()/2, screen.get_height()/2]
    serverMsg.rect.center = [screen.get_width()/2, screen.get_height()/2-45]
    selectedUnitTxt.rect.center = [screen.get_width()/2, 30]
    redCostTxt.rect.center = [screen.get_width() / 4 * 3, screen.get_height() - 20]
    blueCostTxt.rect.center = [screen.get_width() / 4, screen.get_height() - 20]
    profileHeading.rect.center = [screen.get_width()/2, 40]
    profileMatches.rect.center = [screen.get_width()/2, 70]
    profileWon.rect.center = [screen.get_width()/2, 100]
    profileLost.rect.center = [screen.get_width()/2, 130]
    profileTimePlayed.rect.center = [screen.get_width() / 2, 200]


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
