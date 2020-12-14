from main.settings import *
from random import choice, random
from tiles.collide import Collide
from entity.mob import Mob


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