# RUSSE Cyril
# RANDAXHE Martin


import math
import pygame
import sys


#Constantes

BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
BLEU_CLAIR = (127, 191, 255)
BLEU = (0, 0, 255)
ROUGE = (255, 0, 0)
FENETRE_LARGEUR = 800
FENETRE_HAUTEUR = 600
dimension_fenetre = (FENETRE_LARGEUR, FENETRE_HAUTEUR)
d = 0


def c_new(a, b):
    return (a, b)

def c_re(z):
    return z[0]

def c_im(z):
    return z[1]

def c_add(x, y):
    return(c_re(x) + c_re(y), c_im(x) + c_im(y))

def c_mult(x, y):
    return(c_re(x) * c_re(y) - c_im(x) * c_im(y), c_re(x) * c_im(y) + c_im(x) * c_re(y))

def c_div(x, y):
    if c_re(y) == 0 and c_im(y) == 0:
        return (math.nan, math.nan)
    return ((c_re(x) * c_re(y) + c_im(x) * c_im(y)) / (c_re(y)**2 + c_im(y)**2), (c_im(x) * c_re(y) - c_im(y) * c_re(x)) / (c_re(y)**2 + c_im(y)**2))

def c_conj(z):
    return(c_re(z), -c_im(z))

def c_abs(z):
    return math.sqrt(c_re(z)**2 + c_im(z)**2)

def c_arg(z):
    return math.atan2(c_im(z), c_re(z))

def c_new_pol(m, a):
    return (m * math.cos(a), m * math.sin(a))

def teta(p, q):
    return 2 * math.pi * (p / q)

def complexe_vers_pixel(z):
    z_a = z[0]
    z_b = z[1]
    pixel_par_complex = 320/2
    z_a = int(z_a * pixel_par_complex + FENETRE_LARGEUR/2)
    z_b = int(-z_b *pixel_par_complex + FENETRE_HAUTEUR/2)
    return(z_a, z_b)

def pixel_vers_complexe(z):
    z_a = z[0]
    z_b = z[1]
    complexe_par_pixel = 2 / 320
    z_a = (z_a - FENETRE_LARGEUR / 2) * complexe_par_pixel
    z_b = -(z_b - FENETRE_HAUTEUR/2) * complexe_par_pixel
    return (z_a, z_b)

def affiche_complexe(z, couleur):
    position = complexe_vers_pixel(z)
    pygame.draw.circle(fenetre, couleur, position, FENETRE_LARGEUR // 100)

def test_convergence(c):
    global d
    z = [0, 0]
    d = 0
    for i in range(0, 200):
        z_precedent = z
        z = c_mult(z_precedent, z_precedent)
        z = c_add(z, c)
        if c_abs(z) > 2:
            d = i
            return False

    return True

def couleur(n):
    n = n % 75
    if not n:
        n = 1
    if n >= 1 and n <= 25:
        if n == 25:
            return(255, 0, 255)
        return(int((n-1) * 255/24), 255 - int((n - 1) * 255/24), 255 )
    elif n > 25 and n < 51:
        n = n % 25
        if n == 0:
            return(255, 0, 255)
        return(255 , int((n-1) * 255/24), 255 - int((n - 1) * 255/24))
    elif n > 50 and n < 76:
        n = n % 25
        if n == 0:
            return(255, 255, 0)
        return(255 - int((n - 1) * 255/24), 255, int((n-1) * 255/24))

def traiter_evenement():
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit
    return

pygame.init()

fenetre = pygame.display.set_mode(dimension_fenetre, 0)
pygame.display.set_caption("Pgm4 fractal")

pixels = pygame.PixelArray(fenetre)
fenetre.fill(BLANC)
pygame.display.flip()

for i in range(dimension_fenetre[0]):
    for j in range(dimension_fenetre[1]):
        z1 = [i,j]
        z1 = pixel_vers_complexe(z1)

        if test_convergence(z1):
            pixels[i][j] = NOIR
        else:
            pixels[i][j] = couleur(d + 1)


    pygame.display.update(((i, 0), (1, dimension_fenetre[1])))
    traiter_evenement()

while True:
    traiter_evenement()
    pygame.time.wait(25)
