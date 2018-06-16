# -*- coding: UTF-8 -*-
"""
Some simple tools for making units
"""

import pygame
from pygame.locals import *


class SpriteSheet(object):
    """
    Support for loading spritesheets
    """
    def __init__(self, sheet):
        if type(sheet) == pygame.Surface:
            self.sheet = sheet.convert()
        elif type(sheet) == str:
            self.sheet = pygame.image.load(sheet).convert()

    def image_at(self, rectangle, colorkey=None):
        """
        Load an image from the spritesheet.

        :param rectangle: [x, y, width, height]
        :param colorkey: [red, green, blue]
        :rtype: pygame.Surface
        """
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image

    def images_at(self, rects, colorkey=None):
        """
        Load multiple images from the spritesheet

        :param rects: [[x, y, width, height], ...]
        :param colorkey: [red, green, blue]
        :rtype: [pygame.Surface, ...]
        """
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey=None):
        """
        Load a strip of images from the spritesheet

        :param rect: [[x, y, width, height], ...]
        :param image_count: int
        :param colorkey: [red, green, blue]
        :rtype: [pygame.Surface, ...]
        """
        tuples = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3]) for x in range(image_count)]
        return self.images_at(tuples, colorkey)


pygame.init()
screen = pygame.display.set_mode([640, 480])
ss = SpriteSheet("/Users/Grant/Downloads/spritesheet.png")
sfss = ss.image_at((220, 220, 60, 60), (0, 0, 0))
running = 1
while running:
    screen.fill([255, 255, 255])
    screen.blit(sfss, [50, 50])
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = 0

pygame.quit()
