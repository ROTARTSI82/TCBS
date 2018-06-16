#!venv/bin python
# -*- coding: UTF-8 -*-

"""
The code for the AI of your soldier!
This is an example, so feel free to modify this code!
"""

import random
import time

import pygame
from pygame.locals import *


def from_spritesheet(spritesheet, rectangle, colorkey=None):
    """
    Load an image from the spritesheet.

    :param spritesheet: str or pygame.Surface
    :param rectangle: [x, y, width, height]
    :param colorkey: [red, green, blue]
    :rtype: pygame.Surface
    """
    rect = pygame.Rect(rectangle)
    image = pygame.Surface(rect.size).convert()
    if type(spritesheet) == str:
        image.blit(pygame.image.load(spritesheet), (0, 0), rect)
    elif type(spritesheet) == pygame.Surface:
        image.blit(spritesheet, (0, 0), rect)
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image


class SandboxUnit(pygame.sprite.Sprite):
    """
    This is the version of your soldier that would be loaded in sandbox mode.
    """
    name = "Infantryman (SANDBOX) - $100"  # What to display at the top when this unit is selected.
    cost = 100  # How many coins your soldier costs to place

    def __init__(self, pos, team):
        # Define basic attributes
        pygame.sprite.Sprite.__init__(self)
        self.team = team
        self.speed = 1
        self.target = None

        # Melee attributes
        self.health = 50
        self.meleeDamage = 10
        self.meleeCooldown = 1
        self.lastMeleeAttack = 0

        # Bullet attributes
        self.lastRangeAttack = 0
        self.rangeCooldown = 2

        # Set the icon to a red square if we're on the red team, and a blue one if we're on the blue team.
        self.image = pygame.Surface([25, 25])
        if self.team == "red":
            self.image.fill([255, 0, 0])
        elif self.team == "blue":
            self.image.fill([0, 0, 255])

        # Set the position to pos
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def pack(self):
        """
        Return the arguments that __init__() takes

        :rtype: ((int, int), str)
        """
        return self.rect.center, self.team

    def update(self):
        """
        Is called every tick. Add code to move your soldier here.

        :return: None
        """
        global sndbxRUnits, sndbxBUnits, bullets

        # Don't do anything if the battle is over
        if len(sndbxBUnits) == 0 or len(sndbxRUnits) == 0:
            return

        # Check if the target is still alive,
        # and set a new target if our old target is dead
        if self.team == "blue":
            if self.target not in sndbxRUnits:
                self.target = random.choice(sndbxRUnits.sprites())
        if self.team == "red":
            if self.target not in sndbxBUnits:
                self.target = random.choice(sndbxBUnits.sprites())

        # Move towards the target
        listcenter = list(self.rect.center)
        if self.rect.center[0] > self.target.rect.center[0]:
            listcenter[0] -= self.speed
        if self.rect.center[0] < self.target.rect.center[0]:
            listcenter[0] += self.speed
        if self.rect.center[1] > self.target.rect.center[1]:
            listcenter[1] -= self.speed
        if self.rect.center[1] < self.target.rect.center[1]:
            listcenter[1] += self.speed
        self.rect.center = tuple(listcenter)

        # If self.rangeCooldown seconds have passed since self.lastRangeAttack,
        # Shoot a SmartBullet
        if (time.time() - self.lastRangeAttack) > self.rangeCooldown:
            bullets.add(SmartBullet(self.rect.center, self.team))
            self.lastRangeAttack = time.time()

        # Remove us from sprite group if health reaches 0
        if self.health <= 0:
            self.kill()

    def on_soldier_hit(self, hitlist):
        """
        Is called when two enemy soldiers collide
        Add code to damage your enemy here

        :param hitlist: List of enemy soldiers touching your soldier
        :return: None
        """
        # If self.meleeCooldown seconds have passed since self.lastMeleeAttack,
        # Damage a random enemy on hitlist by self.meleeDamage
        target = random.choice(hitlist)
        if (time.time() - self.lastMeleeAttack) > self.meleeCooldown:
            target.health -= self.meleeDamage
            self.lastMeleeAttack = time.time()

    def on_bullet_hit(self, hitlist):
        """
        NotImplemented

        :param hitlist: List of bullet sprites touching your soldier
        :return:
        """
        pass


class MultiplayerUnit(pygame.sprite.Sprite):
    """
    This is the version of your soldier that would be loaded in multiplayer mode.
    """
    name = "exampleUnit (MULTIPLAYER) - $20"
    cost = 20

    def __init__(self, pos, team, unitid):
        pygame.sprite.Sprite.__init__(self)
        self.team = team
        self.speed = 1
        self.unitid = unitid
        self.health = 50

        self.meleeDamage = 10
        self.meleeCooldown = 1
        self.lastMeleeAttack = 0
        self.target = None

        self.lastRangeAttack = 0
        self.rangeCooldown = 2

        self.image = pygame.Surface([25, 25])
        if team == "red":
            self.image.fill([255, 0, 0])
        elif team == "blue":
            self.image.fill([0, 0, 255])

        self.rect = self.image.get_rect()
        self.rect.center = pos

    def _pack(self):
        return self.rect.center, self.team, self.unitid

    def damage(self, amount):
        self.health -= amount

    def update(self, calledbyhost):
        global multRUnits, multBUnits, bullets, BBullets, RBullets

        # Don't do anything if the battle is over
        if len(multBUnits) == 0 or len(multRUnits) == 0:
            return

        # Check if the target is still alive,
        # and set a new target if our old target is dead
        if self.team == "blue":
            if self.target not in multRUnits:
                self.target = random.choice(multRUnits.sprites())
        if self.team == "red":
            if self.target not in multBUnits:
                self.target = random.choice(multBUnits.sprites())

        # Move towards the target
        listcenter = list(self.rect.center)
        if self.rect.center[0] > self.target.rect.center[0]:
            listcenter[0] -= self.speed
        if self.rect.center[0] < self.target.rect.center[0]:
            listcenter[0] += self.speed
        if self.rect.center[1] > self.target.rect.center[1]:
            listcenter[1] -= self.speed
        if self.rect.center[1] < self.target.rect.center[1]:
            listcenter[1] += self.speed
        self.rect.center = tuple(listcenter)

        if (time.time() - self.lastRangeAttack) > self.rangeCooldown:
            if self.team == "red" and not calledbyhost:
                RBullets.add(MultiplayerSmartBullet(self.rect.center, self.team))
                self.lastRangeAttack = time.time()
            if self.team == "blue" and calledbyhost:
                BBullets.add(MultiplayerSmartBullet(self.rect.center, self.team))
                self.lastRangeAttack = time.time()

        if self.health <= 0:
            self.kill()

    def on_soldier_hit(self, hitlist, calledbyhost):
        """
        Is called when two enemy soldiers collide
        Add code to damage your enemy here

        :param hitlist: List of enemy soldiers touching your soldier
        :return: None
        """
        # If self.meleeCooldown seconds have passed since self.lastMeleeAttack,
        # Damage a random enemy on hitlist by self.meleeDamage
        pass

    def on_bullet_hit(self, hitlist, calledbyhost):
        """
        NotImplemented

        :param hitlist: List of bullet sprites touching your soldier
        :return:
        """
        pass


class MultiplayerSmartBullet(pygame.sprite.Sprite):
    def __init__(self, pos, team):
        # Define basic attributes
        pygame.sprite.Sprite.__init__(self)
        self.team = team
        self.speed = 3
        self.damage = 20
        self.target = None

        # Set the image to a yellow sqaure and the posistion to pos
        self.image = pygame.Surface([10, 10])
        self.image.fill([255, 255, 0])
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def _pack(self):
        return self.rect.center, self.team

    def update(self, calledbyhost):
        """
        Add code to move your bullet!

        :rtype: None
        """
        global multRUnits, multBUnits

        # Don't do anything if the battle is over
        if len(multBUnits) == 0 or len(multRUnits) == 0:
            return

        # Check if the target is still alive,
        # and set a new target if our old target is dead
        if self.team == "blue":
            if self.target not in multRUnits:
                self.target = random.choice(multRUnits.sprites())
        if self.team == "red":
            if self.target not in multBUnits:
                self.target = random.choice(multBUnits.sprites())

        # Move towards the target
        listcenter = list(self.rect.center)
        if self.rect.center[0] > self.target.rect.center[0]:
            listcenter[0] -= self.speed
        if self.rect.center[0] < self.target.rect.center[0]:
            listcenter[0] += self.speed
        if self.rect.center[1] > self.target.rect.center[1]:
            listcenter[1] -= self.speed
        if self.rect.center[1] < self.target.rect.center[1]:
            listcenter[1] += self.speed
        self.rect.center = tuple(listcenter)

    def on_bullet_hit(self, hitlist, calledbyhost):
        """
        Called when the bullet touches a soldier

        :param hitlist: List of soldiers touching the bullet
        :return: None
        """
        global multRUnits, multBUnits, c
        # Damage a random enemy touching the bullet
        for k in hitlist:
            if self.team == "red" and k in multBUnits:
                if not calledbyhost:
                    c.Send({"action": "callfunc", "unitid": k.unitid, "sentbyhost": calledbyhost,
                            "func": "damage", "args": [self.damage, ], "kwargs": {}})
                self.kill()
                return
            if self.team == "blue" and k in multRUnits:
                if calledbyhost:
                    c.Send({"action": "callfunc", "unitid": k.unitid, "sentbyhost": calledbyhost,
                            "func": "damage", "args": [self.damage, ], "kwargs": {}})
                self.kill()
                return


MultiplayerUnit.__name__ = "vanilla_infantryman"
MultiplayerSmartBullet.__name__ = "vanilla_infantryman_bullet"


class SmartBullet(pygame.sprite.Sprite):
    """
    The Bullets shot by your soldier!
    """
    def __init__(self, pos, team):
        # Define basic attributes
        pygame.sprite.Sprite.__init__(self)
        self.team = team
        self.speed = 3
        self.damage = 20
        self.target = None

        # Set the image to a yellow sqaure and the posistion to pos
        self.image = pygame.Surface([10, 10])
        self.image.fill([255, 255, 0])
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        """
        Add code to move your bullet!

        :rtype: None
        """
        global sndbxRUnits, sndbxBUnits

        # Don't do anything if the battle is over
        if len(sndbxBUnits) == 0 or len(sndbxRUnits) == 0:
            return

        # Check if the target is still alive,
        # and set a new target if our old target is dead
        if self.team == "blue":
            if self.target not in sndbxRUnits:
                self.target = random.choice(sndbxRUnits.sprites())
        if self.team == "red":
            if self.target not in sndbxBUnits:
                self.target = random.choice(sndbxBUnits.sprites())

        # Move towards the target
        listcenter = list(self.rect.center)
        if self.rect.center[0] > self.target.rect.center[0]:
            listcenter[0] -= self.speed
        if self.rect.center[0] < self.target.rect.center[0]:
            listcenter[0] += self.speed
        if self.rect.center[1] > self.target.rect.center[1]:
            listcenter[1] -= self.speed
        if self.rect.center[1] < self.target.rect.center[1]:
            listcenter[1] += self.speed
        self.rect.center = tuple(listcenter)

    def on_bullet_hit(self, hitlist):
        """
        Called when the bullet touches a soldier

        :param hitlist: List of soldiers touching the bullet
        :return: None
        """
        global sndbxRUnits, sndbxBUnits
        # Damage a random enemy touching the bullet
        for k in hitlist:
            if self.team == "red" and k in sndbxBUnits:
                k.health -= self.damage
                self.kill()
                return
            if self.team == "blue" and k in sndbxRUnits:
                k.health -= self.damage
                self.kill()
                return


serializableBullets = [MultiplayerSmartBullet, ]