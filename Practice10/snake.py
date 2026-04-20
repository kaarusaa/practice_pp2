import pygame
import random

pygame.init()

width = 600
height = 600

white = (255, 255, 255)
gray = (200, 200, 200)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

screen = pygame.display.set_mode((width, height))

font = pygame.font.SysFont(None, 36)
image_game_over = font.render("Game Over", True, red)
image_game_over_rect = image_game_over.get_rect(center = (width // 2, height // 2))
sc_rect = image_game_over.get_rect(center = (width // 2, height // 2 + 30))

CELL = 30 # One snake cell size

def draw_grid(): # Draw cell borders
    for i in range(height // CELL):
        for j in range(width // CELL):
                if j!=0: # Skip top row (reserved for score display)
                        pygame.draw.rect(screen, gray, (i * CELL, j * CELL, CELL, CELL), 1)


def draw_grid_chess():
    colors = [white, gray]

    for i in range(height // CELL):
        if i != 0:
            for j in range(width // CELL):
                pygame.draw.rect(screen, colors[(i + j) % 2], (i * CELL, j * CELL, CELL, CELL)) # (i + j) % 2 alternates colors creating chess pattern

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self): # Converts point to text
        return f"{self.x}, {self.y}"

class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)] # Initial snake body
        self.dx = 1
        self.dy = 0
        self.score = 0
        self.level = 1 
        self.alive = True

    def move(self):
        # Move body from tail to head
        # Each segment copies previous segment
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
            
        # Move head in current direction
        self.body[0].x += self.dx
        self.body[0].y += self.dy

        # checks the right border
        if self.body[0].x > width // CELL - 1:
            print("Snake is out of the border! r")
            self.alive = False
        # checks the left border
        if self.body[0].x < 0:
            print("Snake is out of the border! l")
            self.alive = False
        # checks the bottom border
        if self.body[0].y > height // CELL - 1:
            print("Snake is out of the border! b")
            self.alive = False
        # checks the top border
        if self.body[0].y == 0:
            print("Snake is out of the border! t")
            self.alive = False


    def draw(self):
        head = self.body[0]
        pygame.draw.rect(screen, red, (head.x * CELL, head.y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, yellow, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_collision(self, food):
        head = self.body[0]
        # Check if snake eats food
        if head.x == food.pos.x and head.y == food.pos.y:
            self.score +=1
            print("Got food!")
            self.body.append(Point(head.x, head.y)) # Grow snake
            food.generate_random_pos(self.body) # Generate new food
            self.level = 1 + self.score//3 # Increase level every 3 points

class Food:
    def __init__(self):
        self.pos = Point(9, 9)

    def draw(self):
        pygame.draw.rect(screen, green, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def generate_random_pos(self, snake_body):
        while True:
            self.pos.x = random.randint(0, width // CELL - 1)
            self.pos.y = random.randint(0, height // CELL - 1)
            # Prevent food spawning:
            # 1) inside snake body
            # 2) in top row (UI row)
            if not any(self.pos.x == s.x and self.pos.y == s.y for s in snake_body) and self.pos.y > 0:
                break



FPS = 5
clock = pygame.time.Clock()
food = Food()
snake = Snake()
food.generate_random_pos(snake.body)  
running = True
while running:
    score = snake.score
    level = snake.level
    if snake.alive == False:
        stra = f"""Score: {score} 
Level: {level}"""
        sc_r = font.render(stra, True, red)
        font.render("Game Over", True, red)
        screen.fill(black)
        screen.blit(image_game_over, image_game_over_rect)
        screen.blit(sc_r, sc_rect)
        pygame.display.flip()
        pygame.time.wait(10000) # Wait 10 seconds

    sc = font.render(f'Score: {score}', True, white)
    lv = font.render(f'Level: {level}', True, white)   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                snake.dx = 1
                snake.dy = 0
            elif event.key == pygame.K_LEFT:
                snake.dx = -1
                snake.dy = 0
            elif event.key == pygame.K_DOWN:
                snake.dx = 0
                snake.dy = 1
            elif event.key == pygame.K_UP:
                snake.dx = 0
                snake.dy = -1

    screen.fill(black)

    draw_grid()

    snake.move()
    snake.check_collision(food)

    snake.draw()
    

# For the initial food position, either call it after both are created:
    food.draw()
    screen.blit(sc, (2, 0))
    screen.blit(lv, (120, 0))
    pygame.display.flip()
    clock.tick(FPS + level)

pygame.quit()
