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

FENETRE_HAUTEUR = 600
FENETRE_LARGEUR = 800
dimension_fenetre = (FENETRE_LARGEUR, FENETRE_HAUTEUR)
images_par_seconde = 25

position_vaisseau = ([FENETRE_HAUTEUR // 2, FENETRE_LARGEUR // 2])
orientation_vaisseau = 0
masse_vaisseau = 1
VAISSEAU_RAYON = 15
force_pousse = 0

compteur_propulsion = 0

position_planete = [FENETRE_LARGEUR // 2, FENETRE_HAUTEUR * 3 // 4]
planete_est_presente = False
PLANETE_RAYON = 40

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
        dessiner_triangle(JAUNE, position_vaisseau, 38 ,
                        orientation_vaisseau + math.pi * 21 / 20, math.pi / 30)
        dessiner_triangle(JAUNE, position_vaisseau, 38 ,
                        orientation_vaisseau + math.pi * 19 / 20, math.pi / 30)

    dessiner_triangle(ORANGE, position_vaisseau, 23 ,
                        orientation_vaisseau + math.pi, math.pi / 7)
    pygame.draw.circle(fenetre, ROUGE,
    (int(position_vaisseau[0]), int(position_vaisseau[1])), VAISSEAU_RAYON)

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

def traiter_clic(position, bouton):
    global planete_est_presente, masse_planete
    if bouton == 1:
        position_planete[0] = position[0]
        position_planete[1] = position[1]
        planete_est_presente = True
        masse_planete = 1600
    elif bouton == 3:
        planete_est_presente = False
        masse_planete = 0


#---FIN Touches---#

#---Physique---#
def initialiser_calculs():
    global temps_precedent, vitesse
    temps_precedent=0
    vitesse = [0, 0]

    return

def maj_position(position, temps, masse, force, angle, masse_objet, pos_objet):
    global temps_precedent
    angle_entre_objets = angle_vaisseau_planete()
    norme_vecteur = distance_planete_vaisseau()
    acceleration = [0, 0]
    force_gravitationnelle = (0.001 * masse_objet * masse) / (norme_vecteur**2)
    resultante_force_x = (math.cos(angle_entre_objets) * force_gravitationnelle +
                                                        force * math.cos(angle))
    resultante_force_y = (math.sin(angle_entre_objets) * force_gravitationnelle +
                                                        force * math.sin(angle))
    acceleration[0] = resultante_force_x / masse
    acceleration[1] = resultante_force_y / masse

    delta_t = temps - temps_precedent

    vitesse[0] += acceleration[0] * delta_t
    vitesse[1] += acceleration[1] * delta_t
    position[0] += vitesse[0] * delta_t
    position[1] += vitesse[1] * delta_t


    temps_precedent = temps

    return position

def repositionnement(position_vaisseau):
    if position_vaisseau[0] < -100:
        position_vaisseau[0] = FENETRE_LARGEUR + 100
    if position_vaisseau[0] > FENETRE_LARGEUR + 100:
        position_vaisseau[0] = -100
    if position_vaisseau[1] < -100:
        position_vaisseau[1] = FENETRE_HAUTEUR + 100
    if position_vaisseau[1] > FENETRE_HAUTEUR + 100:
        position_vaisseau[1] = -100

def afficher_planete():
    if planete_est_presente:
        pygame.draw.circle(fenetre, BLEU,
        (int(position_planete[0]), int(position_planete[1])), PLANETE_RAYON)

def distance_planete_vaisseau():
    vecteur = [0, 0]
    vecteur[0] = position_planete[0] - position_vaisseau[0]
    vecteur[1] = position_planete[1] - position_vaisseau[1]
    norme_vecteur = math.sqrt(vecteur[0]**2 + vecteur[1]**2)

    return norme_vecteur

def angle_vaisseau_planete():
    angle = (math.atan2(position_planete[1] - position_vaisseau[1],
                            position_planete[0] - position_vaisseau[0]))

    return angle

#---FIN physique---#

#---Collision---#

def verification_collision():
    norme_vecteur = distance_planete_vaisseau()
    if norme_vecteur <= (PLANETE_RAYON + VAISSEAU_RAYON) and planete_est_presente:
        pygame.quit()
        sys.exit()

#---FIN Collision---#

#--- FIN FONCTIONS---#


#Initialisation

pygame.init()

fenetre = pygame.display.set_mode(dimension_fenetre)
pygame.display.set_caption("pgm7 : spaceship")

horloge = pygame.time.Clock()
couleur_fond = NOIR

masse_planete = 0

initialiser_calculs()

pygame.key.set_repeat(10, 10)

while True:
    maintenant = pygame.time.get_ticks()

    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evenement.type == pygame.KEYDOWN:
            traite_entrees()
        if evenement.type == pygame.MOUSEBUTTONDOWN:
            traiter_clic(evenement.pos, evenement.button)

    fenetre.fill(couleur_fond)
    verification_collision()
    affichage_vaisseau()
    afficher_planete()


    if compteur_propulsion > 0:
        force_pousse = 0.0003
        compteur_propulsion -= 1
    position_vaisseau = maj_position(position_vaisseau, maintenant,
                            masse_vaisseau, force_pousse, orientation_vaisseau,
                            masse_planete, position_planete)
    repositionnement(position_vaisseau)
    force_pousse = 0



    pygame.display.flip()
    horloge.tick(images_par_seconde)
