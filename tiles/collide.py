import pygame as pg
from tilemap import collide_hit_rect


class Collide:
    def __init__(self, sprite, group):
        self.sprite = sprite
        self.group = group

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self.sprite, self.group, False, collide_hit_rect)
            if hits:
                if hits[0].rect.centerx > self.sprite.hit_rect.centerx:
                    self.sprite.pos.x = hits[0].rect.left - self.sprite.hit_rect.width / 2
                if hits[0].rect.centerx < self.sprite.hit_rect.centerx:
                    self.sprite.pos.x = hits[0].rect.right + self.sprite.hit_rect.width / 2
                self.sprite.vel.x = 0
                self.sprite.hit_rect.centerx = self.sprite.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self.sprite, self.group, False, collide_hit_rect)
            if hits:
                if hits[0].rect.centery > self.sprite.hit_rect.centery:
                    self.sprite.pos.y = hits[0].rect.top - self.sprite.hit_rect.height / 2
                if hits[0].rect.centery < self.sprite.hit_rect.centery:
                    self.sprite.pos.y = hits[0].rect.bottom + self.sprite.hit_rect.height / 2
                self.sprite.vel.y = 0
                self.sprite.hit_rect.centery = self.sprite.pos.y
