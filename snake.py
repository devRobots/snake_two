# Description: Snake game
# Este juego de snake crea muros en el mapa cadad vez que la serpiente come una manzana

import pygame, sys, random
from pygame.locals import *

# Constantes
ANCHOVENTANA = 640
ALTOVENTANA = 480
TAMANHOCUADRO = 20
ANCHOVENTANACUADROS = int(ANCHOVENTANA / TAMANHOCUADRO)
ALTOVENTANACUADROS = int(ALTOVENTANA / TAMANHOCUADRO)
FPS = 10

# Colores
COLOR_SNAKE = (0, 255, 0)
COLOR_COMIDA = (255, 0, 0)
COLOR_FONDO = (0, 0, 0)
COLOR_BORDE = (100, 100, 100)
COLOR_POWERUP = (255, 255, 0)

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    # Inicializa pygame
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((ANCHOVENTANA, ALTOVENTANA))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Snake')

    mostrarPantallaInicio()
    while True:
        ejecutarJuego()
        mostrarPantallaFinal()


def ejecutarJuego():
    # Inicializa la posicion de la serpiente
    serpiente = [{'x': 5, 'y': 5},
                {'x': 4, 'y': 5},
                {'x': 3, 'y': 5},
                {'x': 2, 'y': 5},
                {'x': 1, 'y': 5}]
    direccion = 'derecha'

    # Inicializa la posicion de la comida
    comida = obtenerPosicionAleatoria()

    # Inicializa el puntaje
    puntaje = 0

    # Inicializa los muros
    muros = []

    while True:  # Loop principal del juego
        for event in pygame.event.get():  # Loop de manejo de eventos
            if event.type == QUIT:
                terminar()

            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direccion != 'derecha':
                    direccion = 'izquierda'
                elif (event.key == K_RIGHT or event.key == K_d) and direccion != 'izquierda':
                    direccion = 'derecha'
                elif (event.key == K_UP or event.key == K_w) and direccion != 'abajo':
                    direccion = 'arriba'
                elif (event.key == K_DOWN or event.key == K_s) and direccion != 'arriba':
                    direccion = 'abajo'
                elif event.key == K_ESCAPE:
                    terminar()

        # Verifica si la serpiente ha chocado contra si misma o contra el borde
        if serpiente[0]['x'] == -1 or serpiente[0]['x'] == ANCHOVENTANACUADROS or serpiente[0]['y'] == -1 or \
                serpiente[0]['y'] == ALTOVENTANACUADROS:
            return  # Termina el juego

        for segmento in serpiente[1:]:
            if segmento['x'] == serpiente[0]['x'] and segmento['y'] == serpiente[0]['y']:
                return  # Termina el juego

        # Verifica si la serpiente ha comido la comida
        if serpiente[0]['x'] == comida['x'] and serpiente[0]['y'] == comida['y']:
            muros.append(obtenerPosicionAleatoria())
            comida = obtenerPosicionAleatoria()
            if puntaje % 7 == 0:
                puntaje += 3
            else:
                puntaje += 1
        else:
            del serpiente[-1]
        
        # Verifica si la serpiente ha chocado contra un muro
        for muro in muros:
            if serpiente[0]['x'] == muro['x'] and serpiente[0]['y'] == muro['y']:
                return # Termina el juego

        # Mueve la serpiente
        if direccion == 'arriba':
            nuevoSegmento = {'x': serpiente[0]['x'], 'y': serpiente[0]['y'] - 1}
        elif direccion == 'abajo':
            nuevoSegmento = {'x': serpiente[0]['x'], 'y': serpiente[0]['y'] + 1}
        elif direccion == 'izquierda':
            nuevoSegmento = {'x': serpiente[0]['x'] - 1, 'y': serpiente[0]['y']}
        elif direccion == 'derecha':
            nuevoSegmento = {'x': serpiente[0]['x'] + 1, 'y': serpiente[0]['y']}
        serpiente.insert(0, nuevoSegmento)
        
        # Dibuja el fondo
        DISPLAYSURF.fill(COLOR_FONDO)

        # Dibuja la serpiente
        for segmento in serpiente:
            dibujarCuadro(segmento['x'], segmento['y'], COLOR_SNAKE)

        # Dibuja la comida
        # Puede tener dos colores, dependiendo de si es un powerup o no
        if puntaje % 7 == 0:
            dibujarCuadro(comida['x'], comida['y'], COLOR_POWERUP)
        else:
            dibujarCuadro(comida['x'], comida['y'], COLOR_COMIDA)

        # Dibuja los muros
        for muro in muros:
            dibujarCuadro(muro['x'], muro['y'], COLOR_BORDE)

        # Dibuja el puntaje
        dibujarPuntaje(puntaje)

        # Actualiza la pantalla
        pygame.display.update()
        FPSCLOCK.tick(FPS)



def terminar():
    pygame.quit()
    sys.exit()


def obtenerPosicionAleatoria():
    return {'x': random.randint(0, ANCHOVENTANACUADROS - 1), 'y': random.randint(0, ALTOVENTANACUADROS - 1)}

def dibujarCuadro(x, y, color):
    pygame.draw.rect(DISPLAYSURF, color, (x * TAMANHOCUADRO, y * TAMANHOCUADRO, TAMANHOCUADRO, TAMANHOCUADRO))


def mostrarPantallaInicio():
    # Dibuja el texto de la pantalla de inicio
    tituloFont = pygame.font.Font('freesansbold.ttf', 100)
    tituloSurf = tituloFont.render('Snake!', True, (255, 255, 255))
    tituloRect = tituloSurf.get_rect()
    tituloRect.center = (ANCHOVENTANA / 2, ALTOVENTANA / 2)
    DISPLAYSURF.blit(tituloSurf, tituloRect)

    presioneTeclaFont = pygame.font.Font('freesansbold.ttf', 20)
    presioneTeclaSurf = presioneTeclaFont.render('Presione una tecla para comenzar.', True, (255, 255, 255))
    presioneTeclaRect = presioneTeclaSurf.get_rect()
    presioneTeclaRect.center = (ANCHOVENTANA / 2, ALTOVENTANA / 2 + 100)
    DISPLAYSURF.blit(presioneTeclaSurf, presioneTeclaRect)

    while True:  # Loop de manejo de eventos
        for event in pygame.event.get():  # Loop de manejo de eventos
            if event.type == QUIT:
                terminar()

            elif event.type == KEYDOWN:
                if (event.key == K_ESCAPE):
                    terminar()
                return

        pygame.display.update()
        FPSCLOCK.tick()
    

def mostrarPantallaFinal():
    # Dibuja el texto de la pantalla de inicio
    tituloFont = pygame.font.Font('freesansbold.ttf', 100)
    tituloSurf = tituloFont.render('Game Over', True, (255, 255, 255))
    tituloRect = tituloSurf.get_rect()
    tituloRect.center = (ANCHOVENTANA / 2, ALTOVENTANA / 2)
    DISPLAYSURF.blit(tituloSurf, tituloRect)

    presioneTeclaFont = pygame.font.Font('freesansbold.ttf', 20)
    presioneTeclaSurf = presioneTeclaFont.render('Presione una tecla para volver a jugar.', True, (255, 255, 255))
    presioneTeclaRect = presioneTeclaSurf.get_rect()
    presioneTeclaRect.center = (ANCHOVENTANA / 2, ALTOVENTANA / 2 + 100)
    DISPLAYSURF.blit(presioneTeclaSurf, presioneTeclaRect)

    while True:  # Loop de manejo de eventos
        for event in pygame.event.get():  # Loop de manejo de eventos
            if event.type == QUIT:
                terminar()

            elif event.type == KEYDOWN:
                if (event.key == K_ESCAPE):
                    terminar()
                return

        pygame.display.update()
        FPSCLOCK.tick()


def dibujarPuntaje(puntaje):
    puntajeSurf = BASICFONT.render('Puntaje: %s' % (puntaje), True, (255, 255, 255))
    puntajeRect = puntajeSurf.get_rect()
    puntajeRect.topleft = (ANCHOVENTANA - 120, 10)
    DISPLAYSURF.blit(puntajeSurf, puntajeRect)


if __name__ == '__main__':
    main()

