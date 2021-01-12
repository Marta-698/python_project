import pygame
import os
import sys

pygame.init()
size = WIDTH, HEIGHT = 1920, 1000
pygame.display.set_caption('Платформер')
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
FPS = 60


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


tile_images = {}
tile_width = tile_height = 16


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def start_click(pos):
    x, y = pos
    player = None
    if 300 <= y <= 665:
        # if 224 <= x <= 424:
        #    player = Player(20, 20, 1)
        #    player.cut_sheet('idle')
        # elif 610 <= x <= 790:
        # player = Player()
        # elif 1050 <= x <= 1250:
        #   player = Player()
        # elif 1500 <= x <= 1690:
        #   player = Player()
        return player is not None


def start_screen():
    fon = pygame.transform.scale(load_image('field.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    MainStartText()
    ChooseStartText()
    Player(-276, -100, 1)
    Player(400, 150, 2)
    Player(572, -60, 3)
    Player(996, -90, 4)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_click(event.pos):
                    return
        screen.blit(fon, (0, 0))
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(10)


class MainStartText(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = load_image('mainstarttext.png')
        self.rect = self.image.get_rect().move(WIDTH // 2 - 450, 0)


class ChooseStartText(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = load_image('startchoose.png')
        self.rect = self.image.get_rect().move(WIDTH // 2 - 300, 155)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, n):
        super().__init__(player_group, all_sprites)
        self.x, self.y, self.n = x, y, n
        if self.n == 1:
            self.a, self.b, self.c, self.d, self.e, self.f, self.g = 8, 8, 2, 2, 4, 4, 6
        elif self.n == 2:
            self.a, self.b, self.c, self.d, self.e, self.f, self.g = 6, 8, 2, 2, 6, 4, 11
        elif self.n == 3:
            self.a, self.b, self.c, self.d, self.e, self.f, self.g = 8, 8, 2, 2, 6, 4, 6
        elif self.n == 4:
            self.a, self.b, self.c, self.d, self.e, self.f, self.g = 4, 8, 2, 2, 4, 3, 6
        self.frames = []
        self.cut_sheet('idlebig')
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]

    def cut_sheet(self, status):
        columns = None
        width = height = 0
        string = 0
        self.frames = []
        if status == 'idlebig':
            if self.n == 1 or self.n == 3:
                width, height = 9600, 1200
            elif self.n == 2:
                width, height = 4182, 697
            else:
                width, height = 4800, 1200
            string = 'Idle'
            columns = self.a
        if status == 'idle':
            string = 'Idle'
            columns = self.a
        sheet = pygame.transform.scale(load_image(f'{self.n}{string}.png'), (width, height))
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height()).move(self.x, self.y)
        for i in range(columns):
            frame_location = (self.rect.w * i, 0)
            self.frames.append(sheet.subsurface(pygame.Rect(
                frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


def generate_level(level):
    new_player, x, y, pos_x, pos_y = None, None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                pos_x, pos_y = x, y
    new_player = Player(pos_x, pos_y, 1)
    return new_player, x, y, level


start_screen()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    pygame.display.flip()
    clock.tick(FPS)
