from pickle import FALSE
import pygame
from random import randint

pygame.init()
pygame.mixer.init()
mw = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.mixer.music.load("background_music.wav")
pygame.mixer.music.play()
runtime = True


class Label:
    def __init__(self, text, x=0, y=0, color=(0, 0, 0), size=14):
        self.size = size
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont("roboto", size)
        self.text = self.font.render(text, False, color)

    def draw(self, window):
        window.blit(self.text, (self.x, self.y))


class Sprite(pygame.sprite.Sprite):
    def __init__(self, filename, x=0, y=0):
        super().__init__()
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, window):
        window.blit(self.image, self.rect)

    def flip(self, flip_x, flip_y):
        img_copy = self.image.copy()
        self.image = pygame.transform.flip(img_copy, flip_x, flip_y)
    
    def resize(self, width, height):
        img_copy = self.image.copy()
        x = self.rect.x
        y = self.rect.y
        self.image = pygame.transform.scale(img_copy, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw_hitbox(self, thickness):
        pygame.draw.rect(mw, (255, 0, 0), self.rect, thickness)


class Character(Sprite):
    def __init__(self, filename, speed=1):
        super().__init__(filename)
        self.speed = speed
        self.right_view = True
        self.is_ground = False

    def move(self, keys):
        if keys[pygame.K_a]:
            if self.right_view:
                self.right_view = False
                self.flip(1, 0)
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            if not self.right_view:
                self.right_view = True
                self.flip(1, 0)
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            pass
        if not self.is_ground:
            self.rect.y += self.speed

    def check_ground(self, platforms):
        self.is_ground = False
        for p in platforms:
            if self.rect.colliderect(p.rect):
                self.is_ground = True
                break



star = Character('star.png', 4)
bg = Sprite("background.png")
score = Label("0", 10, 10, (255,255,255), 70)

# создание платформ
p = Sprite('platform.png', 0, 690)
p.resize(1280, 20)
platforms = [p]

while runtime: 
    bg.draw(mw)
    star.draw(mw)
    # star.draw_hitbox(2)
    score.draw(mw)
    for p in platforms:
        p.draw(mw)

    events = pygame.event.get()
    star.move(pygame.key.get_pressed())
    star.check_ground(platforms)
    for event in events:
        if event.type == pygame.QUIT:
            runtime = False

    clock.tick(60)
    pygame.display.update()
