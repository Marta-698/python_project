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
decor_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
playerRect_group = pygame.sprite.Group()
NPC_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
finish_group = pygame.sprite.Group()
finish_screen_group = pygame.sprite.Group()
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
    'big_grass': load_image('big_grass.png', 3, colorkey=1),
    'R': load_image('black.png', 2),
    'B': load_image('bricks.png', 2),
    'b': load_image('brown.png', 2),
    'C': load_image('crate.png', 2),
    'k': load_image('dirt.png', 2),
    'm': load_image('down_dirt.png', 2),
    'x': load_image('down_plate.png', 2),
    'grass_1': load_image('grass_1.png', 3),
    'grass_3': load_image('grass_3.png', 3),
    'g': load_image('green.png', 2),
    '1': load_image('ground_1.png', 2),
    '2': load_image('ground_2.png', 2),
    '3': load_image('ground_3.png', 2),
    '4': load_image('ground_4.png', 2),
    '8': load_image('ground_8.png', 2),
    '-': load_image('ground_11.png', 2),
    'j': load_image('left_dirt.png', 2),
    'n': load_image('left_down_dirt.png', 2),
    'z': load_image('left_down_plate.png', 2),
    'f': load_image('left_green.png', 2),
    'a': load_image('left_plate.png', 2),
    '}': load_image('left_small_platform.png', 3, colorkey=5),
    'r': load_image('left_up_green.png', 2, colorkey=3),
    'q': load_image('left_up_plate.png', 2),
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
    'tree': load_image('tree.png', 3),
    't': load_image('up_green.png', 2),
    'w': load_image('up_plate.png', 2),
    'M': load_image('block.png', 2),
    'i': load_image('small_spiral.png', 2),
    'tree1': load_image('tree1.png', 3, colorkey=1),
    'tree2': load_image('tree2.png', 3, colorkey=1),
    'tree3': load_image('tree3.png', 3, colorkey=1),
    'stump': load_image('stump.png', 2, colorkey=1),
    'sign': load_image('sign.png', 3, colorkey=3),
    'shrooms': load_image('shrooms.png', 3, colorkey=2)
}
tile_width = tile_height = 40


class Tile(pygame.sprite.Sprite):  # Расстановка тайлов
    def __init__(self, tile_type, pos_x, pos_y, width=40, height=40):
        if tile_type in ['r', 't', 'y', '{', '}']:
            super().__init__(platform_group, all_sprites)
            if tile_type in ('{', '}'):
                width, height = 80, 40
            self.image = pygame.transform.scale(tile_images[tile_type], (width, height))
        elif tile_type in ['R', 'B']:
            super().__init__(all_sprites)
        else:
            super().__init__(tile_group, all_sprites)
        self.image = pygame.transform.scale(tile_images[tile_type], (width, height))
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Decor(pygame.sprite.Sprite):  # Расстановка декораций
    def __init__(self, name, x, y, width, height):
        super().__init__(decor_group, all_sprites)
        self.image = pygame.transform.scale(tile_images[name], (width, height))
        self.rect = self.image.get_rect().move(x * 10, y * 10)


class Stump(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(finish_group, all_sprites)
        self.image = pygame.transform.scale(tile_images['stump'], (40, 40))
        self.rect = self.image.get_rect().move(x * 10, y * 10)


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
    Specifications1()
    Specifications2()
    Specifications3()
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


def finish_screen(status):
    global game_finished
    game_finished = True
    pygame.mixer.music.stop()
    pygame.mixer.music.load('data/finishmusic.mp3')
    pygame.mixer.music.play(-1)
    fon = pygame.transform.scale(load_image('img.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    if status:
        Congrats()
    else:
        GameOver()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                terminate()
        screen.blit(fon, (0, 0))
        finish_screen_group.update()
        finish_screen_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


class Congrats(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(finish_screen_group)
        self.image = load_image('congrats.png')
        self.rect = self.image.get_rect().move(WIDTH // 2 - 450, 0)


class GameOver(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(finish_screen_group)
        self.image = load_image('gameover.png')
        self.rect = self.image.get_rect().move(WIDTH // 2 - 450, 0)


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


class Specifications1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(start_sprites)
        self.image = load_image('image1.png')
        self.rect = self.image.get_rect().move(120, 670)


class Specifications2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(start_sprites)
        self.image = load_image('image2.png')
        self.rect = self.image.get_rect().move(660, 670)


class Specifications3(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(start_sprites)
        self.image = load_image('image3.png')
        self.rect = self.image.get_rect().move(1200, 670)


class Player(pygame.sprite.Sprite):  # Главный герой
    def __init__(self, x, y, n, area=True):
        if area:
            super().__init__(player_group)
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
        self.total_hp = self.hp
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
            finish_screen(False)
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
            if self.vx and not self.vy and self.action != 'run' and not self. \
                    attacking and not self.taking_hit:
                self.cut_sheet('run')
        elif not self.vy:
            if self.action != 'idle' and not self.attacking and not self.taking_hit:
                self.cut_sheet('idle')
        if self.vy < 0 and self.action != 'jump' and not self.attacking and not self.taking_hit:
            self.cut_sheet('jump')
        elif self.vy > 0 and self.action != 'fall' and not self.attacking and not self.taking_hit:
            self.cut_sheet('fall')
        if self.vx > 0 and not self.way and not self.attacking and not self.taking_hit:
            self.way = True
            self.cut_sheet(self.action)
        elif self.vx < 0 and self.way and not self.attacking and not self.taking_hit:
            self.way = False
            self.cut_sheet(self.action)
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
        if pygame.sprite.spritecollideany(self.collide, finish_group):
            finish_screen(True)
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
        super().__init__(NPC_group)
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
        self.alive = True

    def update(self):
        if self.count > 1:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.total_frames += 1
            if self.alive:
                self.image = pygame.transform.scale(load_image(self.frames[self.cur_frame]),
                                                    (72, 56))
            else:
                self.image = pygame.transform.scale(load_image(death_frames[self.cur_frame]),
                                                    (80, 82))
            if not self.way:
                self.image = pygame.transform.flip(self.image, True, False)
            self.count = 0
            if self.total_frames == 14:
                self.way = not self.way
                self.vx = -self.vx
                self.total_frames = 0
        if self.hp <= 0:
            self.alive = False
            self.vx = 0
        if not self.alive and self.cur_frame == 5:
            all_sprites.remove(self)
            NPC_group.remove(self)
        self.rect.x += self.vx


class Eagle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(NPC_group)
        self.cur_frame = self.total_frames = 0
        self.vy = 2
        self.hp = 20
        self.frames = ['eagle-1.png', 'eagle-2.png', 'eagle-3.png', 'eagle-4.png']
        self.count = 0
        self.image = load_image(self.frames[self.cur_frame])
        self.rect = self.image.get_rect().move(x, y)
        self.alive = True

    def update(self):
        if self.count > 1:
            self.total_frames += 1
            if self.alive:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = pygame.transform.scale(load_image(self.frames[self.cur_frame]),
                                                    (80, 82))
            else:
                self.cur_frame = (self.cur_frame + 1) % len(death_frames)
                self.image = pygame.transform.scale(load_image(death_frames[self.cur_frame]),
                                                    (80, 82))
            self.count = 0
        if self.total_frames == 8:
            self.total_frames = 0
            self.vy = -self.vy
        if self.hp <= 0:
            self.alive = False
        if not self.alive and self.cur_frame == 5:
            all_sprites.remove(self)
            NPC_group.remove(self)
        self.rect.y += self.vy


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
death_frames = ['death-1.png', 'death-2.png', 'death-3.png', 'death-4.png', 'death-5.png',
                'death-6.png']
opossum = Opossum(1600, 784)
opossum1 = Opossum(6300, 1064)
opossum2 = Opossum(4235, 984)
eagle = Eagle(2360, 400)
eagle1 = Eagle(8000, 590)
level = generate_level(load_level('map.txt'))
Decor('small_grass', 190, 81, 48, 30)
Decor('big_grass', 187, 64, 48, 39)
Decor('big_grass', 235, 80, 48, 39)
Decor('small_grass', 230, 57, 48, 30)
Decor('small_grass', 310, 65, 48, 30)
Decor('spike_skull', 792, 76, 53, 36)
Decor('spikes', 950, 96, 60, 40)
Decor('tree1', 110, 67, 136, 174)
Decor('tree2', 360, 69, 96, 192)
Decor('tree3', 840, 61, 96, 192)
Decor('grass_3', 772, 80, 40, 40)
Decor('grass_1', 776, 80, 40, 40)
Decor('grass_1', 780, 80, 40, 40)
Decor('grass_1', 784, 80, 40, 40)
Decor('grass_1', 788, 80, 40, 40)
Decor('sign', 780, 76, 36, 40)
Decor('shrooms', 815, 75.5, 48, 45)
Stump(938, 96)
Stump(942, 96)
Stump(946, 96)
Stump(950, 96)
Stump(954, 96)
Stump(958, 96)
Stump(962, 96)
Stump(966, 96)
Stump(970, 96)
Stump(974, 96)
Stump(978, 96)
Stump(982, 96)
Stump(986, 96)
Stump(990, 96)
Stump(994, 96)
Stump(998, 96)
fon = pygame.transform.scale(load_image('back.png'), (WIDTH, HEIGHT))
camera = Camera()
dt = 0
pygame.mixer.music.load('data/musictheme.mp3')
pygame.mixer.music.play(-1)
game_finished = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        player.check_event(event)
    screen.blit(fon, (0, 0))
    if not game_finished:
        all_sprites.update()
        all_sprites.draw(screen)
        player_group.update()
        player_group.draw(screen)
        camera.update(player)
        NPC_group.update()
        NPC_group.draw(screen)
        for sprites in (all_sprites, player_group, NPC_group):
            for sprite in sprites:
                camera.apply(sprite)
        for thing in [player, opossum, opossum1, eagle, eagle1, opossum2]:
            thing.count += V / FPS
        player.timer -= dt
        if player.timer <= 0:
            player.can_take_hit = True
        pygame.draw.rect(screen, (0, 0, 0), (10, 10, player.total_hp * 5, 10), 1)
        pygame.draw.rect(screen, (255, 0, 0), (11, 11, max(0, player.hp * 5 - 2), 8))
        pygame.display.flip()
        dt = clock.tick(FPS) / 1000
