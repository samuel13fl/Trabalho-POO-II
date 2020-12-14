import pygame as pg
from main.settings import *
from random import choice, random
from tiles.collide import Collide


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB_HEALTH
        self.speed = choice(MOB_SPEEDS)
        self.target = game.player
        self.splat = pg.transform.scale(pg.image.load(path.join(img_folder, SPLAT)).convert_alpha(), (64, 64))
        self.collide = Collide(self, self.game.walls)

    # função para um mob evitar os outros
    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos

                # se outro mob estiver dentro do raio, um vetor de aceleração é posto contra ele
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        target_dist = self.target.pos - self.pos

        # lenght squared serve para evitar cálculos de raiz que são lentos
        if target_dist.length_squared() < DETECT_RADIUS ** 2:  # checa se o jogador está perto
            if random() < 0.002:
                choice(self.game.zombie_moan_sounds).play()

            # a função "angle to" encontra o angulo do eixo x até a posição do jogador
            # assim, podemos rotacionar a sprite do zumbi
            self.rot = target_dist.angle_to(vec(1, 0))
            self.image = pg.transform.rotate(pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha(), self.rot)

            self.rect.center = self.pos
            self.acc = vec(1, 0).rotate(-self.rot)

            self.avoid_mobs()
            if abs(self.acc.length()) >= 0.01:
                self.acc.scale_to_length(self.speed)

            self.acc += self.vel * -1  # restringe a velocidade máxima do mob
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            self.collide.collide_with_walls('x')
            self.hit_rect.centery = self.pos.y
            self.collide.collide_with_walls('y')
            self.rect.center = self.hit_rect.center
        if self.health <= 0:
            choice(self.game.zombie_hit_sounds).play()
            self.kill()
            self.game.map_img.blit(self.splat, self.pos - vec(32, 32))

    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / MOB_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < MOB_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)
