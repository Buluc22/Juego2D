import pygame
import random
import math
from pygame import mixer

# Iniciar pygame
pygame.init()

# Crear pantalla del juego
pantalla = pygame.display.set_mode((800, 600))

# Titulo e icono del juego
pygame.display.set_caption("Guerra Galáctica")
icono = pygame.image.load("nave-espacial.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("black-hole.jpg")

# agregar musica
mixer.music.load('MusicaFondo.mp3')
mixer.music.play(-1)

# variables del jugador
img_jugador = pygame.image.load("nave-espacial-prota.png")
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0

# variables del enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("nave-espacial_enemigos.png"))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(0.6)
    enemigo_y_cambio.append(50)

# variables del rayo laser
img_rayo = pygame.image.load("rayo.png")
rayo_x = 0
rayo_y = 500
rayo_x_cambio = 0
rayo_y_cambio = 2
rayo_visible = False

# puntaje
puntaje = 0
fuente = pygame.font.Font('freesansbold.ttf', 32)
texto_x = 10
texto_y = 10

# texto final del juego
fuente_final = pygame.font.Font('freesansbold.ttf', 40)


def texto_final():
    mi_fuente_final = fuente_final.render("JUEGO TERMINADO", True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (200, 200))


# funcion mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


# funcion jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))


# funcion enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))


# funcion disparar rayo
def disparar_rayo(x, y):
    global rayo_visible
    rayo_visible = True
    pantalla.blit(img_rayo, (x + 16, y + 10))


# funcion detectar colision
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2))
    if distancia < 27:
        return True
    else:
        return False


# Loop del juego
se_ejecuta = True
while se_ejecuta:

    # imagen de fondo
    pantalla.blit(fondo, (0, 0))

    # iterar eventos
    for evento in pygame.event.get():

        # envento cerrar
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        # evento presionar teclas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_a:
                jugador_x_cambio = -0.6
            if evento.key == pygame.K_d:
                jugador_x_cambio = 0.6
            if evento.key == pygame.K_SPACE:
                sonido_rayo = mixer.Sound('disparo.mp3')
                sonido_rayo.play()
                if not rayo_visible:
                    rayo_x = jugador_x
                    disparar_rayo(rayo_x, rayo_y)

        # envento soltar teclas
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_d or evento.key == pygame.K_a:
                jugador_x_cambio = 0

    # modificar ubicacion del jugador
    jugador_x += jugador_x_cambio

    # mantener dentro de bordes al jugador
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    # modificar ubicacion del enemigo
    for e in range(cantidad_enemigos):

        # fin del juego
        if enemigo_y[e] > 500:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break

        enemigo_x[e] += enemigo_x_cambio[e]

        # mantener dentro de bordes al enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.6
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -0.6
            enemigo_y[e] += enemigo_y_cambio[e]

        # colision
        colision = hay_colision(enemigo_x[e], enemigo_y[e], rayo_x, rayo_y)
        if colision:
            sonido_colision = mixer.Sound('Golpe.mp3')
            sonido_colision.play()
            rayo_y = 500
            rayo_visible = False
            puntaje += 1
            print(puntaje)
            enemigo_x[e] = random.randint(0, 736)
            enemigo_y[e] = random.randint(50, 200)

        enemigo(enemigo_x[e], enemigo_y[e], e)

    # movimiento rayo
    if rayo_y <= -64:
        rayo_y = 500
        rayo_visible = False

    if rayo_visible:
        disparar_rayo(rayo_x, rayo_y)
        rayo_y -= rayo_y_cambio

    jugador(jugador_x, jugador_y)

    mostrar_puntaje(texto_x, texto_y)

    # actualizar
    pygame.display.update()
