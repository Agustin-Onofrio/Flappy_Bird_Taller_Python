
# Import module
import random
import sys
import pygame
from pygame.locals import *
  
# All the Game Variables
ANCHO_VENTANA = 600
ALTO_VENTANA = 499
  
# set height and width of window
window = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
elevation = ALTO_VENTANA 
game_images = {}
VELOCIDAD_INICIAL = 32
VELOCIDAD_MEDIA=50
VELOCIDAD_DIFICIL=70
pipeimage = 'images/pipe.png'
IMAGEN_FONDO = 'images/background.jpg'
IMAGEN_JUGADOR = 'images/bird.png'
# sealevel_image = 'images/base.jfif'
  
  
def flappygame():
    your_score = 0
    horizontal = int(ANCHO_VENTANA/5)
    vertical = int(ANCHO_VENTANA/2)
    ground = 0
    mytempheight = 100
    velocidad=VELOCIDAD_INICIAL
  
    # Generating two pipes for blitting on window
    first_pipe = createPipe()
    second_pipe = createPipe()
  
    # List containing lower pipes
    down_pipes = [
        {'x': ANCHO_VENTANA+300-mytempheight,
         'y': first_pipe[1]['y']},
        {'x': ANCHO_VENTANA+300-mytempheight+(ANCHO_VENTANA/2),
         'y': second_pipe[1]['y']},
    ]
  
    # List Containing upper pipes
    up_pipes = [
        {'x': ANCHO_VENTANA+300-mytempheight,
         'y': first_pipe[0]['y']},
        {'x': ANCHO_VENTANA+200-mytempheight+(ANCHO_VENTANA/2),
         'y': second_pipe[0]['y']},
    ]
  
    # pipe velocity along x
    pipeVelX = -4
  
    # bird velocity
    bird_velocity_y = -9
    bird_Max_Vel_Y = 10
    bird_Min_Vel_Y = -8
    birdAccY = 1
  
    bird_flap_velocity = -8
    bird_flapped = False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if vertical > 0:
                    bird_velocity_y = bird_flap_velocity
                    bird_flapped = True
  
        # This function will return true
        # if the flappybird is crashed
        game_over = isGameOver(horizontal,
                               vertical,
                               up_pipes,
                               down_pipes)
        if game_over:
            mostrarPerdiste()
            return
  
        # check for your_score
        playerMidPos = horizontal + game_images['flappybird'].get_width()/2
        for pipe in up_pipes:
            pipeMidPos = pipe['x'] + game_images['pipeimage'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                your_score += 1
                print(f"Your your_score is {your_score}")
  
        if bird_velocity_y < bird_Max_Vel_Y and not bird_flapped:
            bird_velocity_y += birdAccY
  
        if bird_flapped:
            bird_flapped = False
        playerHeight = game_images['flappybird'].get_height()
        vertical = vertical + \
            min(bird_velocity_y, elevation - vertical - playerHeight)
  
        # move pipes to the left
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX
  
        # Add a new pipe when the first is
        # about to cross the leftmost part of the screen
        if 0 < up_pipes[0]['x'] < 5:
            newpipe = createPipe()
            up_pipes.append(newpipe[0])
            down_pipes.append(newpipe[1])
  
        # if the pipe is out of the screen, remove it
        if up_pipes[0]['x'] < -game_images['pipeimage'][0].get_width():
            up_pipes.pop(0)
            down_pipes.pop(0)
  
        # Lets blit our game images now
        window.blit(game_images['background'], (0, 0))
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            window.blit(game_images['pipeimage'][0],
                        (upperPipe['x'], upperPipe['y']))
            window.blit(game_images['pipeimage'][1],
                        (lowerPipe['x'], lowerPipe['y']))
  
        # window.blit(game_images['sea_level'], (ground, elevation))
        window.blit(game_images['flappybird'], (horizontal, vertical))
  
        # Fetching the digits of score.
        numbers = [int(x) for x in list(str(your_score))]
        width = 0
  
        # finding the width of score images from numbers.
        for num in numbers:
            width += game_images['scoreimages'][num].get_width()
        Xoffset = (ANCHO_VENTANA - width)/1.1
  
        # Blitting the images on the window.
        for num in numbers:
            window.blit(game_images['scoreimages'][num],
                        (Xoffset, ANCHO_VENTANA*0.02))
            Xoffset += game_images['scoreimages'][num].get_width()
  
        # Refreshing the game window and displaying the score.
        pygame.display.update()
        framepersecond_clock.tick(velocidad)
        if(your_score>3):
            velocidad=VELOCIDAD_MEDIA
            if(your_score>6):
                velocidad=VELOCIDAD_DIFICIL
  
  
def isGameOver(horizontal, vertical, up_pipes, down_pipes):
    if vertical > elevation -50  or vertical < 0:
        return True
  
    for pipe in up_pipes:
        pipeHeight = game_images['pipeimage'][0].get_height()
        if(vertical < pipeHeight + pipe['y'] and\
           abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width()):
            return True
  
    for pipe in down_pipes:
        if (vertical + game_images['flappybird'].get_height() > pipe['y']) and\
        abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width():
            return True
    return False
  
  
def createPipe():
    offset = ALTO_VENTANA/3
    pipeHeight = game_images['pipeimage'][0].get_height()
    y2 = offset + \
        random.randrange(
            # 0, int(ALTO_VENTANA - game_images['sea_level'].get_height() - 1.2 * offset))  
            0, int(ALTO_VENTANA - 0 - 1.2 * offset))
    pipeX = ANCHO_VENTANA + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        # upper Pipe
        {'x': pipeX, 'y': -y1},
  
        # lower Pipe
        {'x': pipeX, 'y': y2}
    ]
    return pipe
  
def mostrarPerdiste():
    print("PERDISTE")
    pass


  
# program where the game starts
if __name__ == "__main__":
  
        # For initializing modules of pygame library
    pygame.init()
    framepersecond_clock = pygame.time.Clock()
  
    # Sets the title on top of game window
    pygame.display.set_caption('Flappy Bird Game')
  
    # Load all the images which we will use in the game
  
    # images for displaying score
    game_images['scoreimages'] = (
        pygame.image.load('images/0.png').convert_alpha(),
        pygame.image.load('images/1.png').convert_alpha(),
        pygame.image.load('images/2.png').convert_alpha(),
        pygame.image.load('images/3.png').convert_alpha(),
        pygame.image.load('images/4.png').convert_alpha(),
        pygame.image.load('images/5.png').convert_alpha(),
        pygame.image.load('images/6.png').convert_alpha(),
        pygame.image.load('images/7.png').convert_alpha(),
        pygame.image.load('images/8.png').convert_alpha(),
        pygame.image.load('images/9.png').convert_alpha()
    )
    game_images['flappybird'] = pygame.image.load(
        IMAGEN_JUGADOR).convert_alpha()
    # game_images['sea_level'] = pygame.image.load(
    #     sealevel_image).convert_alpha()
    game_images['background'] = pygame.image.load(
        IMAGEN_FONDO).convert_alpha()
    game_images['pipeimage'] = (pygame.transform.rotate(pygame.image.load(
        pipeimage).convert_alpha(), 180), pygame.image.load(
      pipeimage).convert_alpha())
  
    print("WELCOME TO THE FLAPPY BIRD GAME")
    print("Press space or enter to start the game")
    
    
    # Here starts the main game
  
    while True:
  
        # sets the coordinates of flappy bird
  
        horizontal = int(ANCHO_VENTANA/5)
        vertical = int(
            (ALTO_VENTANA - game_images['flappybird'].get_height())/2)
        ground = 100
        print("Comienzo del juego!")
        while True:
            for event in pygame.event.get():
  
                # if user clicks on cross button, close the game
                if event.type == QUIT or (event.type == KEYDOWN and \
                                          event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
  
                # If the user presses space or
                # up key, start the game for them
                elif event.type == KEYDOWN and (event.key == K_SPACE or\
                                                event.key == K_UP):
                    flappygame()
  
                # if user doesn't press anykey Nothing happen
                else:
                    window.blit(game_images['background'], (0, 0))
                    window.blit(game_images['flappybird'],
                                (horizontal, vertical))
                    # window.blit(game_images['sea_level'], (ground, elevation))
                    pygame.display.update()
                    framepersecond_clock.tick(VELOCIDAD_INICIAL)