import pygame as pg
from main.settings import *
from random import uniform


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, damage):  # dir é direção que a bala percorrerá
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.create_image()
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * self.game.player.weapon.bullet_speed * uniform(0.9, 1.1)
        self.spawn_time = pg.time.get_ticks()
        self.damage = damage

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > self.game.player.weapon.bullet_lifetime:
            self.kill()

    def create_image(self):
        bullet_images = {}
        bullet_images['lg'] = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        bullet_images['sm'] = pg.transform.scale(bullet_images['lg'], (10, 10))
        return bullet_images[self.game.player.weapon.bullet_size]