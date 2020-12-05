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
WEAPONS['pistol'] = {'bullet_speed': 500,
                     'bullet_lifetime': 1000,
                     'rate': 250,
                     'kickback': 200,
                     'spread': 5,
                     'damage': 10,
                     'bullet_size': 'lg',
                     'bullet_count': 1}
                     
                     
WEAPONS['shotgun'] = {'bullet_speed': 400,
                      'bullet_lifetime': 500,
                      'rate': 900,
                      'kickback': 300,
                      'spread': 50,
                      'damage': 5,
                      'bullet_size': 'sm',
                      'bullet_count': 20}
                     

WEAPONS['staff'] = {'bullet_speed': 1,
                      'bullet_lifetime': 1500,
                      'rate': 900,
                      'kickback': 1,
                      'spread': 1,
                      'damage': 5,
                      'bullet_size': 'lg',
                      'bullet_count': 50}
                      

spriteweapon = {'pistol' : 'PISTOLFRAME.png',
                'shotgun': 'SHOTGUNBIG.png',
                'staff' : 'staff.png'}
# Mob

MOB_IMG = 'ZOMBIE.png'
MOB_SPEEDS = [100, 100, 100, 100]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 25
MOB_KNOCKBACK = 20
AVOID_RADIUS = 50
DETECT_RADIUS = 500

# Effects
MUZZLE_FLASHES = ['whitePuff15.png', 'whitePuff16.png', 'whitePuff17.png',
                  'whitePuff18.png']
SPLAT = 'splat green.png'
FLASH_DURATION = 50
NIGHT_COLOR = (20, 20, 20)
LIGHT_RADIUS = (900, 900)
LIGHT_MASK = "light_350_med.png"
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
BG_MUSIC = 'espionage.ogg'
PLAYER_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav']
ZOMBIE_MOAN_SOUNDS = ['brains2.wav', 'brains3.wav', 'zombie-roar-1.wav', 'zombie-roar-2.wav',
                      'zombie-roar-3.wav', 'zombie-roar-5.wav', 'zombie-roar-6.wav', 'zombie-roar-7.wav']
ZOMBIE_HIT_SOUNDS = ['splat-15.wav']
WEAPON_SOUNDS = {'pistol': ['pistol.wav'],
                 'shotgun': ['shotgun.wav'],
                 'staff': ['shotgun.wav']}
EFFECTS_SOUNDS = {'level_start': 'level_start.wav',
                  'health_up': 'health_pack.wav',
                  'gun_pickup': 'gun_pickup.wav'}