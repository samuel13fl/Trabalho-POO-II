import sys
from random import choice, random
import main.settings as settings
import pickle
from tiles.tilemap import *
from entity.player import Player
from entity.mob import Mob
from entity.ghost import Ghost
from tiles.obstacle import Obstacle
from items.weapon import *
from items.item import Item


class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 4, 2048)  # pre init seta os padrões quando mixer.init for chamado
        pg.init()  # inicializa o pygame
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))  # inicializa a tela
        pg.display.set_caption(TITLE)  # coloca o titulo na janela inicializada

        self.cursor = pg.image.load(path.join(img_folder, mouse)).convert_alpha()  # carrega a imagem do cursor

        self.clock = pg.time.Clock()  # clock do jogo
        self.load_data()  # função onde carregamos o necessário para o jogo rodar (especialmente sons e tela)

    # as três funções draw carregam a interface enquanto o  jogo roda
    def draw_text(self, text, font_name, size, color, x, y, align="topleft"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        self.screen.blit(text_surface, text_rect)

    def draw_player_health(self, pct):

        if pct < 0:
            pct = 0
        elif pct == 1:
            health = pg.image.load(path.join(img_folder, 'HEARTFULL.png')).convert_alpha()
        elif pct == 0.75:
            health = pg.image.load(path.join(img_folder, 'HEART3.png')).convert_alpha()
        elif pct == 0.50:
            health = pg.image.load(path.join(img_folder, 'HEART2.png')).convert_alpha()
        elif pct <= 0.25:
            health = pg.image.load(path.join(img_folder, 'HEART1.png')).convert_alpha()
        self.screen.blit(health, (10, 10))

    def draw_gun(self):

        weapon = pg.image.load(path.join(img_folder, self.player.weapon.sprite)).convert_alpha()
        self.screen.blit(weapon, (832, 640))

    # essa função foi feita para o jogador rodar junto com o mouse e fazer o mouse acompanhar o scroll da tela
    def mousepos_worldpos(self, mouse_pos):
        cam_pos = self.camera.camera.topleft
        return (mouse_pos[0] - cam_pos[0], mouse_pos[1] - cam_pos[1])


    def load_data(self):
        # carregando a tela
        pg.Surface(self.screen.get_size()).convert_alpha().fill((0, 0, 0, 180))  # preenche a tela com cor solida

        # Carregando os sons
        self.volume = 0.1
        pg.mixer.music.load(path.join(music_folder, BG_MUSIC))
        pg.mixer.music.set_volume(self.volume)
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[type]))
            s.set_volume(self.volume)
            self.effects_sounds[type] = s
        self.weapon_sounds = {}
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                s = pg.mixer.Sound(path.join(snd_folder, snd))
                s.set_volume(self.volume)
                self.weapon_sounds[weapon].append(s)
        self.zombie_moan_sounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(self.volume)
            self.zombie_moan_sounds.append(s)
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(self.volume)
            self.player_hit_sounds.append(s)
        self.zombie_hit_sounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(self.volume)
            self.zombie_hit_sounds.append(s)

    # Setup para um novo jogo
    def new(self):
        # Criando grupos de sprites

        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.mobslist = []
        self.ghostlist = []
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.itemslist = []

        # Usando a biblioteca Pytween para criar um mapa em tiles, usando o editor de mapas
        self.map = TiledMap(path.join(path.join(path.dirname(__file__), 'maps'), 'fase1.tmx'))
        self.map_img = self.map.make_map()
        self.map.rect = self.map_img.get_rect()

        # loop que lê os objetos posicionados no editor de mapas e cria eles
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)

            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'zombie':
                M = Mob(self, obj_center.x, obj_center.y)
                self.mobslist.append(M)
            if tile_object.name == 'ghost':
                G = Ghost(self, obj_center.x, obj_center.y)
                self.ghostlist.append(G)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name in ['health', 'shotgun', 'staff']:
                I = Item(self, obj_center, tile_object.name)
                self.itemslist.append(I)

        self.camera = Camera(self.map.width, self.map.height)
        self.paused = False

    def run(self):
        # loop do jogo
        self.playing = True
        pg.mixer.music.play(loops=-1)
        while True:
            self.dt = self.clock.tick(FPS) / 1000  # controla a velocidade do movimento das coisas
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
        # update loop
        self.all_sprites.update()
        self.camera.update(self.player) # centra a câmera no jogador

        # checa se é game over
        if len(self.mobs) == 0:
            self.playing = False

        # player colide com um item (o false diz que não é pra fazer o jogador desaparecer)
        hits = pg.sprite.spritecollide(self.player, self.items, False)  # retorna uma lista de items que colidem
        for hit in hits:
            if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
                self.itemslist.remove(hit)
                hit.kill()
                self.effects_sounds['health_up'].play()
                self.player.add_health(HEALTH_PACK_AMOUNT)
            if hit.type == 'shotgun':
                self.itemslist.remove(hit)
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapon = Shotgun()
            if hit.type == 'staff':
                self.itemslist.remove(hit)
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapon = 'staff'

        # mob colide com player. collide_hit_rect é uma função que checa isso, caso contrário deve passar o rect
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            if random() < 0.7:
                choice(self.player_hit_sounds).play()
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False

        if hits:
            self.player.hit()  # função que dá invincibility frames após levar um hit
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)  # essa linha é onde ocorre o knockback

        # bala colide com mob
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for mob in hits:
            for bullet in hits[mob]:
                mob.health -= bullet.damage
                if mob.health <= 0 and mob in self.mobslist:
                    self.mobslist.remove(mob)
                if mob.health <= 0 and mob in self.ghostlist:
                    self.ghostlist.remove(mob)
            mob.vel = vec(0, 0)

    # função que é chamada quando um novo jogo começa
    def draw(self):
        # titulo da janela
        pg.display.set_caption("GUNDALF THE WIZARD   {:.2f}".format(self.clock.get_fps()))

        # impede que o mouse use a imagem de cursor fora da tela de jogo rodando
        pg.mouse.set_visible(False)

        self.screen.blit(self.map_img, self.camera.apply(self.map))  # alinha a camera no canto correto

        self.screen.blit(self.cursor, (pg.mouse.get_pos()))  # desenha o cursor

        # desenha a barra de vida dos mobs
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        # interface, usa as funções draw
        self.draw_text('Enemies: {}'.format(len(self.mobs)),
                       path.join(path.join(path.dirname(__file__), 'img'), 'PressStart2P.ttf'),
                       30, WHITE,
                       WIDTH - 10, 10, align="topright")
        self.draw_gun()
        self.draw_player_health(self.player.health / PLAYER_HEALTH)
        pg.display.flip()

    # muda todos os volumes para o valor atual de self.volume
    def change_volume(self):
        for sound_type in self.weapon_sounds:
            self.weapon_sounds[sound_type][0].set_volume(self.volume)
        for sound_type in self.effects_sounds:
            self.effects_sounds[sound_type].set_volume(self.volume)
        for sound_type in self.zombie_moan_sounds:
            sound_type.set_volume(self.volume)
        for sound_type in self.player_hit_sounds:
            sound_type.set_volume(self.volume)
        for sound_type in self.zombie_hit_sounds:
            sound_type.set_volume(self.volume)
        pg.mixer.music.set_volume(self.volume)

    # desenha o volume na tela de opções
    def draw_volume(self):

        if self.volume == 1:
            volume = pg.image.load(path.join(img_folder, 'NUMBER100.png')).convert_alpha()
        elif 1 > self.volume >= 0.9:
            volume = pg.image.load(path.join(img_folder, 'NUMBER90.png')).convert_alpha()
        elif 0.9 > self.volume >= 0.8:
            volume = pg.image.load(path.join(img_folder, 'NUMBER80.png')).convert_alpha()
        elif 0.8 > self.volume >= 0.7:
            volume = pg.image.load(path.join(img_folder, 'NUMBER70.png')).convert_alpha()
        elif 0.7 > self.volume >= 0.6:
            volume = pg.image.load(path.join(img_folder, 'NUMBER60.png')).convert_alpha()
        elif 0.6 > self.volume >= 0.5:
            volume = pg.image.load(path.join(img_folder, 'NUMBER50.png')).convert_alpha()
        elif 0.5 > self.volume >= 0.4:
            volume = pg.image.load(path.join(img_folder, 'NUMBER40.png')).convert_alpha()
        elif 0.4 > self.volume >= 0.3:
            volume = pg.image.load(path.join(img_folder, 'NUMBER30.png')).convert_alpha()
        elif 0.3 > self.volume >= 0.2:
            volume = pg.image.load(path.join(img_folder, 'NUMBER20.png')).convert_alpha()
        elif 0.2 > self.volume >= 0.1:
            volume = pg.image.load(path.join(img_folder, 'NUMBER10.png')).convert_alpha()
        else:
            volume = pg.image.load(path.join(img_folder, 'NUMBER0.png')).convert_alpha()
        self.screen.blit(volume, (140, 140))
        pg.display.flip()

    # loop de eventos dentro do jogo
    def events(self):
        # eventos
        for event in pg.event.get():
            # fechar a janela
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                # apertar ESC para pausar
                if event.key == pg.K_ESCAPE:
                    self.show_pause_screen()

                # aumentar e diminuir o volume dentro de jogo
                if event.key == pg.K_EQUALS:
                    if self.volume >= 1:
                        self.volume = 1
                    else:
                        self.volume += 0.1
                    self.change_volume()
                if event.key == pg.K_MINUS:
                    if self.volume <= 0:
                        self.volume = 0
                    else:
                        self.volume -= 0.1

                    self.change_volume()

    def save(self):
        self.mobspos = []
        self.ghostpos = []
        self.itemspos = []
        for i in range(len(self.mobslist)):
            if isinstance(self.mobslist[i], Mob):
                self.mobspos.append(self.mobslist[i].pos)
        for i in range(len(self.ghostlist)):
            if isinstance(self.ghostlist[i], Ghost):
                self.ghostpos.append(self.ghostlist[i].pos)
        for item in self.itemslist:
            self.itemspos.append([item.pos, item.type])
        with open("savefile", "wb") as f:
            data = [[self.player.health, self.player.weapon, self.player.rect.center],
                    self.mobspos,
                    self.itemspos,
                    self.ghostpos]
            pickle.dump(data, f)

    def load(self):
        with open("savefile", "rb") as f:
            loaddata = pickle.load(f)
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.mobslist = []
        self.ghostlist = []
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.itemslist = []
        self.map = TiledMap(path.join(map_folder, 'Fase1.tmx'))
        self.map_img = self.map.make_map()
        self.map.rect = self.map_img.get_rect()

        self.player = Player(self, loaddata[0][2][0], loaddata[0][2][1])
        self.player.health = loaddata[0][0]
        self.player.weapon = loaddata[0][1]
        for zombie in loaddata[1]:
            M = Mob(self, zombie[0], zombie[1])
            self.mobslist.append(M)
        for ghost in loaddata[3]:
            G = Ghost(self, ghost[0], ghost[1])
            self.ghostlist.append(G)
        for item in loaddata[2]:
            I = Item(self, item[0], item[1])
            self.itemslist.append(I)
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)

        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False

    def show_pause_screen(self):
        self.paused = True
        pg.mouse.set_visible(True)
        self.current_screen = "Pause"
        self.screen.blit(pg.image.load(path.join(img_folder, settings.pausescreen)).convert_alpha(), (0, 0))
        self.button_pause_back = pg.Rect(416, 323, 192, 28)
        self.button_pause_save = pg.Rect(448, 436, 128, 28)
        self.button_pause_quit = pg.Rect(448, 565, 128, 28)
        pg.draw.rect(self.screen, (255, 0, 0), self.button_pause_back, -1)
        pg.draw.rect(self.screen, (255, 0, 0), self.button_pause_save, -1)
        pg.draw.rect(self.screen, (255, 0, 0), self.button_pause_quit, -1)
        pg.display.flip()
        self.wait_for_key()

    def show_start_screen(self):
        pg.mouse.set_visible(True)
        self.current_screen = "Start Screen"
        self.screen.blit(pg.image.load(path.join(img_folder, settings.mainscreen)).convert_alpha(), (0, 0))
        self.button_start_start = pg.Rect(68, 204, 220, 30)
        self.button_start_option = pg.Rect(64, 340, 190, 35)
        self.button_start_load = pg.Rect(68, 465, 125, 30)
        self.button_start_quit = pg.Rect(63, 596, 130, 30)
        pg.draw.rect(self.screen, (0, 0, 0), self.button_start_start, -1)
        pg.draw.rect(self.screen, (0, 0, 0), self.button_start_load, -1)
        pg.draw.rect(self.screen, (0, 0, 0), self.button_start_option, -1)
        pg.draw.rect(self.screen, (0, 0, 0), self.button_start_quit, -1)
        pg.display.flip()
        pg.mixer.music.pause()
        self.wait_for_key()

    def show_victoryscreen(self):
        pg.mouse.set_visible(True)
        self.current_screen = "victoryscreen"
        self.screen.blit(pg.image.load(path.join(img_folder, settings.victoryscreen)).convert_alpha(), (0, 0))
        self.button_go_restart = pg.Rect(100, 703, 288, 33)
        self.button_go_quit = pg.Rect(640, 706, 192, 28)
        pg.draw.rect(self.screen, (255, 0, 0), self.button_go_restart, -1)
        pg.draw.rect(self.screen, (255, 0, 0), self.button_go_quit, -1)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        pg.mouse.set_visible(True)
        self.current_screen = "Game Over Screen"
        self.screen.blit(pg.image.load(path.join(img_folder, settings.gameoverscreen)).convert_alpha(), (0, 0))
        self.button_go_restart = pg.Rect(156, 666, 289, 32)
        self.button_go_quit = pg.Rect(694, 666, 192, 29)
        pg.draw.rect(self.screen, (255, 0, 0), self.button_go_restart, -1)
        pg.draw.rect(self.screen, (255, 0, 0), self.button_go_quit, -1)
        pg.display.flip()
        self.wait_for_key()

    def options(self):
        pg.mouse.set_visible(True)
        self.current_screen = "Options Screen"
        self.screen.blit(pg.image.load(path.join(img_folder, settings.optionscreen)).convert_alpha(), (0, 0))
        self.button_options_return = pg.Rect(336, 480, 385, 57)
        self.button_options_volumeup = pg.Rect(744, 80, 40, 72)
        self.button_options_volumedown = pg.Rect(272, 80, 40, 72)
        pg.draw.rect(self.screen, (0, 0, 0), self.button_options_return, -1)
        pg.draw.rect(self.screen, (255, 0, 0), self.button_options_volumeup, -1)
        pg.draw.rect(self.screen, (255, 0, 0), self.button_options_volumedown, -1)
        self.draw_volume()
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
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE and self.current_screen == "Pause":
                        self.paused = False
                        self.current_screen = ''
                        waiting = False
                        pg.mouse.set_visible(True)
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click_test = True
            mx, my = pg.mouse.get_pos()
            if self.click_test:
                if self.current_screen == "Pause":
                    if self.button_pause_back.collidepoint((mx, my)):
                        self.paused = False
                        self.current_screen = ''
                        waiting = False

                    elif self.button_pause_save.collidepoint((mx, my)):
                        g.save()
                    elif self.button_pause_quit.collidepoint((mx, my)):
                        g.show_start_screen()

                elif self.current_screen == "victoryscreen":
                    if self.button_go_restart.collidepoint((mx, my)):
                        g.new()
                        g.run()

                    elif self.button_go_quit.collidepoint((mx, my)):
                        g.show_start_screen()

                elif self.current_screen == "Game Over Screen":
                    if self.button_go_restart.collidepoint((mx, my)):
                        g.new()
                        g.run()

                    elif self.button_go_quit.collidepoint((mx, my)):
                        g.show_start_screen()

                elif self.current_screen == "Start Screen":
                    if self.button_start_start.collidepoint((mx, my)):
                        g.new()
                        g.run()

                    elif self.button_start_option.collidepoint((mx, my)):
                        g.options()

                    elif self.button_start_load.collidepoint((mx, my)):
                        g.load()
                        g.run()

                    elif self.button_start_quit.collidepoint((mx, my)):
                        self.quit()

                elif self.current_screen == "Options Screen":
                    if self.button_options_return.collidepoint((mx, my)):
                        g.show_start_screen()

                    elif self.button_options_volumeup.collidepoint((mx, my)):
                        if self.volume >= 1:
                            self.volume = 1
                        else:
                            self.volume += 0.1

                        self.change_volume()
                        self.screen.blit(pg.image.load(path.join(img_folder, settings.optionscreen)).convert_alpha(),
                                         (0, 0))
                        self.draw_volume()

                    elif self.button_options_volumedown.collidepoint((mx, my)):
                        if self.volume <= 0:
                            self.volume = 0
                        else:
                            self.volume -= 0.1

                        self.change_volume()
                        self.screen.blit(pg.image.load(path.join(img_folder, settings.optionscreen)).convert_alpha(),
                                         (0, 0))
                        self.draw_volume()

            self.click_test = False


g = Game()
g.show_start_screen()
