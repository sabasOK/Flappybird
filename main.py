import pygame
from sys import exit
from sprites import Bird, Pipe


def collision_sprite():
    if pygame.sprite.spritecollide(bird.sprite, pipe_group, False):
        hit_sound.play()
        pipe_group.empty()
        bird.add(Bird())
        return False
    if bird.sprite.rect.y >= 950:
        fall_sound.play()
        pipe_group.empty()
        bird.add(Bird())
        return False
    else:
        return True


def score_draw():
    if game_active:
        score_surf = font.render(f"Score:{int(score)}", False, "Black")
        score_rect = score_surf.get_rect(center=(100, 50))
        screen.blit(score_surf, score_rect)
    else:
        score_surf = font.render(f"Score:{int(score)}", False, "Black")
        score_rect = score_surf.get_rect(center=(576 / 2, 1024 / 1.6))
        screen.blit(score_surf, score_rect)


def score_check():
    global score
    if pipe_group:
        for sprite in pipe_group:
            if sprite.rect.x == 130:
                score += 0.5


pygame.init()
screen = pygame.display.set_mode((576, 1024))
pygame.display.set_caption("FlappyBird")
clock = pygame.time.Clock()
font = pygame.font.Font("game/Pixeltype.ttf", 50)
game_active = False
score = 0
hit_sound = pygame.mixer.Sound("game/audio/hit.wav")
fall_sound = pygame.mixer.Sound("game/audio/die.wav")

# Groups

pipe_group = pygame.sprite.Group()
bird = pygame.sprite.GroupSingle()
bird.add(Bird())

# Background
bg_surf = pygame.image.load("game/sprites/background-night.png").convert()
bg_surf = pygame.transform.scale(bg_surf, (screen.get_width(), screen.get_height()))

ground = pygame.image.load("game/sprites/base.png").convert()
ground = pygame.transform.scale(ground, (screen.get_width(), ground.get_height()))
groundx = 0

# Intro screen
start_surf = pygame.image.load("game/sprites/flappybird.png").convert_alpha()
start_surf = pygame.transform.rotozoom(start_surf, 0, 2)
start_rect = start_surf.get_rect(center=(576 / 2, 1024 / 2.2))
start_text_surf = font.render(f" pres ENTER to start", False, "Black")
start_text_rect = start_text_surf.get_rect(center=(576 / 2, 1024 / 1.8))

# Game over screen
game_over_surf = pygame.image.load("game/sprites/gameover.png").convert_alpha()
game_over_surf = pygame.transform.rotozoom(game_over_surf, 0, 2)
game_over_rect = game_over_surf.get_rect(center=(576 / 2, 1024 / 2.2))
over_text_surf = font.render(f"pres ENTER to restart", False, "Black")
over_text_rect = over_text_surf.get_rect(center=(576 / 2, 1024 / 1.8))

# Timer
pipe_timer = pygame.USEREVENT + 1
pygame.time.set_timer(pipe_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pipe_timer:
                pipe = Pipe("pipe")
                pipe_group.add(pipe)
                pipe_group.add(Pipe("", pipe.y_pos))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_active = True
                score = 0

    if game_active:
        screen.blit(bg_surf, (0, 0))
        screen.blit(ground, (groundx, 950))
        screen.blit(ground, (groundx + screen.get_width(), 950))
        groundx -= 1
        if abs(groundx) == screen.get_width():
            groundx = 0
        bird.draw(screen)
        bird.update()
        pipe_group.draw(screen)
        pipe_group.update()
        score_check()
        score_draw()
        game_active = collision_sprite()

    else:
        screen.blit(bg_surf, (0, 0))
        if score == 0:
            screen.blit(start_surf, start_rect)
            screen.blit(start_text_surf, start_text_rect)
        else:
            screen.blit(game_over_surf, game_over_rect)
            screen.blit(over_text_surf, over_text_rect)
            score_draw()

    pygame.display.update()
    clock.tick(60)
