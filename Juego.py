import pygame
import numpy as np
import time

#Ancho y Alto de la pantalla.
WIDTH, HEIGHT = 800, 800
nX, nY = 80, 80
xSize = WIDTH/nX
ySize = HEIGHT/nY

pygame.init() # Initialize PyGame

#Creación de la pantalla
screen = pygame.display.set_mode([WIDTH,HEIGHT])

#Color de fondo
BG_COLOR = (10,10,10)
LIVE_COLOR = (255,255,255)
DEAD_COLOR = (128,128,128)
#Estado de las Celdas: Celdas vivas = 1; Celdas muertas = 0
status = np.zeros((nX,nY)) #Inicializar estado de las celdas

pauseRun = False

running = True
while running:

    newStatus = np.copy(status) # Copiar estado

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #Pausa el juego con ENTER
        if event.type == pygame.KEYDOWN:
            pauseRun = not pauseRun
        #Marca la casilla en la que se pulse el clik derecho
        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            x, y = int(np.floor(posX/xSize)), int(np.floor(posY/ySize))
            #newStatus[x,y] = np.abs(newStatus[x,y]-1)
            newStatus[x,y] = not mouseClick[2]
            
    #Limpiar background
    screen.fill(BG_COLOR) 

    for x in range(0,nX):
        for y in range(0,nY):


            if not pauseRun:

                # Calculamos el Numero de vecinos cercanos
                nNeigh = status[(x-1)%nX,(y-1)%nY] + status[(x)%nX,(y-1)%nY] + \
                        status[(x+1)%nX,(y-1)%nY] + status[(x-1)%nX,(y)%nY] + \
                        status[(x+1)%nX,(y)%nY] + status[(x-1)%nX,(y+1)%nY] + \
                         status[(x)%nX,(y+1)%nY] + status[(x+1)%nX,(y+1)%nY]

                #Regla 1: Una celula muerta con 3 vecinas vivas "revive"
                if status[x,y] == 0 and nNeigh==3:
                    newStatus[x,y] = 1

                #Regla 2: Una celula viva con mas de 3 o menos de 2 vecinas vivas "muere"
                elif status[x,y] == 1 and (nNeigh < 2 or nNeigh > 3):
                    newStatus[x,y] = 0

            #Se crea el poligono de cada celda a dibujar
            poly = [(x*xSize,y*ySize),
                    ((x+1)*xSize,y*ySize),
                    ((x+1)*xSize,(y+1)*ySize),
                    (x*xSize,(y+1)*ySize)]
            #Se dibujan las celdas pra cada par de x e y
            if newStatus[x,y] == 1:
                pygame.draw.polygon(screen,LIVE_COLOR,poly,0)
            else:
                pygame.draw.polygon(screen,DEAD_COLOR,poly,1)
    #Se actualiza el estado
    status = np.copy(newStatus)
    time.sleep(0.1)
    pygame.display.flip()


pygame.quit()
