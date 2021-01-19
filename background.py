import pygame
import os
import sys
import random

pygame.init()
size = WIDTH, HEIGHT = 1920, 1000
pygame.display.set_caption('Платформер')
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
start_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
playerRect_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
FPS = 60
V = 15
JUMP_POWER = 10
GRAVITY = 0.35


def terminate():  # Остановка программы
    pygame.quit()
    sys.exit()


def load_image(name, place=1, colorkey=None):  # Загрузка изображения из различных папок
    if place == 1:
        fullname = os.path.join('data', name)
    elif place == 2:
        fullname = os.path.join('data/tileset', name)
    else:
        fullname = os.path.join('data/sprites', name)
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


tile_images = {  # Тайлы и декорации
    'S': load_image('1_stone.png', 2),
    'W': load_image('3_stones.png', 2),
    'big_bricks': load_image('big_bricks.png', 3),
    'big_crate': load_image('big_crate.png', 3),
    'big_grass': load_image('big_grass.png', 3),
    'big_spiral': load_image('big_spiral.png', 3),
    'B': load_image('black.png', 2),
    'block_big': load_image('block_big.png', 3),
    'R': load_image('bricks.png', 2),
    'b': load_image('brown.png', 2),
    'bush.png': load_image('bush.png', 3),
    'closet': load_image('closet.png', 3),
    'crank_down': load_image('crank_down.png', 3),
    'crank_up': load_image('crank_up.png', 3),
    'C': load_image('crate.png', 2),
    'k': load_image('dirt.png', 2),
    'door': load_image('door.png', 3),
    'm': load_image('down_dirt.png', 2),
    'x': load_image('down_plate.png', 2),
    'face_block': load_image('face_block.png', 3),
    'front_stump': load_image('front_stump.png', 3),
    'grass_1': load_image('grass_1.png', 3),
    'grass_2': load_image('grass_2.png', 3),
    'grass_3': load_image('grass_3.png', 3),
    'grass_4': load_image('grass_4.png', 3),
    'grass_5': load_image('grass_5.png', 3),
    'g': load_image('green.png', 2),
    'green_bricks': load_image('green_bricks.png', 3),
    '1': load_image('ground_1.png', 2),
    '2': load_image('ground_2.png', 2),
    '3': load_image('ground_3.png', 2),
    '4': load_image('ground_4.png', 2),
    '5': load_image('ground_5.png', 2),
    '6': load_image('ground_6.png', 2),
    '7': load_image('ground_7.png', 2),
    '8': load_image('ground_8.png', 2),
    '9': load_image('ground_9.png', 2),
    '0': load_image('ground_10.png', 2),
    '-': load_image('ground_11.png', 2),
    'house': load_image('house.png', 3),
    'L': load_image('ladder.png', 2),
    'left_big_climb_dirt': load_image('left_big_climb_dirt.png', 3),
    'left_big_climb_green': load_image('left_big_climb_green.png', 3),
    'left_big_platform': load_image('left_big_platform.png', 3),
    'left_branch': load_image('left_branch.png', 3),
    'left_column': load_image('left_column.png', 3),
    'left_corner': load_image('left_corner.png', 3),
    'j': load_image('left_dirt.png', 2),
    'n': load_image('left_down_dirt.png', 2),
    'z': load_image('left_down_plate.png', 2),
    'f': load_image('left_green.png', 2),
    'left_green_decor': load_image('left_green_decor.png', 3),
    'a': load_image('left_plate.png', 2),
    'left_small_climb_dirt': load_image('left_small_climb_dirt.png', 3),
    'left_small_climb_green': load_image('left_small_climb_green.png', 3),
    'left_small_platform': load_image('left_small_platform.png', 3),
    'r': load_image('left_up_green.png', 2),
    'q': load_image('left_up_plate.png', 2),
    'platform_long': load_image('platform_long.png', 3),
    'right_big_climb_dirt': load_image('right_big_climb_dirt.png', 3),
    'right_big_climb_green': load_image('right_big_climb_green.png', 3),
    'right_big_platform': load_image('right_big_platform.png', 3),
    'right_branch': load_image('right_branch.png', 3),
    'right_column': load_image('right_column.png', 3),
    'right_corner': load_image('right_corner.png', 3),
    'l': load_image('right_dirt.png', 2),
    ',': load_image('right_down_dirt.png', 2),
    'c': load_image('right_down_plate.png', 2),
    'h': load_image('right_green.png', 2),
    'right_green_decor': load_image('right_green_decor.png', 3),
    'd': load_image('right_plate.png', 2),
    'right_small_climb_dirt': load_image('right_small_climb_dirt.png', 3),
    'right_small_climb_green': load_image('right_small_climb_green.png', 3),
    'right_small_platform': load_image('right_small_platform.png', 3),
    'y': load_image('right_up_green.png', 2),
    'e': load_image('right_up_plate.png', 2),
    'rock': load_image('rock.png', 3),
    'shrooms': load_image('shrooms.png', 3),
    'sign': load_image('sign.png', 3),
    'skulls': load_image('skulls.png', 3),
    'small_grass': load_image('small_grass.png', 3),
    'P': load_image('small_platform.png', 2),
    'I': load_image('small_spirala.png', 2),
    'spike_skull': load_image('spike_skull.png', 3),
    'spikes': load_image('spikes.png', 3),
    'spikes_top': load_image('spikes_top.png', 3),
    '_': load_image('stones.png', 2),
    'T': load_image('torch.png', 2),
    'tree': load_image('tree.png', 3),
    'up_big_green_decor': load_image('up_big_green_decor.png', 3),
    'up_decor': load_image('up_decor.png', 3),
    't': load_image('up_green.png', 2),
    'w': load_image('up_plate.png', 2),
    'up_small_green_decor': load_image('up_small_green_decor.png', 3),
    'up_stump': load_image('up_stump.png', 3)
}
tile_width = tile_height = 40


class Tile(pygame.sprite.Sprite):  # Расстановка тайлов
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites)
        if tile_type == 'w':
            tiles_group.add(self)
        self.image = pygame.transform.scale(tile_images[tile_type], (40, 40))
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


def load_level(filename):  # Чтение уровня из текстового файла
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def start_click(pos):  # Обработка нажатия в начальном экране
    x, y = pos
    player = None
    if 300 <= y <= 680:
        if 300 <= x <= 550:
            player = Player(20, 337, 1)
        elif 790 <= x <= 1060:
            player = Player(1048, 387, 2)
        elif 1350 <= x <= 1595:
            player = Player(20, 344, 3)
        if player:
            player.cut_sheet('idle')
            return player


def start_screen():  # Начальный экран
    fon = pygame.transform.scale(load_image('field.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    mainstarttext = MainStartText()
    choosestarttext = ChooseStartText()
    player1 = Player(280, 305, 1)
    player2 = Player(810, 330, 2)
    player3 = Player(1340, 295, 3)
    pygame.mixer.music.load('data/startmusic.mp3')
    pygame.mixer.music.play(-1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                player = start_click(event.pos)
                if player:
                    pygame.mixer.music.stop()
                    for sprite in [player1, player2, player3, mainstarttext,
                                   choosestarttext]:
                        all_sprites.remove(sprite)
                    return player
        screen.blit(fon, (0, 0))
        all_sprites.update()
        all_sprites.draw(screen)
        player1.count += V / FPS
        player2.count += V / FPS
        player3.count += V / FPS
        pygame.display.flip()
        clock.tick(FPS)


class MainStartText(pygame.sprite.Sprite):  # Главный текст начального экрана
    def __init__(self):
        super().__init__(all_sprites)
        self.image = load_image('mainstarttext.png')
        self.rect = self.image.get_rect().move(WIDTH // 2 - 450, 0)


class ChooseStartText(pygame.sprite.Sprite):  # Текст начального экрана
    def __init__(self):
        super().__init__(all_sprites)
        self.image = load_image('startchoose.png')
        self.rect = self.image.get_rect().move(WIDTH // 2 - 300, 155)


class Player(pygame.sprite.Sprite):  # Главный герой
    def __init__(self, x, y, n):
        super().__init__(player_group, all_sprites)
        self.x, self.y, self.n, self.count, self.cur_frame, self.vx, self.vy = x, y, n, 0, 0, 0, 0
        self.frames = []
        self.way, self.on_ground = True, False
        self.collideRect = CollideRect(n)
        # idle, run, jump, fall, attack, take hit, death
        if self.n == 1:
            self.a, self.b, self.c, self.d, self.e, self.f, self.g = 8, 8, 2, 2, 4, 4, 6
        elif self.n == 2:
            self.a, self.b, self.c, self.d, self.e, self.f, self.g = 8, 8, 2, 2, 6, 4, 6
        elif self.n == 3:
            self.a, self.b, self.c, self.d, self.e, self.f, self.g = 4, 8, 2, 2, 4, 3, 7
        self.cut_sheet('idle_big')
        self.image = self.frames[self.cur_frame]

    def cut_sheet(self, status):  # обработка спрайт-листов
        self.frames = []
        if status == 'idle' or status == 'idle_big':
            string = 'Idle'
            columns = self.a
        elif status in ['run_left', 'run_right']:
            string = 'Run'
            columns = self.b
        elif status == 'jump':
            string = 'Jump'
            columns = self.c
        elif status == 'fall':
            string = 'Fall'
            columns = self.d
        elif status == 'attack':
            columns = self.e
            string = random.choice(['Attack1', 'Attack2'])
        elif status == 'take_hit':
            columns = self.f
            string = 'Take Hit'
        else:
            columns = self.g
            string = 'Death'
        if status == 'idle_big':
            width, height = 1200 * columns, 1200
        else:
            width, height = 300 * columns, 300
        image = load_image(f'{self.n}{string}.png', colorkey=-1)
        if status == 'run_left' or status == 'attack' and not self.way or \
                status == 'idle' and not self.way:
            image = pygame.transform.flip(image, True, False)
        sheet = pygame.transform.scale(image, (width, height))
        if status == 'idle_big':
            self.rect = pygame.Rect(self.x, self.y, 240, 160)
        else:
            self.rect = pygame.Rect(self.rect.x, self.rect.y, 60, 84)
        if status == 'idle_big':
            for i in range(columns):
                frame_location = (450 + 1200 * i, 420)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, (260, 350))))
        else:
            for i in range(columns):
                frame_location = (7 + 300 * i, 65)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, (285, 130))))

    def update(self):  # Обновление персонажа
        if self.count > 1:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.count = 0
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.n == 1:
            self.collideRect.rect.x = self.rect.x + 115
            self.collideRect.rect.y = self.rect.y + 42
        elif self.n == 2:
            self.collideRect.rect.x = self.rect.x + 120
            self.collideRect.rect.y = self.rect.y + 40
        else:
            self.collideRect.rect.x = self.rect.x + 125
            self.collideRect.rect.y = self.rect.y + 42

    def check_event(self, event):  # Реакция героя на события
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.cut_sheet('attack')
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                self.vx = -10
                self.cut_sheet('run_left')
                self.way = False
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                self.vx = 10
                self.cut_sheet('run_right')
                self.way = True
            elif event.key == pygame.K_w or event.key == pygame.K_UP:
                self.vy = -10
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                self.vy = 10
            elif event.key == pygame.K_SPACE:
                pass
            elif event.mod & pygame.KMOD_CTRL:
                print('attack')
        elif event.type == pygame.KEYUP:
            if (event.key == pygame.K_a or event.key == pygame.K_LEFT) and self.vx < 0:
                self.vx = 0
                self.cut_sheet('idle')
            if (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and self.vx > 0:
                self.vx = 0
                self.cut_sheet('idle')
            if event.key == pygame.K_w or event.key == pygame.K_UP and self.vy < 0:
                self.vy = 0
            if event.key == pygame.K_s or event.key == pygame.K_DOWN and self.vy > 0:
                self.vy = 0


class CollideRect(pygame.sprite.Sprite):  # Прямоугольник столкновения игрока
    def __init__(self, n):
        super().__init__(playerRect_group, all_sprites)
        if n == 1:
            w, h = 56, 84
        elif n == 2:
            w, h = 45, 79
        else:
            w, h = 45, 86
        self.rect = pygame.Rect(0, 0, w, h)
        self.image = load_image('nothing.png')


class Camera:  # Камера
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def update(self, target):
        rect = target.image.get_rect().move(target.rect.x, target.rect.y)
        self.dx = rect.x + rect.w // 2 - WIDTH // 2
        self.dy = rect.y + rect.h // 2 - HEIGHT // 2

    def apply(self, sprite):
        sprite.rect.x -= self.dx // 8
        sprite.rect.y -= self.dy // 8


def generate_level(level):  # Генерация уровня
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] != '.':
                Tile(level[y][x], x, y)
    return level


player = start_screen()
level = generate_level(load_level('map.txt'))
fon = pygame.transform.scale(load_image('back.png'), (WIDTH, HEIGHT))
camera = Camera()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        player.check_event(event)
    screen.blit(fon, (0, 0))
    all_sprites.update()
    all_sprites.draw(screen)
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    player.count += V / FPS
    pygame.display.flip()
    clock.tick(FPS)
