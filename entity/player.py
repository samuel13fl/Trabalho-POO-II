from main.settings import *
from tiles.collide import Collide
import math
from items.bullet import Bullet
from items.shot import Shot
from items.weapon import *
from random import choice, uniform
from itertools import chain


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self, game.all_sprites)
        self.game = game
        self.image = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()

        # criando a imagem e centro da sprite
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # o jogador terá dois retângulos, um para colisão e um para a imagem
        # isso é importante pois quando a sprite é rotacionada, o tamanho do retângulo dela muda
        # o hit_rect tem tamanho fixo, então funciona melhor para detectar colisões
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center

        self.vel = vec(0, 0)  # velocidade inicial do jogador (vec é pra fazer um vetor)
        self.pos = vec(x, y)  # posição inicial do jogador

        self.rot = 0  # valor que define o quanto a sprite será rotacionada

        self.last_shot = 0  # importante para definir o fire rate do jogador
        self.health = PLAYER_HEALTH
        self.weapon = Pistol()
        self.damaged = False  # importante na função dos invincibility frames
        self.collide = Collide(self, self.game.walls)  # classe que vai fazer a colisão

    # função que define o que é feito em cada comando do jogador. Mover e e atirar
    def get_keys(self):
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

    #  rotaciona a sprite de acordo com a posição do mouse
    def rotate(self):
        mouse_pos_x, mouse_pos_y = self.game.mousepos_worldpos(pg.mouse.get_pos())
        rel_x = mouse_pos_x - self.pos.x
        rel_y = mouse_pos_y - self.pos.y
        angle = -math.degrees(math.atan2(rel_y, rel_x))
        self.rot = angle
        self.rect = self.image.get_rect(center=self.rect.center)

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.weapon.rate:  # checa se o tempo atual é maior que o tempo após o ultimo tiro
            self.last_shot = now
            dir = vec(1, 0).rotate(-self.rot)  # definindo a direção da bala, mesma rotação que o jogador
            pos = self.pos + BARREL_OFFSET.rotate(-self.rot)  # spawnando a bala na mão do jogador, usando offset
            self.vel = vec(-self.weapon.kickback, 0).rotate(-self.rot)  # recuo do jogador em cada tiro
            for i in range(self.weapon.bullet_count):

                # uniform retorna um número entre os dois que foram passados
                spread = uniform(-self.weapon.spread, self.weapon.spread)  # escolhendo aleatoriamente o spread
                Bullet(self.game, pos, dir.rotate(spread), self.weapon.damage)
                snd = choice(self.game.weapon_sounds[self.weapon.name])
                if snd.get_num_channels() > 2:
                    snd.stop()
                snd.play()

            # shot é o efeito que aparace em cada tiro, spawna na mesma posição que a bala
            Shot(self.game, pos)

    # função que pisca o jogador quando ele tomar um hit
    def hit(self):
        self.damaged = True
        # damage alpha é uma corrente de valores de cor que aumentam gradualmente
        self.damage_alpha = chain(DAMAGE_ALPHA * 4)

    def update(self):
        self.rotate()
        self.get_keys()

        # criamos uma imagem temporária para rotacionar, fazer isso direto na do jogador distorce ela
        temp = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.image = pg.transform.rotate(temp, self.rot)

        # faz o jogador piscar quando toma um hit (self.damage é setado na função hit)
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

    # restora a vida quando o jogador pega uma poção
    def add_health(self, amount):
        self.health += amount
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH
