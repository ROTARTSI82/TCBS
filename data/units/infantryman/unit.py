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
import math


def from_spritesheet(rectangle):
    """
    Load an image from the spritesheet.

    :param rectangle: [x, y, width, height]
    :rtype: pygame.Surface
    """
    rect = pygame.Rect(rectangle)
    image = pygame.Surface(rect.size).convert()
    image.blit(pygame.image.load("units/spritesheet.png"), (0, 0), rect)
    image.set_colorkey((255, 255, 255), RLEACCEL)
    return image


vanilla_infantryman_blue = from_spritesheet((215, 180, 60, 90))
vanilla_infantryman_red = from_spritesheet((5, 173, 60, 90))


class SandboxUnit(pygame.sprite.Sprite):
    """
    This is the version of your soldier that would be loaded in sandbox mode.
    """
    name = "Infantryman (SANDBOX) - $55"  # What to display at the top when this unit is selected.
    cost = 55  # How many coins your soldier costs to place

    def __init__(self, pos, team):
        # Define basic attributes
        pygame.sprite.Sprite.__init__(self)
        self.team = team
        self.speed = 2.5
        self.target = None

        # Melee attributes
        self.health = 150
        self.rotation = 0
        self.velocity = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(pos)

        # Bullet attributes
        self.lastRangeAttack = 0
        self.rangeCooldown = 0.25

        # Set the icon to a red square if we're on the red team, and a blue one if we're on the blue team.
        if self.team == "red":
            self.image = vanilla_infantryman_red
        elif self.team == "blue":
            self.image = vanilla_infantryman_blue
        self.masterimage = self.image

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

        targetpos = pygame.math.Vector2(self.target.rect.center)
        mypos = pygame.math.Vector2(self.rect.center)
        dx, dy = (targetpos.x - mypos.x, targetpos.y - mypos.y)
        travelTime = mypos.distance_to(targetpos) / self.speed
        if travelTime != 0:
            self.velocity = pygame.math.Vector2((dx / travelTime), (dy / travelTime))
        mypos += self.velocity
        self.rect.center = [int(mypos.x), int(mypos.y)]
        self.rotation = math.degrees(math.atan2(-dy, dx)) - 90
        old_rect_pos = self.rect.center
        self.image = pygame.transform.rotate(self.masterimage, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = old_rect_pos

        # If self.rangeCooldown seconds have passed since self.lastRangeAttack,
        # Shoot a SmartBullet
        if (time.time() - self.lastRangeAttack) > self.rangeCooldown:
            bullets.add(InfantrymanBullet(self.rect.center, self.team, self.target))
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
        pass

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
                RBullets.add(MultiplayerInfantrymanBullet(self.rect.center, self.team))
                self.lastRangeAttack = time.time()
            if self.team == "blue" and calledbyhost:
                BBullets.add(MultiplayerInfantrymanBullet(self.rect.center, self.team))
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


class MultiplayerInfantrymanBullet(pygame.sprite.Sprite):
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
MultiplayerInfantrymanBullet.__name__ = "vanilla_infantryman_bullet"


class InfantrymanBullet(pygame.sprite.Sprite):
    """
    The Bullets shot by your soldier!
    """
    def __init__(self, pos, team, target):
        # Define basic attributes
        pygame.sprite.Sprite.__init__(self)
        self.team = team
        self.speed = 20
        self.damage = 12.5
        self.target = target

        # Set the image to a yellow sqaure and the posistion to pos
        self.image = pygame.Surface([15, 15], SRCALPHA, 32).convert_alpha()
        pygame.draw.circle(self.image, [255, 255, 0], [7, 7], 5)
        self.rect = self.image.get_rect()
        self.rect.center = pos

        targetpos = pygame.math.Vector2(self.target.rect.center)
        self.pos = pygame.math.Vector2(self.rect.center)
        dx, dy = (targetpos.x - self.pos.x, targetpos.y - self.pos.y)
        traveltime = self.pos.distance_to(targetpos) / self.speed
        if traveltime != 0:
            self.velocity = pygame.math.Vector2((dx / traveltime), (dy / traveltime))
        else:
            self.velocity = pygame.math.Vector2(0, 0)

    def update(self):
        """
        Add code to move your bullet!

        :rtype: None
        """
        global sndbxRUnits, sndbxBUnits, screen

        # Don't do anything if the battle is over
        if len(sndbxBUnits) == 0 or len(sndbxRUnits) == 0:
            return

        # Check if the target is still alive,
        # and set a new target if our old target is dead

        # Move towards the target
        if self.velocity == pygame.math.Vector2(0, 0):
            targetpos = pygame.math.Vector2(self.target.rect.center)
            self.pos = pygame.math.Vector2(self.rect.center)
            dx, dy = (targetpos.x - self.pos.x, targetpos.y - self.pos.y)
            traveltime = self.pos.distance_to(targetpos) / self.speed
            if traveltime != 0:
                self.velocity = pygame.math.Vector2((dx / traveltime), (dy / traveltime))
            else:
                self.velocity = pygame.math.Vector2(0, 0)
        self.pos += self.velocity
        self.rect.center = [int(self.pos.x), int(self.pos.y)]

        if self.rect.centery > screen.get_height() or self.rect.centery < 0:
            self.kill()
        if self.rect.centerx > screen.get_width() or self.rect.centerx < 0:
            self.kill()

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


serializableBullets = [MultiplayerInfantrymanBullet, ]
