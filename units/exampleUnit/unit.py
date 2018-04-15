# -*- coding: UTF-8 -*-

# A very crudely coded AI for testing purposes
# Code is messy, but it works :)


import pygame
import random
import time
from pygame.locals import *

class SandboxUnit(pygame.sprite.Sprite):
    name = "exampleUnit - $10"

    def __init__(self,pos,team):
        pygame.sprite.Sprite.__init__(self)
        self.team = team
        self.health = 250
        self.meleeDamage = 10
        self.cooldown = 1
        self.lastAttack = 0
        try:
            self.image = pygame.image.load(self.team+".png")
        except:
            self.image = pygame.Surface([50, 50])
            if self.team == "red":
                self.image.fill([255,0,0])
            elif self.team == "blue":
                self.image.fill([0,0,255])
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.target = None
    def update(self):
        if len(sndbxBUnits) == 0 or len(sndbxRUnits) == 0:
            return
        if self.team == "blue":
            if self.target not in sndbxRUnits:
                self.target = random.choice(sndbxRUnits.sprites())
        if self.team == "red":
            if self.target not in sndbxBUnits:
                self.target = random.choice(sndbxBUnits.sprites())
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
        if self.health <= 0:
            self.kill()
    def onSoldierHit(self, hitlist):
        target = random.choice(hitlist)
        if (time.time() - self.lastAttack) > self.cooldown:
            target.health -= self.meleeDamage
    def onBulletHit(self, hitlist):
        pass

class MultiplayerUnit(pygame.sprite.Sprite):
    def __init__(self,pos,team): pass

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([10, 10])
        self.rect = self.image.get_rect()
        self.rect.center = pos
    def update(self):
        pass
