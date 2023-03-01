import pygame
from random import randint


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        image1 = pygame.image.load("sprites/yellowbird-upflap.png").convert_alpha()
        image2 = pygame.image.load("sprites/yellowbird-midflap.png").convert_alpha()
        image3 = pygame.image.load("sprites/yellowbird-downflap.png").convert_alpha()
        self.bird_move = [image1, image2, image3]
        self.bird_index = 0
        self.image = pygame.transform.scale2x(self.bird_move[int(self.bird_index)])
        self.rect = self.image.get_rect(midright=(198, 300))
        self.bird_gravity = 0
        self.jump_sound = pygame.mixer.Sound("audio/wing.ogg")

    def animation(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            self.bird_index = 0
        else:
            self.bird_index += 0.1
            if self.bird_index >= len(self.bird_move):
                self.bird_index = 2
        self.image = pygame.transform.scale2x(self.bird_move[int(self.bird_index)])

    def bird_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.bird_gravity = -10
            self.jump_sound.play()

    def gravity(self):
        self.bird_gravity += 0.6
        self.rect.y += self.bird_gravity
        if self.rect.top <= 0:
            self.rect.top = 0

    def update(self):
        self.gravity()
        self.bird_input()
        self.animation()


class Pipe(pygame.sprite.Sprite):
    def __init__(self, p_type, y_pos1=None):
        super().__init__()

        image = pygame.image.load("sprites/pipe-green.png").convert_alpha()

        if p_type == "pipe":
            self.y_pos = randint(-100, 300)
            image = pygame.transform.rotozoom(image, 180, 2)

        elif not p_type:
            self.y_pos = 900 + y_pos1
            image = pygame.transform.rotozoom(image, 0, 2)

        self.image = image
        self.rect = self.image.get_rect(midleft=(600, self.y_pos))

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.rect.x -= 5
        self.destroy()
