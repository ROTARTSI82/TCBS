#!venv/bin python
# -*- coding: UTF-8 -*-

"""
The code for the AI of your soldier!
This is an example, so feel free to modify this code!
"""

import pygame
import random
import time
from pygame.locals import *


class SandboxUnit(pygame.sprite.Sprite):
    """
    This is the version of your soldier that would be loaded in sandbox mode.
    """
    name = "exampleUnit - $10"  # What to display at the top when this unit is selected.

    def __init__(self, pos, team):
        # Define basic attributes
        pygame.sprite.Sprite.__init__(self)
        self.team = team
        self.health = 50
        self.meleeDamage = 10
        self.cooldown = 1
        self.lastAttack = 0

        # Set the icon to a red square if we're on the red team, and a blue one if we're on the blue team.
        self.image = pygame.Surface([25, 25])
        if self.team == "red":
            self.image.fill([255, 0, 0])
        elif self.team == "blue":
            self.image.fill([0, 0, 255])

        # Set the position to pos
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.target = None

    def update(self):
        """
        Is called every tick. Add code to move your soldier here.

        :return: None
        """
        global sndbxRUnits, sndbxBUnits

        # Don't do anything if the battle is over
        if len(sndbxBUnits) == 0 or len(sndbxRUnits) == 0:
            return

        # Check if the target is still alive
        if self.team == "blue":
            if self.target not in sndbxRUnits:
                self.target = random.choice(sndbxRUnits.sprites())
        if self.team == "red":
            if self.target not in sndbxBUnits:
                self.target = random.choice(sndbxBUnits.sprites())

        # Move towards the target
        listcenter = list(self.rect.center)
        if self.rect.center[0] > self.target.rect.center[0]:
            listcenter[0] -= 1
        if self.rect.center[0] < self.target.rect.center[0]:
            listcenter[0] += 1
        if self.rect.center[1] > self.target.rect.center[1]:
            listcenter[1] -= 1
        if self.rect.center[1] < self.target.rect.center[1]:
            listcenter[1] += 1
        self.rect.center = tuple(listcenter)

        # Remove us from sprite group if health reaches 0
        if self.health <= 0:
            self.kill()

    def on_soldier_hit(self, hitlist):
        """
        Is called when two enemy soldiers collide
        Add code to damage your enemy here

        :param hitlist: List of enemy soldiers touching your soldier
        :return:
        """
        # If self.cooldown seconds have passed since self.lastAttack,
        # Damage a random enemy on hitlist by self.meleeDamage
        target = random.choice(hitlist)
        if (time.time() - self.lastAttack) > self.cooldown:
            target.health -= self.meleeDamage
            self.lastAttack = time.time()

    def on_bullet_hit(self, hitlist):
        """
        NotImplemented

        :param hitlist: List of bullet sprites touching your soldier
        :return:
        """


class MultiplayerUnit(pygame.sprite.Sprite):
    """
    This is the version of your soldier that would be loaded in multiplayer mode.
    """
    def __init__(self, pos, team): pass


class Bullet(pygame.sprite.Sprite):
    """
    NotImplemented
    """
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([10, 10])
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        """
        NotImplemented

        :return: None
        """
        pass
