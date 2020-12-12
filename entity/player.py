from settings import *
from collide import Collide
import math
from bullet import Bullet
from shot import Shot
from weapon import *
from random import choice, uniform
from itertools import chain


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self, game.all_sprites)
        self.game = game
        self.image = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        self.last_shot = 0
        self.health = PLAYER_HEALTH
        self.weapon = Pistol()
        self.damaged = False
        self.orig_image = self.image
        self.collide = Collide(self, self.game.walls)

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        self.click = False
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071
        if pg.mouse.get_pressed()[0]:
            self.shoot()

    def rotate(self):
        mouse_pos_x, mouse_pos_y = self.game.mousepos_worldpos(pg.mouse.get_pos())
        rel_x = mouse_pos_x - self.pos.x
        rel_y = mouse_pos_y - self.pos.y
        angle = -math.degrees(math.atan2(rel_y, rel_x))
        self.rot = angle
        self.rect = self.image.get_rect(center=self.rect.center)

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.weapon.rate:
            self.last_shot = now
            dir = vec(1, 0).rotate(-self.rot)
            pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
            self.vel = vec(-self.weapon.kickback, 0).rotate(-self.rot)
            for i in range(self.weapon.bullet_count):
                spread = uniform(-self.weapon.spread, self.weapon.spread)
                Bullet(self.game, pos, dir.rotate(spread), self.weapon.damage)
                snd = choice(self.game.weapon_sounds[self.weapon.name])
                if snd.get_num_channels() > 2:
                    snd.stop()
                snd.play()
            Shot(self.game, pos)

    def hit(self):
        self.damaged = True
        self.damage_alpha = chain(DAMAGE_ALPHA * 4)

    def update(self):
        self.rotate()
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        temp = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.image = pg.transform.rotate(temp, self.rot)
        if self.damaged:
            try:
                self.image.fill((255, 255, 255, next(self.damage_alpha)), special_flags=pg.BLEND_RGBA_MULT)
            except:
                self.damaged = False
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        self.collide.collide_with_walls('x')
        self.hit_rect.centery = self.pos.y
        self.collide.collide_with_walls('y')
        self.rect.center = self.hit_rect.center

    def add_health(self, amount):
        self.health += amount
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH