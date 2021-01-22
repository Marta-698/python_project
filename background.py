import pygame
import os
import sys
import random

pygame.init()
size = WIDTH, HEIGHT = 1920, 1000
pygame.display.set_caption('Отряд супергероев')
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
start_sprites = pygame.sprite.Group()
tile_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
playerRect_group = pygame.sprite.Group()
NPC_group = pygame.sprite.Group()
FPS = 90
V = 15


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
        if colorkey == 1:
            colorkey = image.get_at((0, 0))
        elif colorkey == 2:
            colorkey = image.get_at((15, 0))
        elif colorkey == 3:
            colorkey = image.get_at((0, 15))
        elif colorkey == 4:
            colorkey = image.get_at((15, 15))
        elif colorkey == 5:
            colorkey = image.get_at((31, 15))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


tile_images = {  # Тайлы и декорации
    'S': load_image('1_stone.png', 2),
    'W': load_image('3_stones.png', 2),
    '$': load_image('4_stones.png', 2),
    'big_bricks': load_image('big_bricks.png', 3),
    'big_crate': load_image('big_crate.png', 3),
    'big_grass': load_image('big_grass.png', 3, colorkey=1),
    'big_spiral': load_image('big_spiral.png', 3),
    'B': load_image('black.png', 2),
    'block_big': load_image('block_big.png', 3),
    'R': load_image('bricks.png', 2),
    'b': load_image('brown.png', 2),
    'C': load_image('crate.png', 2),
    'k': load_image('dirt.png', 2),
    'm': load_image('down_dirt.png', 2),
    'x': load_image('down_plate.png', 2),
    'grass_1': load_image('grass_1.png', 3),
    'grass_2': load_image('grass_2.png', 3),
    'grass_3': load_image('grass_3.png', 3),
    'grass_4': load_image('grass_4.png', 3),
    'grass_5': load_image('grass_5.png', 3),
    'g': load_image('green.png', 2),
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
    'left_branch': load_image('left_branch.png', 3),
    'left_corner': load_image('left_corner.png', 3),
    'j': load_image('left_dirt.png', 2),
    'n': load_image('left_down_dirt.png', 2),
    'z': load_image('left_down_plate.png', 2),
    'f': load_image('left_green.png', 2),
    'a': load_image('left_plate.png', 2),
    '}': load_image('left_small_platform.png', 3, colorkey=5),
    'r': load_image('left_up_green.png', 2, colorkey=3),
    'q': load_image('left_up_plate.png', 2),
    'right_branch': load_image('right_branch.png', 3),
    'right_corner': load_image('right_corner.png', 3),
    'l': load_image('right_dirt.png', 2),
    ',': load_image('right_down_dirt.png', 2),
    'c': load_image('right_down_plate.png', 2),
    'h': load_image('right_green.png', 2),
    'd': load_image('right_plate.png', 2),
    '{': load_image('right_small_platform.png', 3, colorkey=3),
    'y': load_image('right_up_green.png', 2, colorkey=4),
    'e': load_image('right_up_plate.png', 2),
    'small_grass': load_image('small_grass.png', 3, colorkey=1),
    'P': load_image('small_platform.png', 2),
    'I': load_image('small_spirala.png', 2),
    'spike_skull': load_image('spike_skull.png', 3),
    'spikes': load_image('spikes.png', 3),
    's': load_image('stones.png', 2),
    'T': load_image('torch.png', 2),
    'tree': load_image('tree.png', 3),
    't': load_image('up_green.png', 2),
    'w': load_image('up_plate.png', 2),
    'M': load_image('block.png', 2),
    'i': load_image('small_spiral.png', 2),
    'tree1': load_image('tree1.png', 3, colorkey=1),
    'tree2': load_image('tree2.png', 3, colorkey=1),
    'tree3': load_image('tree3.png', 3, colorkey=1)
}
tile_width = tile_height = 40


class Tile(pygame.sprite.Sprite):  # Расстановка тайлов
    def __init__(self, tile_type, pos_x, pos_y, width=40, height=40, type=False):
        if tile_type in ['r', 't', 'y', '{', '}']:
            super().__init__(platform_group, all_sprites)
            if tile_type in ('{', '}'):
                width, height = 80, 40
            self.image = pygame.transform.scale(tile_images[tile_type], (width, height))
        elif type:
            super().__init__(all_sprites)
        else:
            super().__init__(tile_group, all_sprites)
        self.image = pygame.transform.scale(tile_images[tile_type], (width, height))
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
            player = Player(1100, 600, 1)
        elif 790 <= x <= 1060:
            player = Player(1100, 600, 2)
        elif 1350 <= x <= 1595:
            player = Player(1100, 600, 3)
        if player:
            player.cut_sheet('idle')
            return player


def start_screen():  # Начальный экран
    fon = pygame.transform.scale(load_image('field.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    MainStartText()
    ChooseStartText()
    player1 = Player(280, 305, 1, area=False)
    player2 = Player(810, 330, 2, area=False)
    player3 = Player(1340, 295, 3, area=False)
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
                    return player
        screen.blit(fon, (0, 0))
        start_sprites.update()
        start_sprites.draw(screen)
        player1.count += V / FPS
        player2.count += V / FPS
        player3.count += V / FPS
        pygame.display.flip()
        clock.tick(FPS)


class MainStartText(pygame.sprite.Sprite):  # Главный текст начального экрана
    def __init__(self):
        super().__init__(start_sprites)
        self.image = load_image('mainstarttext.png')
        self.rect = self.image.get_rect().move(WIDTH // 2 - 450, 0)


class ChooseStartText(pygame.sprite.Sprite):  # Текст начального экрана
    def __init__(self):
        super().__init__(start_sprites)
        self.image = load_image('startchoose.png')
        self.rect = self.image.get_rect().move(WIDTH // 2 - 300, 160)


def finish_screen():
    fon = pygame.transform.scale(load_image('field.jpg'), (WIDTH, HEIGHT))


class Player(pygame.sprite.Sprite):  # Главный герой
    def __init__(self, x, y, n, area=True):
        if area:
            super().__init__(all_sprites)
        else:
            super().__init__(start_sprites)
        self.x, self.y, self.n, self.count, self.cur_frame, self.vx, self.vy = x, y, n, 0, 0, 0, 5
        self.frames, self.way, self.on_ground = [], True, False
        self.right_pressed = self.left_pressed = False
        self.attacking = self.can_attack = False
        self.taking_hit = False
        self.can_take_hit = True
        self.dying = self.is_dead = False
        self.action = ''
        self.timer = 1
        self.collide = CollideRect(n)
        self.attack = AttackRect(n)
        # idle, run, jump, fall, attack, take hit, death
        if self.n == 1:
            self.c_x, self.c_y, self.k, self.hp, self.damage, self.speed = 115, 42, 0, 50, 15, 6
            self.frames_count = {'idle_big': 8, 'idle': 8, 'run': 8, 'jump': 2, 'fall': 2,
                                 'attack': 4, 'take_hit': 4, 'death': 6}
        elif self.n == 2:
            self.c_x, self.c_y, self.k, self.hp, self.damage, self.speed = 120, 39, 5, 65, 20, 5
            self.frames_count = {'idle_big': 8, 'idle': 8, 'run': 8, 'jump': 2, 'fall': 2,
                                 'attack': 6, 'take_hit': 4, 'death': 6}
        elif self.n == 3:
            self.c_x, self.c_y, self.k, self.hp, self.damage, self.speed = 125, 42, -2, 40, 15, 7
            self.frames_count = {'idle_big': 4, 'idle': 4, 'run': 8, 'jump': 2, 'fall': 2,
                                 'attack': 4, 'take_hit': 3, 'death': 7}
        self.cut_sheet('idle_big')
        self.image = self.frames[self.cur_frame]

    def cut_sheet(self, status):  # обработка спрайт-листов
        self.frames = []
        self.action = status
        columns = self.frames_count[status]
        if status == 'attack':
            status = random.choice(['attack1', 'attack2'])
        if status == 'idle_big':
            width, height = 1200 * columns, 1200
        else:
            width, height = 300 * columns, 300
        if status == 'idle_big':
            image = load_image(f'{self.n}{"idle"}.png', colorkey=1)
        else:
            image = load_image(f'{self.n}{status}.png', colorkey=1)
        if not self.way:
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
        if self.is_dead:
            return
        if self.count > 1 and self.attacking:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.count = 0
            if self.cur_frame + 1 == len(self.frames):
                self.attacking = self.can_attack = False
        if self.count > 1 and self.dying:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.count = 0
            if self.cur_frame + 1 == len(self.frames):
                self.dying = False
                self.is_dead = True
        elif self.count > 1 and self.taking_hit:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.count = 0
            if self.cur_frame + 1 == len(self.frames):
                self.taking_hit = False
        elif self.count > 1:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.count = 0
        if self.rect.h > 150:
            return
        self.on_ground = False
        if self.left_pressed:
            self.vx = -self.speed
        elif self.right_pressed:
            self.vx = self.speed
        else:
            self.vx = 0
        for tile in tile_group:
            rect1 = self.collide.rect
            rect2 = tile.rect
            if 0 <= (rect1.bottom + self.vy) - rect2.top <= 10 and (
                    rect2.x < rect1.x < rect2.right or rect2.x < rect1.right < rect2.right or
                    rect1.x < rect2.x < rect1.right or rect1.x < rect2.right < rect1.right):
                self.vy = 0
                self.on_ground = True
                self.rect.bottom = rect2.top - self.c_y + self.k
            if 0 <= rect2.right - (rect1.left + self.vx) <= 7 and (
                    rect2.y < rect1.y < rect2.bottom or rect2.y < rect1.bottom < rect2.bottom or
                    rect1.y < rect2.y < rect1.bottom or rect1.y < rect2.bottom < rect1.bottom):
                self.vx = max(self.vx, 0)
            if 0 <= (rect1.right + self.vx) - rect2.left <= 7 and (
                    rect2.y < rect1.y < rect2.bottom or rect2.y < rect1.bottom < rect2.bottom or
                    rect1.y < rect2.y < rect1.bottom or rect1.y < rect2.bottom < rect1.bottom):
                self.vx = min(self.vx, 0)
        for platform in platform_group:
            rect1 = self.collide.rect
            rect2 = platform.rect
            if 0 <= (rect1.bottom + self.vy) - rect2.top <= 10 and self.vy >= 0 and (
                    rect2.x < rect1.x < rect2.right or rect2.x < rect1.right < rect2.right or
                    rect1.x < rect2.x < rect1.right or rect1.x < rect2.right < rect1.right):
                self.vy = 0
                self.on_ground = True
                self.rect.bottom = rect2.top - self.c_y + self.k
        if not self.on_ground and abs(float('%.1f' % (self.vy + 0.2))) <= 8:
            self.vy = float('%.1f' % (self.vy + 0.2))
        if self.vx and not self.vy:
            if self.vx > 0 and not self.way and not self.attacking and not self.taking_hit:
                self.way = True
                self.cut_sheet('run')
            elif self.vx < 0 and self.way and not self.attacking and not self.taking_hit:
                self.way = False
                self.cut_sheet('run')
            if self.action != 'run' and not self.attacking and not self.taking_hit:
                self.cut_sheet('run')
        elif not self.vy:
            if self.action != 'idle' and not self.attacking and not self.taking_hit:
                self.cut_sheet('idle')
        if self.vy < 0 and self.action != 'jump' and not self.attacking and not self.taking_hit:
            self.cut_sheet('jump')
        elif self.vy > 0 and self.action != 'fall' and not self.attacking and not self.taking_hit:
            self.cut_sheet('fall')
        if pygame.sprite.spritecollideany(self.collide, NPC_group) and self. \
                action != 'take_hit' and self.can_take_hit:
            self.hp -= 10
            self.vy = -6
            self.taking_hit = True
            self.can_take_hit = False
            self.timer = 1
            self.cut_sheet('take_hit')
        if self.can_attack:
            for npc in NPC_group:
                if pygame.sprite.collide_rect(self.attack, npc):
                    npc.hp -= self.damage
                    self.can_attack = False
        if self.hp <= 0:
            self.dying = True
            self.cut_sheet('death')
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.collide.rect.x = self.rect.x + self.c_x
        self.collide.rect.y = self.rect.y + self.c_y
        if self.way:
            self.attack.rect.x = self.collide.rect.x
        else:
            self.attack.rect.right = self.collide.rect.right
        self.attack.rect.y = self.collide.rect.y

    def check_event(self, event):  # Реакция героя на события
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.attacking:
                self.attacking = True
                self.can_attack = True
                self.cur_frame = 0
                self.cut_sheet('attack')
                pass
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                self.left_pressed = True
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                self.right_pressed = True
            if (event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.
                    K_UP) and self.on_ground:
                self.on_ground = False
                self.vy = -8
            if event.mod & pygame.KMOD_CTRL and not self.attacking:
                self.attacking = True
                self.can_attack = True
                self.cur_frame = 0
                self.cut_sheet('attack')
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                self.left_pressed = False
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                self.right_pressed = False


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


class AttackRect(pygame.sprite.Sprite):  # Прямоугольник столкновения игрока
    def __init__(self, n):
        super().__init__(playerRect_group, all_sprites)
        if n == 1:
            w, h = 156, 84
        elif n == 2:
            w, h = 145, 79
        else:
            w, h = 145, 86
        self.rect = pygame.Rect(0, 0, w, h)
        self.image = load_image('nothing.png')


class Opossum(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(NPC_group, all_sprites)
        self.way = True
        self.cur_frame = 0
        self.total_frames = 0
        self.vx = 5
        self.hp = 30
        self.frames = ['opossum-1.png', 'opossum-2.png', 'opossum-3.png', 'opossum-4.png',
                       'opossum-5.png', 'opossum-6.png']
        self.count = 0
        self.image = load_image(self.frames[self.cur_frame])
        self.rect = self.image.get_rect().move(x, y)
        self.way = False

    def update(self):
        if self.count > 1:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.total_frames += 1
            self.image = pygame.transform.scale(load_image(self.frames[self.cur_frame]), (72, 56))
            if not self.way:
                self.image = pygame.transform.flip(self.image, True, False)
            self.count = 0
            if self.total_frames == 14:
                self.way = not self.way
                self.vx = -self.vx
                self.total_frames = 0
        self.rect.x += self.vx
        if self.hp <= 0:
            all_sprites.remove(self)
            NPC_group.remove(self)


class Eagle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(NPC_group, all_sprites)


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
opossum = Opossum(1600, 784)
level = generate_level(load_level('map.txt'))
Tile('small_grass', 44, 20, width=48, height=40, type=True)
Tile('small_grass', 47, 16, width=48, height=40, type=True)
Tile('big_grass', 60, 20, width=48, height=40, type=True)
Tile('big_grass', 57, 14, width=48, height=40, type=True)
Tile('spike_skull', 200, 19, width=56, height=40, type=True)
Tile('spikes', 230, 24, width=60, height=40, type=True)
Tile('tree1', 26, 16.7, width=136, height=174, type=True)
Tile('tree2', 90, 16.2, width=96, height=192, type=True)
Tile('tree3', 214, 15.2, width=96, height=192, type=True)
fon = pygame.transform.scale(load_image('back.png'), (WIDTH, HEIGHT))
camera = Camera()
dt = 0
timer1 = 2
i = 0
last = player.rect.x
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
    opossum.count += V / FPS
    player.timer -= dt
    if player.timer <= 0:
        player.can_take_hit = True
    pygame.display.flip()
    dt = clock.tick(FPS) / 1000
