import pygame as pg
from tiles.tilemap import collide_hit_rect


# classe feita para colisão de uma sprite com as paredes do jogo
class Collide:
    def __init__(self, sprite, group):
        self.sprite = sprite
        self.group = group

    def collide_with_walls(self, dir):
        # colisão na horizontal
        # o parâmetro collide_hit_rect é necessário para fazer a função usar hit_rect ao invés de rect
        # lembrando que rect é só para a imagem, não para a colisão
        if dir == 'x':
            hits = pg.sprite.spritecollide(self.sprite, self.group, False, collide_hit_rect)
            if hits:
                # checa se o centro da parede é maior que o centro do jogador
                # é necessário fazer isso para as 4 direções possíveis
                if hits[0].rect.centerx > self.sprite.hit_rect.centerx:
                    self.sprite.pos.x = hits[0].rect.left - self.sprite.hit_rect.width / 2
                if hits[0].rect.centerx < self.sprite.hit_rect.centerx:
                    self.sprite.pos.x = hits[0].rect.right + self.sprite.hit_rect.width / 2
                self.sprite.vel.x = 0
                self.sprite.hit_rect.centerx = self.sprite.pos.x
        # colisão na vertical
        if dir == 'y':
            hits = pg.sprite.spritecollide(self.sprite, self.group, False, collide_hit_rect)
            if hits:
                if hits[0].rect.centery > self.sprite.hit_rect.centery:
                    self.sprite.pos.y = hits[0].rect.top - self.sprite.hit_rect.height / 2
                if hits[0].rect.centery < self.sprite.hit_rect.centery:
                    self.sprite.pos.y = hits[0].rect.bottom + self.sprite.hit_rect.height / 2
                self.sprite.vel.y = 0
                self.sprite.hit_rect.centery = self.sprite.pos.y
