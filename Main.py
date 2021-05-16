import pygame as pygame
import sys
from os import path

# game settings
WIDTH = 1280
HEIGHT = 720
FPS = 60
TITLE = "Winter Goblin"
BGCOLOR = pygame.Color(255,250,250)

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

PLAYER_SPEED = 125

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map = Map(path.join(game_folder, 'map2.txt'))

    def new(self):
        """initialize all variables and do all the setup for a new game"""
        self.all_sprites = pygame.sprite.Group()
        self.trees = pygame.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile in ['1','2','3']:
                    Tree(self, col, row, tile)
                if tile == 'P':
                    self.player = Player(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        """game loop - set self.playing = False to end the game"""
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw(self):
        self.screen.fill(BGCOLOR)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.images_right = []
        self.images_left = []
        self.images_front = []
        self.images_back = []
        self.index = 0
        self.counter = 0
        for num in range(1, 8):
            img_right = pygame.image.load('Assets/Player/goblin_right_' + str(num) + '.png').convert_alpha()
            img_left = pygame.image.load('Assets/Player/goblin_left_' + str(num) + '.png').convert_alpha()
            img_front = pygame.image.load('Assets/Player/goblin_front_' + str(num) + '.png').convert_alpha()
            img_back = pygame.image.load('Assets/Player/goblin_back_' + str(num) + '.png').convert_alpha()
			
            self.images_right.append(img_right)
            self.images_left.append(img_left)
            self.images_front.append(img_front)
            self.images_back.append(img_back)

        self.image = self.images_back[self.index]		
        self.direction = 'up'

        self.rect = self.image.get_rect()
        self.dx, self.dy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE

    def get_keys(self):
        self.dx, self.dy = 0, 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.dx = -PLAYER_SPEED
            self.counter += 1
            self.direction = 'left'
        if keys[pygame.K_RIGHT]:
            self.dx = PLAYER_SPEED
            self.counter += 1
            self.direction = 'right'
        if keys[pygame.K_UP]:
            self.dy = -PLAYER_SPEED
            self.counter += 1
            self.direction = 'up'
        if keys[pygame.K_DOWN]:
            self.dy = PLAYER_SPEED
            self.counter += 1
            self.direction = 'down'

    def collide_with_trees(self, dir):
        if dir == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.trees, False)
            if hits:
                if self.dx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.dx < 0:
                    self.x = hits[0].rect.right
                self.dx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.trees, False)
            if hits:
                if self.dy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.dy < 0:
                    self.y = hits[0].rect.bottom
                self.dy = 0
                self.rect.y = self.y

    def update(self):
        self.get_keys()
        self.x += self.dx * self.game.dt
        self.y += self.dy * self.game.dt
        self.rect.x = self.x
        self.collide_with_trees('x')
        self.rect.y = self.y
        self.collide_with_trees('y')

        if self.counter > 3:
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

class Tree(pygame.sprite.Sprite):
    def __init__(self, game, x, y, tree_type):
        self.groups = game.all_sprites, game.trees
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.tree_type = tree_type
        
        if tree_type == '1':
            self.image = pygame.image.load('Assets/Terrain/pine-full08.png').convert_alpha()
        if tree_type == '2':
            self.image = pygame.image.load('Assets/Terrain/pine-full01.png').convert_alpha()
        if tree_type == '3':
            self.image = pygame.image.load('Assets/Terrain/pine-half04.png').convert_alpha()
  
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pygame.Rect(x, y, self.width, self.height)

# create the game object
g = Game()

while True:
    g.new()
    g.run()