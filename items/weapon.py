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
