import pygame as pg
from main.settings import *
from random import randint, choice


class Shot(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.create_image()
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > FLASH_DURATION:
            self.kill()

    def create_image(self):
        gun_flashes = []
        size = randint(20, 50)
        for img in SHOTS:
            gun_flashes.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        image = pg.transform.scale(choice(gun_flashes), (size, size))
        return image