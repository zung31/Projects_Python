import os
import pygame
pygame.font.init() # initialize font module
pygame.mixer.init() # initialize sound effect

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # create a screen
pygame.display.set_caption("Spaceship Battle Game") # set title of game window

HEALTH_FONT = pygame.font.SysFont('comicsans', 40) # define font wanna use
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('C:\\', 'Users', 'zungh', 'Desktop', 'Python programs', 'PyGame_Spaceships', 'Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('C:\\', 'Users', 'zungh', 'Desktop', 'Python programs', 'PyGame_Spaceships', 'Assets', 'Gun+Silencer.mp3'))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
VEL = 5 # move 5 pixels per frame
BULLET_VEL = 7; # bullet speed
MAX_BULLETS = 3;
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT) # create a border in the middle of screen (10: width of border)
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('C:\\', 'Users', 'zungh', 'Desktop', 'Python programs', 'PyGame_Spaceships', 'Assets', 'spaceship_yellow.png'))
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('C:\\', 'Users', 'zungh', 'Desktop', 'Python programs', 'PyGame_Spaceships', 'Assets', 'spaceship_red.png'))
#scale :resize spaceship and rotate: rotate spaceship
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

YELLOW_HIT = pygame.USEREVENT + 1 # create a custom event
RED_HIT = pygame.USEREVENT + 2

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('C:\\', 'Users', 'zungh', 'Desktop', 'Python programs', 'PyGame_Spaceships', 'Assets', 'space.jpg')),(WIDTH,HEIGHT))

FPS = 60 # frame update per second (to make game run smoothly and not too fast in all computers)


def draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health):
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER) # draw border on the screen using black color

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE) # alwways put 1 in the second argument
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10)) # draw health text on the screen
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x,yellow.y)) # (position top left corner of image, (x, y)
    WIN.blit(RED_SPACESHIP, (red.x,red.y)) # draw red spaceship on the surface screen

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update() # update the screen

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x -VEL >0: #LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width <BORDER.x: #RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL >0: #UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15: #DOWN
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x +15: #LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + 40 < WIDTH: # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL >0: #UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y +VEL +red.height < HEIGHT -15: #DOWN
        red.y += VEL

def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    # check collide
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet): # check collide func
            pygame.event.post(pygame.event.Event(RED_HIT)) # create a custom event to use it later in our main loop
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH: # check if bullet is out of screen
            yellow_bullets.remove(bullet)
    
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

# draw winnner text, update and restart game
def draw_winner(text):
    WINNER_TEXT = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(WINNER_TEXT, (WIDTH//2 - WINNER_TEXT.get_width()//2, HEIGHT//2 - WINNER_TEXT.get_height()//2)) # draw winner text in the middle of screen
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) # create rectangle for red spaceship
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) # create rectangle for yellow spaceship
    red_bullets = []
    yellow_bullets = []

    red_heatlh = 10
    yellow_health = 10

    clock = pygame.time.Clock() # create a clock object to control FPS
    run = True
    while run:
        clock.tick(FPS) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # check if user click close button
                run = False
                pygame.quit() # exit game when done

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets)< MAX_BULLETS: # create bullet
                    # cause top left so we need to add width and height to get the center of spaceship so the bullet will come out at the head spaceship?
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5) 
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets)< MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5) 
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            #check if the bullet hit the spaceship
            if event.type == RED_HIT:
                red_heatlh -=1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -=1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_heatlh <=0:
            winner_text = "Yellow Wins!"

        if yellow_health <=0:
            winner_text = "Red Wins!"
        if winner_text != "":
            draw_winner(winner_text)
            break

        print(red_bullets,yellow_bullets)
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red) 
        
        handle_bullets(yellow_bullets,red_bullets,yellow,red)

        draw_window(red,yellow,red_bullets,yellow_bullets,red_heatlh,yellow_health)
    #pygame.quit() # exit game when done
    main() # restart game

if(__name__ == "__main__"): # only want to run main function when this file is run
    main() # run main function