
# Import module
import random
import sys
import pygame
from pygame.locals import *
  
# All the Game Variables
ANCHO_VENTANA = 600
ALTO_VENTANA = 499
  
# set height and width of window
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
elevacion = ALTO_VENTANA 
imagenes_del_juego = {}
VELOCIDAD_INICIAL = 32
VELOCIDAD_MEDIA=50
VELOCIDAD_DIFICIL=70
IMAGEN_TUBO = 'images/pipe.png'
IMAGEN_FONDO = 'images/background.jpg'
IMAGEN_JUGADOR_PAJARO = 'images/bird.png'
IMAGEN_JUGADOR_NICOLAS = 'images/nicolas.png'
IMAGEN_JUGADOR_GUSTAVO = 'images/gustavo.png'
IMAGEN_JUGADOR_FRANCO = 'images/franco.png'
# sealevel_image = 'images/base.jfif'
  
  
def flappygame():
    puntaje = 0
    horizontal = int(ANCHO_VENTANA/5)
    vertical = int(ANCHO_VENTANA/2)
    piso = 0
    mytempheight = 100
    velocidad=VELOCIDAD_INICIAL
  
    # Generating two pipes for blitting on window
    primer_tubo = crearTubo()
    segundo_tubo = crearTubo()
  
    # List containing lower pipes
    tubo_inferior = [
        {'x': ANCHO_VENTANA+300-mytempheight,
         'y': primer_tubo[1]['y']},
        {'x': ANCHO_VENTANA+300-mytempheight+(ANCHO_VENTANA/2),
         'y': segundo_tubo[1]['y']},
    ]
  
    # List Containing upper pipes
    tubo_superior = [
        {'x': ANCHO_VENTANA+300-mytempheight,
         'y': primer_tubo[0]['y']},
        {'x': ANCHO_VENTANA+200-mytempheight+(ANCHO_VENTANA/2),
         'y': segundo_tubo[0]['y']},
    ]
  
    # pipe velocity along x
    velocidad_tubo_x = -4
  
    # bird velocity
    velocidad_pajaro_y = -9
    velocidad_pajaro_x = 10
    bird_Min_Vel_Y = -8
    birdAccY = 1
  
    velocidad_salto_pajaro = -8
    bird_flapped = False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if vertical > 0:
                    velocidad_pajaro_y = velocidad_salto_pajaro
                    bird_flapped = True
  
        # This function will return true
        # if the flappybird is crashed
        game_over = isGameOver(horizontal,
                               vertical,
                               tubo_superior,
                               tubo_inferior)
        if game_over:
            mostrarPerdiste()
            return
  
        # check for your_score
        playerMidPos = horizontal + imagen_personaje.get_width()/2
        for pipe in tubo_superior:
            pipeMidPos = pipe['x'] + imagen_tubo_inferior.get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                puntaje += 1
                print(f"Your your_score is {puntaje}")
  
        if velocidad_pajaro_y < velocidad_pajaro_x and not bird_flapped:
            velocidad_pajaro_y += birdAccY
  
        if bird_flapped:
            bird_flapped = False
        playerHeight = imagen_personaje.get_height()
        vertical = vertical + \
            min(velocidad_pajaro_y, elevacion - vertical - playerHeight)
  
        # move pipes to the left
        for upperPipe, lowerPipe in zip(tubo_superior, tubo_inferior):
            upperPipe['x'] += velocidad_tubo_x
            lowerPipe['x'] += velocidad_tubo_x
  
        # Add a new pipe when the first is
        # about to cross the leftmost part of the screen
        if 0 < tubo_superior[0]['x'] < 5:
            newpipe = crearTubo()
            tubo_superior.append(newpipe[0])
            tubo_inferior.append(newpipe[1])
  
        # if the pipe is out of the screen, remove it
        if tubo_superior[0]['x'] < -imagen_tubo_inferior.get_width():
            tubo_superior.pop(0)
            tubo_inferior.pop(0)
  
        # Lets blit our game images now
        ventana.blit(imagen_fondo, (0, 0))
        for upperPipe, lowerPipe in zip(tubo_superior, tubo_inferior):
            ventana.blit(imagen_tubo_inferior,
                        (upperPipe['x'], upperPipe['y']))
            ventana.blit(imagen_tubo_superior,
                        (lowerPipe['x'], lowerPipe['y']))
  
        # window.blit(game_images['sea_level'], (ground, elevation))
        ventana.blit(imagen_personaje, (horizontal, vertical))
  
        mostrar_puntaje(puntaje)
        # Refreshing the game window and displaying the score.
        pygame.display.update()
        fps.tick(velocidad)
        if(puntaje>3):
            velocidad=VELOCIDAD_MEDIA
            if(puntaje>6):
                velocidad=VELOCIDAD_DIFICIL
  
  
def isGameOver(horizontal, vertical, up_pipes, down_pipes):
    if vertical > elevacion -50  or vertical < 0:
        return True
  
    for pipe in up_pipes:
        pipeHeight = imagen_tubo_inferior.get_height()
        if(vertical < pipeHeight + pipe['y'] and\
           abs(horizontal - pipe['x']) < imagen_tubo_inferior.get_width()):
            return True
  
    for pipe in down_pipes:
        if (vertical + imagen_personaje.get_height() > pipe['y']) and\
        abs(horizontal - pipe['x']) < imagen_tubo_inferior.get_width():
            return True
    return False

def mostrar_puntaje(puntaje):
    # Se hace una lista con los digitos del puntaje obtenido
        numbers = [int(x) for x in list(str(puntaje))]
        width = 0
    

        # Calcula el ancho del numero a mostrar
        for num in numbers:
            imagen_del_digito=imagenDigito(num)
            width += imagen_del_digito.get_width()
        Xoffset = (ANCHO_VENTANA - width)/1.1
  
        # Por cada digito muestra la imagen correspondiente
        for num in numbers:
            imagen_del_digito=imagenDigito(num)
            ventana.blit(imagen_del_digito,
                        (Xoffset, ANCHO_VENTANA*0.02))
            Xoffset += imagen_del_digito.get_width()
  

def imagenDigito(digito):
    imagen=""
    if digito==0:
        imagen=pygame.image.load('images/0.png').convert_alpha()
    elif digito==1:
        imagen=pygame.image.load('images/1.png').convert_alpha()
    elif digito==2:
        imagen=pygame.image.load('images/2.png').convert_alpha()
    elif digito==3:
        imagen=pygame.image.load('images/3.png').convert_alpha()
    elif digito==4:
        imagen=pygame.image.load('images/4.png').convert_alpha()
    elif digito==5:
        imagen=pygame.image.load('images/5.png').convert_alpha()
    elif digito==6:
        imagen=pygame.image.load('images/6.png').convert_alpha()
    elif digito==7:
        imagen=pygame.image.load('images/7.png').convert_alpha()
    elif digito==8:
        imagen=pygame.image.load('images/8.png').convert_alpha()
    elif digito==9:
        imagen=pygame.image.load('images/9.png').convert_alpha()
    
    return imagen




  
def crearTubo():
    pasaje = ALTO_VENTANA/3
    pipeHeight = imagen_tubo_inferior.get_height()
    y2 = pasaje + \
        random.randrange(
            # 0, int(ALTO_VENTANA - game_images['sea_level'].get_height() - 1.2 * offset))  
            0, int(ALTO_VENTANA - 0 - 1.2 * pasaje))
    pipeX = ANCHO_VENTANA + 10
    y1 = pipeHeight - y2 + pasaje
    pipe = [
        # upper Pipe
        {'x': pipeX, 'y': -y1},
  
        # lower Pipe
        {'x': pipeX, 'y': y2}
    ]
    return pipe
  
def mostrarPerdiste():
    print("PERDISTE")
    return


def elegirPersonaje():

    print(
        '''Ingresa el personaje con el que queres jugar
        1-Pajaro
        2-Nicolas
        3-Gustavo
        4-Franco''')


    opcion=int(input())

    if opcion==1:
        imagen = pygame.image.load(IMAGEN_JUGADOR_PAJARO).convert_alpha()
    elif opcion==2:
        imagen = pygame.image.load(IMAGEN_JUGADOR_NICOLAS).convert_alpha()
    elif opcion==3:
        imagen = pygame.image.load(IMAGEN_JUGADOR_GUSTAVO).convert_alpha()
    elif opcion==4:
        imagen = pygame.image.load(IMAGEN_JUGADOR_FRANCO).convert_alpha()

    return imagen





  
# Ejecucion principal
if __name__ == "__main__":
  
    # Inicializo pygame
    pygame.init()
    fps = pygame.time.Clock()
  
    # Pongo titulo a la ventana
    pygame.display.set_caption('Flappy Bird Game')
  
    
    imagen_personaje = elegirPersonaje()
    # game_images['sea_level'] = pygame.image.load(
    #     sealevel_image).convert_alpha()
    imagen_fondo = pygame.image.load(IMAGEN_FONDO).convert_alpha()
    
    # imagen_de_los_tubos = (pygame.transform.rotate(pygame.image.load(IMAGEN_TUBO).convert_alpha(), 180), pygame.image.load(IMAGEN_TUBO).convert_alpha())
    #Cargo las imagenes de los tubos
    imagen_tubo_inferior=pygame.transform.rotate(pygame.image.load(IMAGEN_TUBO).convert_alpha(), 180)
    imagen_tubo_superior=pygame.image.load(IMAGEN_TUBO).convert_alpha()
  
    print("Bienvenido al juego de Flappy bird")
    print("Presiona enter para continuar")
    
    
    # Comienzo del juego
    while True:
  
        #Seteo la posicion inicial del personaje
  
        horizontal = int(ANCHO_VENTANA/5)
        vertical = int(
            (ALTO_VENTANA - imagen_personaje.get_height())/2)
        ground = 100
        print("Comienzo del juego!")
        while True:
            for event in pygame.event.get():
  
                # Si aprieta salir de la ventana se para el programa
                if event.type == QUIT or (event.type == KEYDOWN and \
                                          event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
  
                #Si aprieta espacio o la flecha hacia arriba comienza el juego
                elif event.type == KEYDOWN and (event.key == K_SPACE or\
                                                event.key == K_UP):
                    flappygame()
  
                #Si no pasa nada de lo anterior la pantalla no cambia
                else:
                    ventana.blit(imagen_fondo, (0, 0))
                    ventana.blit(imagen_personaje,
                                (horizontal, vertical))
                    # window.blit(game_images['sea_level'], (ground, elevation))
                    pygame.display.update()
                    fps.tick(VELOCIDAD_INICIAL)