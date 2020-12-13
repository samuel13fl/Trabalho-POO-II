import pygame as pg
from random import uniform, choice, randint, random
from settings import *
from tilemap import collide_hit_rect
from tilemap import Camera
import pytweening as tween
from itertools import chain
import math

vec = pg.math.Vector2


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


class Ghost(Mob):  # funciona igual o zumbi, mas sem a colisão com paredes
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.health = 1
        self.speed = 1000

    def update(self):
        target_dist = self.target.pos - self.pos
        if target_dist.length_squared() < DETECT_RADIUS ** 2:
            if random() < 0.002:
                choice(self.game.zombie_moan_sounds).play()
            self.rot = target_dist.angle_to(vec(1, 0))
            self.image = pg.transform.rotate(pg.image.load(path.join(img_folder, GHOST_IMG)).convert_alpha(), self.rot)
            self.rect.center = self.pos
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            if abs(self.acc.length()) >= 0.01:
                self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            self.hit_rect.centery = self.pos.y
            self.rect.center = self.hit_rect.center
        if self.health <= 0:
            choice(self.game.zombie_hit_sounds).play()
            self.kill()
            self.game.map_img.blit(self.splat, self.pos - vec(32, 32))


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


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


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


class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = type
        self.image = self.create_image()
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.step = 0
        self.dir = 1

    def create_image(self):
        item_images = {}
        for item in ITEM_IMAGES:
            item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()
        return item_images[self.type]


class Weapon:
    def __init__(self, bullet_speed, bullet_lifetime, rate, kickback, spread, damage, size, count):
        self.bullet_speed = bullet_speed
        self.bullet_lifetime = bullet_lifetime
        self.rate = rate
        self.kickback = kickback
        self.spread = spread
        self.damage = damage
        self.bullet_size = size
        self.bullet_count = count


class Pistol(Weapon):
    def __init__(self, bullet_speed=500, bullet_lifetime=1000, rate=250, kickback=200, spread=5, damage=10,
                 size='lg',
                 count=1):
        super().__init__(bullet_speed, bullet_lifetime, rate, kickback, spread, damage, size, count)
        self.name = 'pistol'
        self.sprite = 'PISTOLFRAME.png'


class Shotgun(Weapon):
    def __init__(self, bullet_speed=400, bullet_lifetime=500, rate=900, kickback=300, spread=50, damage=5,
                 size='sm',
                 count=20):
        super().__init__(bullet_speed, bullet_lifetime, rate, kickback, spread, damage, size, count)
        self.name = 'shotgun'
        self.sprite = 'SHOTGUNBIG.png'
