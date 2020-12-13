import pygame as pg
from os import path
vec = pg.math.Vector2


# folders
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'img')
snd_folder = path.join(game_folder, 'snd')
music_folder = path.join(game_folder, 'music')
map_folder = path.join(game_folder, 'maps')

# Atalhos para Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60

TITLE = "GUNDALF THE WIZARD"
BGCOLOR = BROWN
mainscreen = 'TITLESCREEN2.png'
optionscreen = 'OPTIONSCREEN1.png'
gameoverscreen = 'GAMEOVER2.png'
pausescreen = 'pausescreen2.png'
victoryscreen = 'VICTORY.png'

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Jogador
PLAYER_HEALTH = 100
PLAYER_SPEED = 280
PLAYER_ROT_SPEED = 200
PLAYER_IMG = 'GUNDALF.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(30, 10)
mouse = 'cursor.png'
# Arma
BULLET_IMG = 'bullet.png'
WEAPONS = {}

# Mob

MOB_IMG = 'ZOMBIE.png'
GHOST_IMG = 'GHOST.png'
MOB_SPEEDS = [200, 150]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 25
MOB_KNOCKBACK = 20
AVOID_RADIUS = 50
DETECT_RADIUS = 500

# Effects
SHOTS = ['shot1.png', 'shot2.png']
SPLAT = 'blood-splat.png'
FLASH_DURATION = 50
DAMAGE_ALPHA = [i for i in range(0, 255, 55)]

# Itens
ITEM_IMAGES = {'pistol' : 'SHOTGUN.png',
               'health': 'HEALTH.png',
               'shotgun': 'SHOTGUN.png',
               'staff': 'staff.png'}
HEALTH_PACK_AMOUNT = 50
BOB_RANGE = 10
BOB_SPEED = 0.3
# Sons
BG_MUSIC = 'music-background.ogg'
PLAYER_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav', 'pain/12.wav', 'pain/13.wav']
ZOMBIE_MOAN_SOUNDS = ['zombie-roar-1.wav', 'zombie-roar-2.wav',
                      'zombie-roar-3.wav', 'zombie-roar-4.wav', 'zombie-roar-5.wav', 'zombie-roar-6.wav', 'zombie-roar-7.wav']
ZOMBIE_HIT_SOUNDS = ['splat-zumbi.wav']
WEAPON_SOUNDS = {'pistol': ['pistol.wav'],
                 'shotgun': ['shotgun.wav'],
                 'staff': ['shotgun.wav']}
EFFECTS_SOUNDS = {'health_up': 'health_pack.wav', 'gun_pickup': 'gun_pickup.wav'}

# função que checa se duas sprites estão colidindo
def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)