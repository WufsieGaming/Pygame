import pygame
import os
pygame.font.init()
pygame.mixer.init()
pygame.init()

img = pygame.image.load(os.path.join('Assets', 'icon.png'))
pygame.display.set_icon(img)
running = True

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Anime Invaders") #name of my game

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

BORDER = pygame.Rect(0, HEIGHT//2 - 5, WIDTH, 10) #border becomes horizontal instead of vertical


BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'vine.mp3' ))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets','pew.mp3' ))

HEALTH_FONT = pygame.font.SysFont('arial.ttf', 40) #font change for the game
WINNER_FONT = pygame.font.SysFont('arial.ttf', 100)

FPS = 29.97 #i used a 29.97 frame rate ratio as the game doesn't require high fps
BULLET_VEL = 5
MAX_BULLETS = 10 #since the game is basic, 10 bullets should make the game fun and competitive.
VEL = 5

NARUTO_HIT = pygame.USEREVENT + 1
GOKU_HIT = pygame.USEREVENT + 2

NARUTO_CHARACTER = pygame.image.load(os.path.join('Assets', 'naruto.png')) #anime character 1 (naruto)
NARUTO = pygame.transform.rotate(pygame.transform.scale(NARUTO_CHARACTER, (100, 100)), 0) 


GOKU_CHARACTER = pygame.image.load(os.path.join('Assets', 'goku.png')) #anime character 2 (goku)
GOKU = pygame.transform.rotate(pygame.transform.scale(GOKU_CHARACTER, (100, 100)), 180)

ANIMEFIELD = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'animefield.jpg')), (WIDTH, HEIGHT))

def draw_window(naruto, goku, goku_bullets, naruto_bullets, goku_health, naruto_health):
    WIN.fill(BLUE)
    WIN.blit(ANIMEFIELD, (0, 0))
    pygame.draw.rect(WIN, WHITE, BORDER) #border
    goku_health_text = HEALTH_FONT.render("Health: " + str(goku_health), 1, BLACK)
    naruto_health_text = HEALTH_FONT.render("Health: " + str(naruto_health), 1, YELLOW)
    WIN.blit(goku_health_text, (WIDTH - goku_health_text.get_width() - 10, 10))
    WIN.blit(naruto_health_text, (10, HEIGHT - naruto_health_text.get_height()- 10,)) #health for both sides


    WIN.blit(NARUTO, (naruto.x, naruto.y))
    WIN.blit(GOKU, (goku.x, goku.y))

    for bullet in goku_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    for bullet in naruto_bullets:
        pygame.draw.rect(WIN, BLACK, bullet)

    pygame.display.update()

#movement controls
def black_handle_movement(keys_pressed, naruto):
    if keys_pressed[pygame.K_a] and naruto.x - VEL > 0:  #LEFT
        naruto.x -= VEL
    if keys_pressed[pygame.K_d] and naruto.x + VEL + 70 < WIDTH : #RIGHT
        naruto.x += VEL
    if keys_pressed[pygame.K_w] and naruto.y - VEL > 0:  #UP
        naruto.y -= VEL
    if keys_pressed[pygame.K_s] and naruto.y - VEL < BORDER.y - 70:  #DOWN
        naruto.y += VEL


def yellow_handle_movement(keys_pressed, goku):
    if keys_pressed[pygame.K_LEFT] and goku.x - VEL > 0 :   #LEFT
        goku.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and goku.x + VEL + 70 < WIDTH:  #RIGHT
        goku.x += VEL
    if keys_pressed[pygame.K_UP] and goku.y + VEL > BORDER.y - 15:  #UP
        goku.y -= VEL
    if keys_pressed[pygame.K_DOWN] and goku.y + VEL + 95 < HEIGHT:  #DOWN
        goku.y += VEL


def handle_bullets(naruto_bullets, goku_bullets, naruto, goku):
    for bullet in naruto_bullets:
        bullet.y -= BULLET_VEL
        if goku.colliderect(bullet):
            pygame.event.post(pygame.event.Event(GOKU_HIT))
            naruto_bullets.remove(bullet)
        elif bullet.y > HEIGHT:
            naruto_bullets.remove(bullet)

    for bullet in goku_bullets:
        bullet.y += BULLET_VEL
        if naruto.colliderect(bullet):
            pygame.event.post(pygame.event.Event(NARUTO_HIT))
            goku_bullets.remove(bullet)
        elif bullet.y < 0:
            goku_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    goku = pygame.Rect(600, 50, 70, 75)
    naruto = pygame.Rect(600, 550, 135, 80)

    goku_bullets = []
    naruto_bullets = []

    goku_health = 25 #health
    naruto_health = 25

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            #shooting controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL and len(naruto_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(naruto.x + naruto.width//2, naruto.y + naruto.height - 2, 10, 5)
                    naruto_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_LCTRL and len(goku_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(goku.x + 40, goku.y + 30 - 2, 10, 5)
                    goku_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == GOKU_HIT:
                goku_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == NARUTO_HIT:
                naruto_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if goku_health <= 0:
            winner_text = "GOKU WINS!" #if goku wins

        if naruto_health <= 0:
            winner_text = "NARUTO WINS!" #if naruto wins

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, naruto)
        black_handle_movement(keys_pressed, goku)

        handle_bullets(naruto_bullets, goku_bullets, naruto, goku)



        draw_window(goku, naruto, goku_bullets, naruto_bullets,
                    goku_health, naruto_health)

    main()
#loop


if __name__ == "__main__":
    main()