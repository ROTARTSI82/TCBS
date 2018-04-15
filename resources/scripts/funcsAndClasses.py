#!venv/bin python
# -*- coding: UTF-8 -*-

"""
(.../TCBS/resources/scripts/funcsAndClasses.py)
------------------------------------------------------------------------
TOTALLY CUSTOMIZABLE BATTLE SIMULATOR a21.18.04.14
------------------------------------------------------------------------
By Grant Yang

Totally Customizable Battle Simulator is a multiplayer
strategy videogame. You can design and program your
own soldiers and make them fight against your
friend's soldiers. It is uses by Totally Accurate
Battle Simulator by Landfall and requires Pygame 1.9 and
Python 2.7. TCBS uses PodSixNet written by chr15m (Chris McCormick).

SEE README.md FOR MORE DETAILS
"""
import traceback

if False:
    import pygame
    from pygame.locals import *
    # Ignore this code. It makes PyCharm happy
    # Since I call this script via execfile, PyCharm thinks
    # all the variables are undefined and gives me endless warnings :(
    from load import *

__appName__ = "Totally Customizable Battle Simulator"
__version__ = "a21.18.04.14"
__author__ = "Grant Yang"

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
                    print(traceback.format_exc())
                except Exception:
                    pass


def take_screenshot():
    """
    Save a .png file of the screen to the screenshots folder

    :rtype: None
    """
    if not os.path.exists("screenshots"):
        os.mkdir("screenshots")
    pygame.image.save(screen, "screenshots/" + str(datetime.datetime.now()) + ".png")


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


def updaterects():
    """
    Update the rects of all sprites when screen size is adjusted

    :rtype: None
    """
    global startBt, mltPlayBt, backBt, joinBt, serverHelpBt
    global coinRegenBt, startBudgetBt, nextBt
    global serverMsg
    global serverTxt, wait4plyrsTxt, selectedUnitTxt
    startBt.rect.center = [screen.get_width()/2, screen.get_height()-20]
    mltPlayBt.rect.center = [screen.get_width()/2, screen.get_height()/2+55]
    backBt.rect.bottomleft = [5, screen.get_height()-5]
    playBt.rect.center = [screen.get_width()/2, screen.get_height()/2]
    joinBt.rect.bottomright = [screen.get_width()/2-5, screen.get_height()-5]
    createBt.rect.bottomleft = [screen.get_width()/2+5, screen.get_height()-5]
    serverHelpBt.rect.topright = [screen.get_width()-5, 5]
    coinRegenBt.rect.topleft = [5, 5]
    startBudgetBt.rect.topleft = [5, 40]
    prevBt.rect.topleft = [10, 10]
    nextBt.rect.topright = [screen.get_width()-10, 10]

    wait4plyrsTxt.rect.topleft = [screen.get_width()/2-150,
                                  screen.get_height()/2-50]
    serverTxt.rect.center = [screen.get_width()/2, screen.get_height()/2]
    serverMsg.rect.center = [screen.get_width()/2, screen.get_height()/2-45]
    selectedUnitTxt.rect.center = [screen.get_width()/2, 30]


def updateoptions():
    """
    Remove the old sprite from buttons and add
    the new updated sprite to buttons

    :rtype: None
    """
    global buttons
    global coinRegenBt, startBudgetBt
    coinRegenBt.kill()
    startBudgetBt.kill()
    del coinRegenBt
    del startBudgetBt
    coinRegenBt = TxtOrBt(["Coin Regen. Rate: {}".format(coinRR),
                           False, [0, 0, 0], [255, 255, 0]], [None, 36])
    startBudgetBt = TxtOrBt(["Starting Budget: {}".format(startBdgt),
                             False, [0, 0, 0], [255, 255, 0]], [None, 36])
    coinRegenBt.rect.topleft = [5, 5]
    startBudgetBt.rect.topleft = [5, 40]


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
        try:
            self.display[0] = langDict[self.display[0]]
        except KeyError:
            pass
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
                log("EXCEPTION","Cannot load font: "+str(e))
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

    def updatehover(self, hovering):
        """
        Turns button blue if cursor is hovering over it
        Turns buttons to normal color otherwise

        :type hovering: bool
        :rtype: None
        """
        if hovering and self.isButton:
            oldrectcenter = self.rect.center
            self.display[3] = self.hoverColor
            self.image = self.font.render(*self.display)
            self.rect = self.image.get_rect()
            self.rect.center = oldrectcenter
        if not hovering and self.isButton:
            oldrectcenter = self.rect.center
            self.display[3] = self.noHoverColor
            self.image = self.font.render(*self.display)
            self.rect = self.image.get_rect()
            self.rect.center = oldrectcenter
