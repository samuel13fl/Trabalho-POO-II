import pygame as pg
import pytweening as tween
from main.settings import *


class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = type
        self.image = self.create_image()
        self.rect = self.image.get_rect()
        # self.type = type
        self.pos = pos
        self.rect.center = pos
        #self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1

    # def update(self):
    #     #offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
    #     self.rect.centery = self.pos.y + self.dir
    #     self.step += BOB_SPEED
    #     if self.step > BOB_RANGE:
    #         self.step = 0
    #         self.dir *= -1

    def create_image(self):
        item_images = {}
        for item in ITEM_IMAGES:
            item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()
        return item_images[self.type]