import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1138
screen_height = 640

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Goblin Attack')

#define game variables
tile_size = 64

class Player():
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.images_front = []
        self.images_back = []
        self.index = 0
        self.counter = 0
        for num in range(1, 8):
            img_right = pygame.image.load('Assets/Player/goblin_right_' + str(num) + '.png').convert()
            img_left = pygame.image.load('Assets/Player/goblin_left_' + str(num) + '.png').convert()
            img_front = pygame.image.load('Assets/Player/goblin_front_' + str(num) + '.png').convert()
            img_back = pygame.image.load('Assets/Player/goblin_back_' + str(num) + '.png').convert()
			
            self.images_right.append(img_right)
            self.images_left.append(img_left)
            self.images_front.append(img_front)
            self.images_back.append(img_back)

        self.image = self.images_back[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
		# self.vel_y = 0
		# self.jumped = False
        self.direction = 'up'

    def update(self):
        dx = 0
        dy = 0
        walk_cooldown = 3

		#get keypresses
        key = pygame.key.get_pressed()
		# if key[pygame.K_SPACE] and self.jumped == False:
		# 	self.vel_y = -15
		# 	self.jumped = True
		# if key[pygame.K_SPACE] == False:
		# 	self.jumped = False
        if key[pygame.K_LEFT]:
            dx -= 2
            self.counter += 1
            self.direction = 'left'
        if key[pygame.K_RIGHT]:
            dx += 2
            self.counter += 1
            self.direction = 'right'
        if key[pygame.K_UP]:
            dy -= 2
            self.counter += 1
            self.direction = 'up'
        if key[pygame.K_DOWN]:
            dy += 2
            self.counter += 1
            self.direction = 'down'

        if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False and key[pygame.K_UP] == False and key[pygame.K_DOWN] == False:
            self.counter = 0
            self.index = 0
            if self.direction == 'right':
                self.image = self.images_right[self.index]
            if self.direction == 'left':
                self.image = self.images_left[self.index]
            if self.direction == 'up':
                self.image = self.images_back[self.index]
            if self.direction == 'down':
                self.image = self.images_front[self.index]

        # if :
        #     self.counter = 0
        #     self.index = 0
        #    

		#handle animation
        if self.counter > walk_cooldown:
            self.counter = 0	
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == 'right':
                self.image = self.images_right[self.index]
            if self.direction == 'left':
                self.image = self.images_left[self.index]
            if self.direction == 'up':
                self.image = self.images_back[self.index]
            if self.direction == 'down':
                self.image = self.images_front[self.index]

		#check for collision

		#update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0

		#draw player onto screen
        screen.blit(self.image, self.rect)


player = Player(100, screen_height - 130)

run = True
while run:

    clock.tick(fps)
    screen.fill((0, 0, 0))

    player.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()