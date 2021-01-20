import pygame

pygame.init()
win = pygame.display.set_mode((1500, 500))
pygame.display.set_caption('опоссум')

walkright = [pygame.image.load('right_opossum-1.png'),
             pygame.image.load('right_opossum-2.png'), pygame.image.load('right_opossum-3.png'),
             pygame.image.load('right_opossum-4.png'), pygame.image.load('right_opossum-5.png'),
             pygame.image.load('right_opossum-1.png')]

image = [pygame.image.load('opossum-1.png'),
            pygame.image.load('opossum-2.png'), pygame.image.load('opossum-3.png'),
            pygame.image.load('opossum-4.png'), pygame.image.load('opossum-5.png'),
            pygame.image.load('opossum-6.png')]
bg = pygame.image.load('front.jpg')

x = 0
y = 427

whith = 60
height = 71

speed = 5

left = False
right = True
animcount = 0
maxLengthLeft = 60 #отвечает за пройденное расстояние опоссумом
clock = pygame.time.Clock()
animcount_2 = 0
RIGHT_MOVE = 1
LEFT_MOVE = 2
MOVE_DISTANCE = 2
state = RIGHT_MOVE


def drawWindow():
    global animcount
    win.blit(bg, (0, 0))

    if animcount + 1 >= 30:
        animcount = 0


    if state == RIGHT_MOVE:
        win.blit(walkright[animcount // 5], (x, y))
        animcount += 1
    else:
        win.blit(image[animcount // 5], (x, y))
        animcount += 1
    pygame.display.update()

run = True
while run:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if state == RIGHT_MOVE:
        x += MOVE_DISTANCE
        if x - MOVE_DISTANCE > maxLengthLeft:
            if x > maxLengthLeft - maxLengthLeft:
                state = LEFT_MOVE
    else:
        x -= MOVE_DISTANCE
        if x < 0:
            state = RIGHT_MOVE

    drawWindow()
pygame.quit()
