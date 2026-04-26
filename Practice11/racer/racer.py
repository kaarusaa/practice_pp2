import pygame
import random
import time

pygame.init() #initializes all the pygame sub-modules

width = 400
height = 600
last_speedup = 0
N = 5  # speed up every 5 points
screen = pygame.display.set_mode((width, height)) #creating a game window


image_bg = pygame.image.load('C:\\Users\\Акниет\\Desktop\\practice_pp2\\Practice10\\racer\\resources\\AnimatedStreet.png')
image_player = pygame.image.load('C:\\Users\\Акниет\\Desktop\\practice_pp2\\Practice10\\racer\\resources\\Player.png')
image_enemy = pygame.image.load('C:\\Users\\Акниет\\Desktop\\practice_pp2\\Practice10\\racer\\resources\\Enemy.png')
coin_image = pygame.image.load('C:\\Users\\Акниет\\Desktop\\practice_pp2\\Practice10\\racer\\resources\\dollar.png').convert_alpha()
# convert_alpha() preserves PNG transparency

collected = 0

pygame.mixer.music.load('C:\\Users\\Акниет\\Desktop\\practice_pp2\\Practice10\\racer\\resources\\background.wav')
pygame.mixer.music.play(-1) #plays the music in a loop

sound_crash = pygame.mixer.Sound('C:\\Users\\Акниет\\Desktop\\practice_pp2\\Practice10\\racer\\resources\\crash.wav')

font = pygame.font.SysFont('Arial', 60)
font_small = pygame.font.SysFont('Arial', 20)

image_game_over = font.render('Game Over', True, 'black')
image_game_over_rect = image_game_over.get_rect(center = (width // 2, height // 2)) # get_rect helps position text
score = font_small.render('Score: ' + str(collected), True, 'black')
score_rect = score.get_rect(center = (325, 10))

class Player(pygame.sprite.Sprite): # Inherit from Sprite to use built-in functionality
    def __init__(self):
        super().__init__()
        self.image = image_player
        self.rect = self.image.get_rect()  # Rect creates a rectangle area 
        self.rect.centerx = width // 2 # Place player in center horizontally
        self.rect.bottom = height # Place player at bottom of screen
        self.speed = 5

    def move(self):
        keys = pygame.key.get_pressed() # Detect currently pressed keys
        if keys[pygame.K_RIGHT]:
             self.rect.move_ip(self.speed, 0)  # move_ip = move in place
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        # Prevent leaving left and right borders
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_enemy
        self.rect = self.image.get_rect()
        self.speed = 10

    def generate_random_rect(self):
        self.rect.left = random.randint(0, width - self.rect.w)
        self.rect.bottom = 0

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > height:
            self.generate_random_rect() # If enemy leaves screen, respawn it from top

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_image
        self.size = random.randint(1,3)
        self.image = pygame.transform.scale(self.image, (30*(self.size*0.5), 30*(self.size*0.5)))
        self.rect = self.image.get_rect()
        self.generate_random_rect()

    def generate_random_rect(self):
        # random x, but keep it within screen width
        self.size = random.randint(1,3)
        self.image = coin_image
        self.image = pygame.transform.scale(self.image, (30*(self.size*0.5), 30*(self.size*0.5))) # resize depending on the size of the coin
        self.rect.left = random.randint(0, WIDTH - self.rect.w)
        # fixed y near the bottom where the player moves
        self.rect.top = random.randint(HEIGHT - 80, HEIGHT - 20)

running = True

#setting the FPS
clock = pygame.time.Clock()
FPS = 60

player = Player()
enemy = Enemy()
coin = Coin()

all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
coin_sprites = pygame.sprite.Group()
all_sprites.add(player, enemy, coin)
enemy_sprites.add(enemy)
coin_sprites.add(coin)

while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    score = font_small.render('Score: ' + str(collected), True, 'black')
    player.move()
    screen.blit(image_bg, (0, 0))
    screen.blit(score, score_rect)
    for entity in all_sprites:
        if not isinstance(entity, Coin):
            entity.move() # Coin does not move, so move() is skipped
        screen.blit(entity.image, entity.rect)

    if pygame.sprite.spritecollideany(player, coin_sprites):
        collected += coin.size # addition of points based on coin size
        if collected // N > last_speedup:
            enemy.speed += 3          # fixed, controlled bump
            last_speedup = collected // N
        coin.generate_random_rect()

    if pygame.sprite.spritecollideany(player, enemy_sprites):
        sound_crash.play()
        time.sleep(1)

        running = False
        screen.fill('red')
        screen.blit(image_game_over, image_game_over_rect)
        pygame.display.flip()
        time.sleep(3) # pauses the program for 3 seconds

    pygame.display.flip() #updates the screen
    clock.tick(FPS) #sets the FPS

pygame.quit()
