import pygame
import random
import math
from pygame import mixer
import io

#Funcion convierte fuente
def fuente_bytes(fuente):
    #abrir archivo ttf
    with open(fuente,'rb') as f:
        ttf_bytes = f.read()
    return io.BytesIO(ttf_bytes)

#Funcion fin de juego
def texto_final():
    mi_fuente_final = fuente_final.render("GAME OVER", True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (200, 200))

#Funcion mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))

#Funcion de jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))

#Funcion de enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))

#Funcion disparar bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16 ,y + 10))

#Funcion detectar coliciones
def hay_colision(x_1, y_1, x_2, y_2):
    distacia = math.sqrt(math.pow(x_2 - x_1, 2) + math.pow(y_2 - y_1, 2))
    if distacia < 27:
        return True
    else:
        return False

#Para iniciar a pygame
pygame.init()

#Define el tamaño de la pantalla de pygame
pantalla = pygame.display.set_mode( (800, 600) )

#Imagen de fondo
fondo = pygame.image.load('Fondo.jpg')

#para cambiar el titulo de la pantalla
pygame.display.set_caption("Invasion espacial")

#para cambiar el icono de la pantalla
icono = pygame.image.load("ovni.png")
pygame.display.set_icon(icono)

#Agregar Musica
sonido_fondo = mixer.Sound('MusicaFondo.mp3')
sonido_fondo.set_volume(0.03)
sonido_fondo.play()

#Variables del jugador
img_jugador = pygame.image.load("cohete.png")
jugador_x = 368
jugador_y = 525
jugador_cambio_x = 0.3
ugador_cambio_x = 25

#Variables del enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_cambio_x = []
enemigo_cambio_y = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("enemigo.png"))
    enemigo_x.append(random.randint (0, 736))
    enemigo_y.append(random.randint (50, 200))
    enemigo_cambio_x.append(.5)
    enemigo_cambio_y.append(30)

#Variables de la bala
img_bala = pygame.image.load("bala.png")
bala_x = 0
bala_y = 500
bala_cambio_x = 0
bala_cambio_y = 2
bala_visible = False

#Puntaje
puntaje = 0
#Fuente puntaje
fuente_comicbd_bytes = fuente_bytes("comicbd.ttf")
fuente = pygame.font.Font(fuente_comicbd_bytes,32)
texto_x = 10
texto_y = 10

#Texto fin de juego
fuente_Fastest_bytes = fuente_bytes("Fastest.ttf")
fuente_final = pygame.font.Font(fuente_Fastest_bytes,40)

ejecutar = True

#Loop para mantener la pantalla visible

while ejecutar:

    #Fondo de pantalla
    pantalla.blit(fondo, (0, 0))
    # Loop para iterar eventos
    for evento in pygame.event.get():

        #evento salir si presiona X de la ventana
        if evento.type == pygame.QUIT:
            ejecutar = False

        #evento salir si presiona tecla escape
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                ejecutar = False

        #Evento si presiona una tecla
        if evento.type == pygame.KEYDOWN:

            # si presiona flecha izquierda
            if evento.key == pygame.K_LEFT:
                jugador_cambio_x = -0.5
            # si presiona flecha derecha
            if evento.key == pygame.K_RIGHT:
                jugador_cambio_x = 0.5
            # Si presiona espacio
            if evento.key == pygame.K_SPACE:
                if not bala_visible:
                    sonido_bala = mixer.Sound('disparo.mp3')
                    sonido_bala.play()
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)

        #Evento si deja de presionar un boton
        if evento.type == pygame.KEYUP:

            #Si deja presionar flecha derecha o izquierda
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_cambio_x = 0

    #Modifica posición jugador
    jugador_x += jugador_cambio_x

    #Mantener dentro de los bordes al jugador
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    #Modifica posición enemigo
    for e in range(cantidad_enemigos):

        #fin de juego
        if enemigo_y[e] > 470:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break

        enemigo_x[e] += enemigo_cambio_x[e]

        #Mantener dentro de los bordes al enemigo
        if enemigo_x[e] <= 0:
            enemigo_cambio_x[e] = .5
            enemigo_y[e] += enemigo_cambio_y[e]
        elif enemigo_x[e] >= 736:
            enemigo_cambio_x[e] = -.5
            enemigo_y[e] += enemigo_cambio_y[e]

        # Colision
        colision = hay_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if colision:
            sonido_colision = mixer.Sound('Golpe.mp3')
            sonido_colision.play()
            bala_y = 500
            bala_visible = False
            puntaje += 1
            enemigo_x[e] = random.randint(0, 736)
            enemigo_y[e] = random.randint(50, 200)

        # Manda llamar a la función enemigo para actualizar su posicion
        enemigo(enemigo_x[e], enemigo_y[e], e)

    #Movimiento bala
    if bala_y <= -64:
        bala_y = 500
        bala_visible = False

    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_cambio_y

    #Manda llamar a la función jugador para actualizar su posicion
    jugador(jugador_x, jugador_y)

    #Muestra puntaje en pantalla
    mostrar_puntaje(texto_x, texto_y)

    #Actualiza pantalla
    pygame.display.update()