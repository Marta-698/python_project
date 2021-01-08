import pygame
import os
import sys

pygame.init()
size = WIDTH, HEIGHT = 1920, 1000
pygame.display.set_caption('Платформер')
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 60
ALT_PRESSED = F4_PRESSED = False


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


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.mod & pygame.KMOD_ALT:
                ALT_PRESSED = True
            if event.key == pygame.K_F4:
                F4_PRESSED = True
        if event.type == pygame.KEYUP:
            if event.mod & pygame.KMOD_ALT:
                ALT_PRESSED = False
            if event.key == pygame.K_F4:
                F4_PRESSED = False
        if ALT_PRESSED and F4_PRESSED:
            terminate()
    pygame.display.flip()
    clock.tick(FPS)
