# RUSSE Cyril
# RANDAXHE Martin


import math
import pygame
import sys


#Constantes

BLEU_CLAIR = (127, 191, 255)
BLEU = (0, 0, 255)
ROUGE = (255, 0, 0)
FENETRE_LARGEUR = 1600
FENETRE_HAUTEUR = 1200
dimension_fenetre = (FENETRE_LARGEUR, FENETRE_HAUTEUR)


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
    pixel_par_complex = 320
    z_a = int(z_a * pixel_par_complex + FENETRE_LARGEUR/2)
    z_b = int(-z_b *pixel_par_complex + FENETRE_HAUTEUR/2)
    return(z_a, z_b)

def pixel_vers_complexe(z):
    z_a = z[0]
    z_b = z[1]
    complexe_par_pixel = 1 / 320
    z_a = (z_a - FENETRE_LARGEUR / 2) * complexe_par_pixel
    z_b = -(z_b - FENETRE_HAUTEUR/2) * complexe_par_pixel
    return (z_a, z_b)


def affiche_complexe(z, couleur):
    position = complexe_vers_pixel(z)
    pygame.draw.circle(fenetre, couleur, position, FENETRE_LARGEUR // 100)


pygame.init()


angle = teta(198, 211)
c = c_new_pol(1, angle)
z = c
angl = c_arg(z)
while(angl > 0.0000001 or angl < -0.0000001) or (angl < -(math.pi - 0.0000001) or angle > (math.pi - 0.0000001)):
    z_precedent = z
    z = c_mult(c, z_precedent)
    # print(z)
    angl = c_arg(z)

print(z)
