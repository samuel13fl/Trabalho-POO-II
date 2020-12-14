import pytmx
from main.settings import *


class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)  # carrega um arquivo .tmx (pixelapha pra ter transparencia)
        self.width = tm.width * tm.tilewidth  # largura e altura do mapa
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    # essa função desenha as tiles na superfície do pygame
    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid  # recebe cada tile com a imagem correspondente a ela
        for layer in self.tmxdata.visible_layers:  # layers que estão visíveis no editor de mapas
            if isinstance(layer, pytmx.TiledTileLayer):  # checa se é uma Tile e não um objeto
                for x, y, gid, in layer:  # gid é o que define a imagem de cada tile, o "id" dela
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))

    # função que será chamada no main para criar a superficie e desenhar o mapa nela
    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface


class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    # função usada para mover uma sprite de acordo com a câmera
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    # atualiza a câmera de acordo com o jogador, que é o target passado aqui
    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # criando limites para o scroll da câmera
        # lembrando que a câmera vai para o lado contrário do movimento do jogador, ou seja
        # quando o jogador vai para a direita, a posição x da câmera diminui e vice versa
        # então x tem que receber o mínimo entre ele mesmo e 0 para nunca ser negativo
        # a mesma lógica vale para a outra coordenada e também precisamos fazer o máximo delas
        # a camera está definida em "topleft" então o mínimo tem que ser 0 na esquerda e topo
        # e o máximo deve ser a diferença entre tamanho da câmera e tamanho total para direita e baixo
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)
        self.camera = pg.Rect(x, y, self.width, self.height)
