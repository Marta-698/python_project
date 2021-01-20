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


class Monster(pygame.sprite.Sprite):
    def __init__(self, width, height):
        self.x, self.y, self.speed, self.animcount, self.RIGHT_MOVE, self.LEFT_MOVE, self.MOVE_DISTANCE = 0, 427, 5, 0, 1, 2, 2
        self.whith, self.height = width, height
        self.left, self.right = False, True
        self.maxLengthLeft = 60 #отвечает за пройденное расстояние опоссумом
        self.state = self.RIGHT_MOVE


    def drawWindow(self):
        win.blit(bg, (0, 0))

        if self.animcount + 1 >= 30:
            self.animcount = 0


        if self.state == self.RIGHT_MOVE:
            win.blit(walkright[self.animcount // 5], (self.x, self.y))
            self.animcount += 1
        else:
            win.blit(image[self.animcount // 5], (self.x, self.y))
            self.animcount += 1
        pygame.display.update()

    run = True
    while run:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        def event(self):
            if self.state == self.RIGHT_MOVE:
                self.x += self.MOVE_DISTANCE
                if self.x - self.MOVE_DISTANCE > self.maxLengthLeft:
                    if self.x > self.maxLengthLeft - self.maxLengthLeft:
                        self.state = self.LEFT_MOVE
            else:
                self.x -= self.MOVE_DISTANCE
                if self.x < 0:
                    self.state = self.RIGHT_MOVE

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('')
    width, height = 600, 95
    clock = pygame.time.Clock()
    pygame.quit()

