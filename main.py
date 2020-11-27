import pygame as pg
import sys
from random import choice, random
from os import path
import settings
from sprites import *
from tilemap import *

# HUD functions

def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 4, 2048)
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        self.load_menus()

    def draw_gun(self):
        while self.playing:
            pg.screen.blit()

    def draw_text(self, text, font_name, size, color, x, y, align="topleft"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        self.screen.blit(text_surface, text_rect)

    def mousepos_worldpos(self,mouse_pos):
        cam_pos = self.camera.camera.topleft
        return (mouse_pos[0] - cam_pos[0] , mouse_pos[1] - cam_pos[1]) # fazendo com que a posição do mouse seja a do mundo

    def load_menus(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        snd_folder = path.join(game_folder, 'snd')
        music_folder = path.join(game_folder, 'music')

        self.mainscreen = pg.image.load(path.join(img_folder, settings.mainscreen)).convert_alpha()
        self.gameoverscreen = pg.image.load(path.join(img_folder, settings.gameoverscreen)).convert_alpha()
        self.optionscreen = pg.image.load(path.join(img_folder, settings.optionscreen)).convert_alpha()
        self.pausescreen = pg.image.load(path.join(img_folder, settings.pausescreen)).convert_alpha()
        self.victoryscreen = pg.image.load(path.join(img_folder, settings.victoryscreen)).convert_alpha()
    
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        snd_folder = path.join(game_folder, 'snd')
        music_folder = path.join(game_folder, 'music')

        self.map_folder = path.join(game_folder, 'maps')
        self.title_font = path.join(img_folder, 'ZOMBIE.TTF')
        self.hud_font = path.join(img_folder, 'Impacted2.0.ttf')
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.bullet_images = {}
        self.bullet_images['lg'] = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.bullet_images['sm'] = pg.transform.scale(self.bullet_images['lg'], (10, 10))
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.splat = pg.image.load(path.join(img_folder, SPLAT)).convert_alpha()
        self.splat = pg.transform.scale(self.splat, (64, 64))
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()
        # lighting effect
        self.fog = pg.Surface((WIDTH, HEIGHT))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask = pg.image.load(path.join(img_folder, LIGHT_MASK)).convert_alpha()
        self.light_mask = pg.transform.scale(self.light_mask, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()
        # Sound loading
        pg.mixer.music.load(path.join(music_folder, BG_MUSIC))
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type] = pg.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[type]))
        self.weapon_sounds = {}
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                s = pg.mixer.Sound(path.join(snd_folder, snd))
                s.set_volume(0.3)
                self.weapon_sounds[weapon].append(s)
        self.zombie_moan_sounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(0.2)
            self.zombie_moan_sounds.append(s)
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            self.player_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))
        self.zombie_hit_sounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            self.zombie_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.map = TiledMap(path.join(self.map_folder, 'TesteFase1.tmx'))
        self.map_img = self.map.make_map()
        self.map.rect = self.map_img.get_rect()
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width/2, tile_object.y + tile_object.height/2)

            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)  
            if tile_object.name == 'zombie':
                Mob(self, obj_center.x, obj_center.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name in ['health', 'shotgun','staff']:
                Item(self, obj_center, tile_object.name)

        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False
        self.night = False
        self.effects_sounds['level_start'].play()

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        pg.mixer.music.play(loops=-1)
        while True:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            if not self.paused:
                self.update()
            self.draw()
            if not self.playing:
                if len(self.mobs) == 0:
                    self.show_victoryscreen()
                else:
                    self.show_go_screen()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        # game over?
        if len(self.mobs) == 0:
            self.playing = False
        # player hits items
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.effects_sounds['health_up'].play()
                self.player.add_health(HEALTH_PACK_AMOUNT)
            if hit.type == 'shotgun':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapon = 'shotgun'
            if hit.type == 'staff':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapon = 'staff'
        # mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            if random() < 0.7:
                choice(self.player_hit_sounds).play()
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.hit()
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        # bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for mob in hits:
            # hit.health -= WEAPONS[self.player.weapon]['damage'] * len(hits[hit])
            for bullet in hits[mob]:
                mob.health -= bullet.damage
            mob.vel = vec(0, 0)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def render_fog(self):
        # draw the light mask (gradient) onto fog image
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center = self.camera.apply(self.player).center
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply(self.map))
        # self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)

        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        if self.night:
            self.render_fog()
        # HUD functions
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        self.draw_text('Zombies: {}'.format(len(self.mobs)), self.hud_font, 30, WHITE,
                       WIDTH - 10, 10, align="topright")
        #comeco
        
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_ESCAPE:
                    self.show_pause_screen() 
                if event.key == pg.K_n:
                    self.night = not self.night
               
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 0:
                    self.click = True
                if event.button == 1:
                    self.click = False
            
    #arrumar ainda

    def show_pause_screen(self):
        self.paused = True
        self.current_screen = "Pause"
        self.screen.blit(self.pausescreen, (0, 0))
        self.button_pause_back = pg.Rect(400, 300, 200, 50)
        self.button_pause_save = pg.Rect(400, 400, 200, 50)
        self.button_pause_quit = pg.Rect(400, 500, 200, 50)
        pg.draw.rect(self.screen, (255, 0, 0), self.button_pause_back,1)
        pg.draw.rect(self.screen, (255, 0, 0), self.button_pause_save,1)
        pg.draw.rect(self.screen, (255, 0, 0), self.button_pause_quit,1)
        pg.display.flip()
        self.wait_for_key()

    def show_start_screen(self):
        self.current_screen = "Start Screen"
        self.screen.blit(self.mainscreen,(0,0))
        self.button_start_start = pg.Rect(68, 204, 220, 30)
        self.button_start_option = pg.Rect(64, 340, 190, 35)
        self.button_start_load = pg.Rect(68, 465, 125, 30)
        self.button_start_quit = pg.Rect(63, 596, 130, 30)
        pg.draw.rect(self.screen, (0, 0, 0), self.button_start_start,-1)
        pg.draw.rect(self.screen, (0, 0, 0), self.button_start_load,-1)
        pg.draw.rect(self.screen, (0, 0, 0), self.button_start_option,-1)
        pg.draw.rect(self.screen, (0, 0, 0), self.button_start_quit,-1)
        pg.display.flip()
        pg.mixer.music.pause()
        self.wait_for_key()
    
    def show_victoryscreen(self):
        self.current_screen = "victoryscreen"
        self.screen.blit(self.victoryscreen,(0,0))
        self.button_go_restart = pg.Rect(156, 666, 289, 32)
        self.button_go_quit = pg.Rect(694, 666, 192, 29)
        pg.draw.rect(self.screen, (255, 0, 0), self.button_go_restart)
        pg.draw.rect(self.screen, (255, 0, 0), self.button_go_quit)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        self.current_screen = "Game Over Screen"
        self.screen.blit(self.gameoverscreen,(0,0))
        self.button_go_restart = pg.Rect(156, 666, 289, 32 )
        self.button_go_quit = pg.Rect(694, 666, 192, 29)
        pg.draw.rect(self.screen, (255, 0, 0), self.button_go_restart,-1)
        pg.draw.rect(self.screen, (255, 0, 0), self.button_go_quit,-1)
        pg.display.flip()
        self.wait_for_key()

    def options(self):
        self.current_screen = "Options Screen"
        self.screen.blit(self.optionscreen,(0,0))
        self.button_options_return = pg.Rect(336, 480, 385, 57)
        self.button_options_volumeup = pg.Rect(744, 80, 40, 72)
        self.button_options_volumedown = pg.Rect(272, 80, 40, 72)
        pg.draw.rect(self.screen, (0, 0, 0), self.button_options_return,-1)
        pg.draw.rect(self.screen, (255, 0, 0), self.button_options_volumeup,1)
        pg.draw.rect(self.screen, (255, 0, 0), self.button_options_volumedown,1)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        self.click_test = False
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click_test = True
            mx, my = pg.mouse.get_pos()

            if self.current_screen == "Pause" and self.button_pause_back.collidepoint((mx, my)):
                if self.click_test:
                    self.paused = False
                    self.current_screen = ''
                    waiting = False

            if self.current_screen == "Pause" and self.button_pause_save.collidepoint((mx, my)):
                if self.click_test:
                    pass 

            if self.current_screen == "Pause" and self.button_pause_quit.collidepoint((mx, my)):
                if self.click_test:
                    g.show_start_screen()
                    
            if self.current_screen == "victoryscreen" and self.button_go_restart.collidepoint((mx, my)):
                if self.click_test:
                    g.new()
                    g.run()
                    

            if self.current_screen == "victoryscreen" and self.button_go_quit.collidepoint((mx, my)):
                if self.click_test:
                    g.show_start_screen()

            if self.current_screen == "Game Over Screen" and self.button_go_restart.collidepoint((mx, my)):
                if self.click_test:
                    g.new()
                    g.run()
                   

            if self.current_screen == "Game Over Screen" and self.button_go_quit.collidepoint((mx, my)):
                if self.click_test:
                    g.show_start_screen()

            if self.current_screen == "Start Screen" and self.button_start_start.collidepoint((mx, my)):
                if self.click_test:
                    g.new()
                    g.run()

            if self.current_screen == "Start Screen" and self.button_start_option.collidepoint((mx, my)):
                if self.click_test:
                    g.options()

            if self.current_screen == "Start Screen" and self.button_start_quit.collidepoint((mx, my)):
                if self.click_test:
                    self.quit()
        
            if self.current_screen == "Options Screen" and self.button_options_return.collidepoint((mx, my)):
                if self.click_test:
                    g.show_start_screen()

            if self.current_screen == "Options Screen" and self.button_options_volumeup.collidepoint((mx, my)):
                if self.click_test:
                    for sound_type in self.weapon_sounds:
                        self.weapon_sounds[sound_type][0].set_volume(self.weapon_sounds[sound_type][0].get_volume() + 0.1)
                    for sound_type in self.effects_sounds:
                        self.effects_sounds[sound_type].set_volume(self.effects_sounds[sound_type].get_volume() + 0.1)
                    for sound_type in self.zombie_moan_sounds:
                        sound_type.set_volume(sound_type.get_volume() + 0.1)
                    for sound_type in self.player_hit_sounds:
                        sound_type.set_volume(sound_type.get_volume() + 0.1)
                    for sound_type in self.zombie_hit_sounds:
                        sound_type.set_volume(sound_type.get_volume() + 0.1)
                    pg.mixer.music.set_volume(pg.mixer.music.get_volume() + 0.1)
                    print(pg.mixer.music.get_volume())

            if self.current_screen == "Options Screen" and self.button_options_volumedown.collidepoint((mx, my)):
                if self.click_test:
                    for sound_type in self.weapon_sounds:
                        self.weapon_sounds[sound_type][0].set_volume(self.weapon_sounds[sound_type][0].get_volume() - 0.1)
                    for sound_type in self.effects_sounds:
                        self.effects_sounds[sound_type].set_volume(self.effects_sounds[sound_type].get_volume() - 0.1)
                    for sound_type in self.zombie_moan_sounds:
                        sound_type.set_volume(sound_type.get_volume() - 0.1)
                    for sound_type in self.player_hit_sounds:
                        sound_type.set_volume(sound_type.get_volume() - 0.3)
                    for sound_type in self.zombie_hit_sounds:
                        sound_type.set_volume(sound_type.get_volume() - 0.3)
                    pg.mixer.music.set_volume(pg.mixer.music.get_volume() - 0.1)
                    print(pg.mixer.music.get_volume())
            self.click_test = False

# create the game object
g = Game()
g.show_start_screen()