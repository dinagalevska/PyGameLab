import pygame
import random
import sys
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Scavenger")

clock = pygame.time.Clock()
FPS = 60

RESOURCE_PATH = "spaceship_game_resources"
BACKGROUND_MUSIC = os.path.join(RESOURCE_PATH, "background_music.wav")
CLASH_SOUND = os.path.join(RESOURCE_PATH, "clash_sound.wav")
SPACESHIP_IMG = os.path.join(RESOURCE_PATH, "spaceship.png")
ASTEROID_IMG = os.path.join(RESOURCE_PATH, "asteroid.png")
CRYSTAL_IMG = os.path.join(RESOURCE_PATH, "energy_crystal.png")

spaceship_image = pygame.image.load(SPACESHIP_IMG).convert_alpha()
asteroid_image = pygame.image.load(ASTEROID_IMG).convert_alpha()
crystal_image = pygame.image.load(CRYSTAL_IMG).convert_alpha()

pygame.mixer.music.load(BACKGROUND_MUSIC)
clash_sound = pygame.mixer.Sound(CLASH_SOUND)

pygame.mixer.music.play(-1)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(spaceship_image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        size = random.randint(30, 70)
        self.image = pygame.transform.scale(asteroid_image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(3, 6)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Crystal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(crystal_image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

all_sprites = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
crystals = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

score = 0
running = True

def spawn_asteroid():
    asteroid = Asteroid()
    all_sprites.add(asteroid)
    asteroids.add(asteroid)

def spawn_crystal():
    crystal = Crystal()
    all_sprites.add(crystal)
    crystals.add(crystal)

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if random.randint(1, 100) < 3:
        spawn_asteroid()
    if random.randint(1, 100) < 2:
        spawn_crystal()

    keys = pygame.key.get_pressed()
    player.update(keys) 
    asteroids.update()  
    crystals.update()   

    if pygame.sprite.spritecollide(player, asteroids, True):
        clash_sound.play()
        print("Collision with asteroid!")
        running = False

    if pygame.sprite.spritecollide(player, crystals, True):
        print("Crystal collected!")
        score += 10

    all_sprites.draw(screen)
    
    font = pygame.font.SysFont("Arial", 24)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    clock.tick(FPS)


screen.fill(BLACK)
font = pygame.font.SysFont("Arial", 48)
text = font.render("Game Over", True, (255, 0, 0))
score_text = font.render(f"Final Score: {score}", True, WHITE)
screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 3))
screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
pygame.display.flip()

pygame.time.wait(3000)
pygame.quit()
sys.exit()
