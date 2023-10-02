#RANDAXHE Martin
#RUSSE Cyril

#---Spaceship--#

import math
import pygame
import sys

#---Paramètres---#
#--Constantes--#
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
ORANGE = (230, 100, 0)
JAUNE = (250, 250, 0)
BLEU = (0, 200, 200)
#--Constantes--#

FENETRE_HAUTEUR = 600 * 3
FENETRE_LARGEUR = 800 * 3
dimension_fenetre = (FENETRE_LARGEUR, FENETRE_HAUTEUR)
images_par_seconde = 25

position_vaisseau = ([FENETRE_HAUTEUR // 2, FENETRE_LARGEUR // 2])
orientation_vaisseau = 0
masse_vaisseau = 1
VAISSEAU_RAYON = 15 * 2
force_pousse = 0

compteur_propulsion = 0

position_planete = [FENETRE_LARGEUR // 2, FENETRE_HAUTEUR * 3 // 4]
PLANETE_RAYON = 15 * 2
masse_planete = 1

maintenant = 0
temps_precedent_pos = 0
temps_precedent_pos_planete = 0
premiere_iteration = True
premiere_iteration_planete = True
FACTEUR_SIMULATION = 7


#---FONCTIONS---#

#---Dessin vaisseau---#
def deplacer_pol(point, distance, angle):
    x, y = point
    xf = x + (math.cos(angle)*distance)
    yf = y + (math.sin(angle)*distance)
    return (xf, yf)


def dessiner_triangle(couleur, p, r, a, b):
    angle = a+b
    p1 = deplacer_pol(p, r, angle)
    angle = a-b
    p2 = deplacer_pol(p, r, angle)
    triangle = [p, p1, p2]
    pygame.draw.polygon(fenetre, couleur, triangle)


def affichage_vaisseau():
    if compteur_propulsion > 0:
        dessiner_triangle(JAUNE, position_vaisseau, 38 , orientation_vaisseau + math.pi * 21 / 20, math.pi / 30)
        dessiner_triangle(JAUNE, position_vaisseau, 38 , orientation_vaisseau + math.pi * 19 / 20, math.pi / 30)

    dessiner_triangle(ORANGE, position_vaisseau, 23 , orientation_vaisseau + math.pi, math.pi / 7)
    pygame.draw.circle(fenetre, ROUGE,
    (int(position_vaisseau[0]), int(position_vaisseau[1])), VAISSEAU_RAYON)
    pygame.draw.circle(fenetre, BLEU, (int(position_planete[0]), int(position_planete[1])), PLANETE_RAYON)

#---FIN Dessin vaisseau---#

#---Touches---#
def traite_entrees():
    global orientation_vaisseau, compteur_propulsion
    touche = evenement.key
    if touche == pygame.K_LEFT:
        orientation_vaisseau -= math.pi / 20
    elif touche == pygame.K_RIGHT:
        orientation_vaisseau += math.pi / 20
    elif touche == pygame.K_UP:
        compteur_propulsion += 1

#---FIN Touches---#

#---Physique---#
def initialiser_calculs():
    global temps_precedent, vitesse_vaisseau, vitesse_planete, norme_vecteur_precedent
    norme_vecteur_precedent = distance_planete_vaisseau()
    temps_precedent=0
    vitesse_vaisseau = [0, 0]
    vitesse_planete = [0, 0]

    return

def maj_position(position, temps, masse, force, angle, vitesse):
    global premiere_iteration, temps_precedent_pos, acceleration
    if premiere_iteration:
        premiere_iteration = False
        temps_precedent_pos = temps
    else:
        angle_entre_objets = angle_vaisseau_planete()
        norme_vecteur = distance_planete_vaisseau()
        acceleration = [0, 0]
        resultante_force_x = (force * math.cos(angle))
        resultante_force_y =  (force * math.sin(angle))
        acceleration[0] = resultante_force_x / masse
        acceleration[1] = resultante_force_y / masse

        delta_t = temps - temps_precedent_pos

        vitesse[0] += acceleration[0] * delta_t
        vitesse[1] += acceleration[1] * delta_t
        position[0] += vitesse[0] * delta_t
        position[1] += vitesse[1] * delta_t


        temps_precedent_pos = temps

    return position

def maj_position_planete(position, temps, masse, vitesse):
    global premiere_iteration_planete, temps_precedent_pos_planete
    if premiere_iteration_planete:
        premiere_iteration_planete = False
        temps_precedent_pos_planete = temps
    else:
        angle_entre_objets = angle_vaisseau_planete()
        norme_vecteur = distance_planete_vaisseau()
        delta_t = temps - temps_precedent_pos_planete

        position[0] += vitesse[0] * delta_t
        position[1] += vitesse[1] * delta_t


        temps_precedent_pos_planete = temps

    return position

def repositionnement(position_vaisseau):
    if position_vaisseau[0] < -60:
        position_vaisseau[0] = FENETRE_LARGEUR + 60
    if position_vaisseau[0] > FENETRE_LARGEUR + 60:
        position_vaisseau[0] = -60
    if position_vaisseau[1] < -60:
        position_vaisseau[1] = FENETRE_HAUTEUR + 60
    if position_vaisseau[1] > FENETRE_HAUTEUR + 60:
        position_vaisseau[1] = -60



def distance_planete_vaisseau():
    vecteur = [0, 0]
    vecteur[0] = position_planete[0] - position_vaisseau[0]
    vecteur[1] = position_planete[1] - position_vaisseau[1]
    norme_vecteur = math.sqrt(vecteur[0]**2 + vecteur[1]**2)

    return norme_vecteur

def angle_vaisseau_planete():
    angle = (math.atan2(position_planete[1] - position_vaisseau[1], position_planete[0] - position_vaisseau[0]))

    return angle

#---FIN physique---#

#---Collision---#

def verification_collision():
    global vitesse_planete, vitesse_vaisseau, norme_vecteur_precedent

    vecteur_d = [position_planete[0] - position_vaisseau[0], position_planete[1] - position_vaisseau[1]]
    norme_vecteur_d = math.sqrt(vecteur_d[0]**2 + vecteur_d[1]**2)
    vecteur_u = [vecteur_d[0] / norme_vecteur_d, vecteur_d[1] / norme_vecteur_d]

    norme_vecteur = distance_planete_vaisseau()

    if norme_vecteur_precedent > norme_vecteur and norme_vecteur <= (PLANETE_RAYON + VAISSEAU_RAYON):


        produit_scalaire_v1_u = vitesse_vaisseau[0] * vecteur_u[0] + vitesse_vaisseau[1] * vecteur_u[1]
        v1L = [produit_scalaire_v1_u * vecteur_u[0], produit_scalaire_v1_u * vecteur_u[1]]
        v1T = [vitesse_vaisseau[0] - v1L[0], vitesse_vaisseau[1] - v1L[1]]

        produit_scalaire_v2_u = vitesse_planete[0] * vecteur_u[0] + vitesse_planete[1] * vecteur_u[1]
        v2L = [produit_scalaire_v2_u * vecteur_u[0], produit_scalaire_v2_u * vecteur_u[1]]
        v2T = [vitesse_planete[0] - v2L[0], vitesse_planete[1] - v2L[1]]

        norme_v1L = v1L[0] * vecteur_u[0] + v1L[1] * vecteur_u[1]
        norme_v2L = v2L[0] * vecteur_u[0] + v2L[1] * vecteur_u[1]

        v1L_prime =  ((masse_vaisseau - masse_planete) * norme_v1L / (masse_vaisseau + masse_planete)) + ((2 * masse_planete) * norme_v2L / (masse_vaisseau + masse_planete))
        v2L_prime =  (2 * masse_vaisseau * norme_v1L / (masse_vaisseau+masse_planete)) + ((masse_planete-masse_vaisseau) * norme_v2L / (masse_vaisseau+masse_planete))


        vitesse_vaisseau = [v1L_prime * vecteur_u[0] + v1T[0], v1L_prime * vecteur_u[1] + v1T[1]]
        vitesse_planete = [v2L_prime * vecteur_u[0] + v2T[0], v2L_prime * vecteur_u[1] + v2T[1]]
    norme_vecteur_precedent = norme_vecteur
#---FIN Collision---#


#--- FIN FONCTIONS---#


#Initialisation

pygame.init()

fenetre = pygame.display.set_mode(dimension_fenetre)
pygame.display.set_caption("pgm10 : billard spatial")

horloge = pygame.time.Clock()
couleur_fond = NOIR
police = pygame.font.SysFont("monospace", 50)


initialiser_calculs()

pygame.key.set_repeat(10, 10)

while True:
    temps_precedent = maintenant
    maintenant = pygame.time.get_ticks()

    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evenement.type == pygame.KEYDOWN:
            traite_entrees()
    fenetre.fill(couleur_fond)
    affichage_vaisseau()


    if compteur_propulsion > 0:
        force_pousse = 0.0003
        compteur_propulsion -= 1

    for t in range(temps_precedent * 10, maintenant * 10, 1):
        verification_collision()
        position_planete = maj_position_planete(position_planete , t / 10, masse_planete, vitesse_planete)
        position_vaisseau = maj_position(position_vaisseau, t / 10, masse_vaisseau, force_pousse, orientation_vaisseau, vitesse_vaisseau)
        repositionnement(position_vaisseau)
        repositionnement(position_planete)
    force_pousse = 0



    pygame.display.flip()
    horloge.tick(images_par_seconde)
