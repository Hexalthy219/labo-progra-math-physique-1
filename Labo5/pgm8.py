#RANDAXHE Martin
#RUSSE Cyril

#---Montagnes russes---#

import math
import pygame
import sys

#---constantes---#
JAUNEPALE = (255, 255, 100)
BLEU = (0, 0, 255)
ROUGE = (255, 0, 0)
NOIR = (0, 0, 0)


#---parametres---#

FENETRE_HAUTEUR = 600
FENETRE_LARGEUR = 800
dimension_fenetre = (FENETRE_LARGEUR  , FENETRE_HAUTEUR  )
images_par_seconde = 25

position_mobile = [0, 0]


a = 0.000165
b = 0
c = -0.055
d = 0
e = 5

temps_maintenant, temps_precedent = 0,0

vitesse = [0, 0]
vitesse_max = 0
acc_ressentie = 0
a_min = 50000000
a_max = 0
premiere_iteration = True

#---FONCTIONS---#

def fenetre_vers_piste(xf, yf):
    m_par_pixel = 1 / 20
    xp = (xf - FENETRE_LARGEUR / 2) * m_par_pixel
    yp = -(yf - FENETRE_HAUTEUR) * m_par_pixel
    return (xp, yp)

def piste_vers_fenetre(xp, yp):
    pixel_par_m = 20
    xf = int(xp * pixel_par_m + FENETRE_LARGEUR / 2)
    yf = int(-yp * pixel_par_m + FENETRE_HAUTEUR)
    return (xf, yf)

def hauteur_piste(x):
    h_x = a * x**4 + b * x**3 + c * x**2 + d * x + e
    return h_x

def dessiner_piste():
    for x in range(0, FENETRE_LARGEUR , 1):
        y = 0
        x_a = fenetre_vers_piste(x, y)[0]
        y = hauteur_piste(x_a)
        x_a, y = piste_vers_fenetre(x_a, y)
        pygame.draw.rect(fenetre, BLEU, ((x, y), (1, FENETRE_HAUTEUR - y)))

def dessiner_mobile(pos):
    x, y =  piste_vers_fenetre(pos[0], pos[1])
    pygame.draw.circle(fenetre, ROUGE,(int(x),int(y)) , 10)

def pente(position):
    pente = (hauteur_piste(position[0] + 10**(-6)) - hauteur_piste(position[0]))/10**(-6)
    return pente

def prod_scal(g1, g2, n1, n2):
    return g1 * n1 + g2 * n2

def mettre_a_jour_position(position, temps_maintenant):
    global vitesse, premiere_iteration, temps_precedent, norme_vitesse, acc_ressentie
    mu_c = 0.03
    vitesse_precedente = [vitesse[0], vitesse[1]]
    g = -9.81
    a_g = [0, g]

    if premiere_iteration:
        vitesse[0] = 0
        vitesse[1] = 0
        premiere_iteration = False
        temps_precedent = temps_maintenant
        delta_t = 0.001
    else:
        delta_t = 0.001
        norme_vitesse = math.sqrt(vitesse[0]**2 + vitesse[1]**2)
        alpha = pente(position)
        teta = math.sqrt(1 + alpha**2)
        n = [-alpha / teta, 1 / teta]
        a_r = [-(prod_scal(a_g[0], a_g[1], n[0], n[1]) * n[0]), -(prod_scal(a_g[0], a_g[1], n[0], n[1]) * n[1])]


        if vitesse[0] > 0:
            u = [1 / teta, alpha / teta]
        else:
            u = [-1 / teta, -alpha / teta]

        vitesse[0] = norme_vitesse * u[0]
        vitesse[1] = norme_vitesse * u[1]
        a_t = [(vitesse[0] - vitesse_precedente[0]) / delta_t,  (vitesse[1] - vitesse_precedente[1]) / delta_t]
        a_p = [a_t[0] + a_r[0], a_t[1] + a_r[1]]
        acc_ressentie = math.sqrt(a_p[0]**2 + a_p[1]**2)
        a_f =  [(-mu_c * abs(prod_scal(a_p[0], a_p[1], n[0], n[1])) * u[0]), (-mu_c * abs(prod_scal(a_p[0], a_p[1], n[0], n[1])) * u[1])]
        a_tot = [ (a_t[0] + a_g[0] + a_r[0] + a_f[0]) , (a_t[1] + a_g[1] + a_r[1] + a_f[1]) ]
        vitesse[0] += delta_t * a_tot[0]
        vitesse[1] += delta_t * a_tot[1]
        position[0] += delta_t * vitesse[0]
        position[1] += delta_t * vitesse[1]
        temps_precedent = temps_maintenant
    return position

def mettre_a_jour_statistique():
    global norme_vitesse, vitesse_max, a_max, a_min, acc_ressentie
    if vitesse_max < norme_vitesse:
        vitesse_max = norme_vitesse
    if acc_ressentie < a_min:
        a_min = acc_ressentie
    if acc_ressentie > a_max:
        a_max = acc_ressentie



#Tableau de bord
def afficher_tableau_de_bord():
    acc_ressenti = acc_ressentie / 9.81
    a_ma = a_max / 9.81
    texte = "Vitesse : {0:.2f} m/s".format(norme_vitesse)
    texte_v_max = "Vitesse max : {0:.2f} m/s".format(vitesse_max)
    texte_a_res = "Acceleration : {0:.2f} g".format(acc_ressenti)
    texte_a_max = "Acceleration max : {0:.2f} g".format(a_ma)

    image = police.render(texte, True, NOIR)
    fenetre.blit(image, (50, 50))
    image = police.render(texte_v_max, True, NOIR)
    fenetre.blit(image, (50, 80))
    image = police.render(texte_a_res, True, NOIR)
    fenetre.blit(image, (50, 110))
    image = police.render(texte_a_max, True, NOIR)
    fenetre.blit(image, (50, 140))


def traite_entrees():
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()

            sys.exit()


#---FIN FONCTIONS---#



#---Initialisation---#

pygame.init()
position_mobile = [-20, hauteur_piste(-20)]
temps_precedent = 0

fenetre = pygame.display.set_mode(dimension_fenetre)
pygame.display.set_caption("pgm8 : Montagnes Russes")

horloge = pygame.time.Clock()
couleur_fond = JAUNEPALE

norme_vitesse = 0

police = pygame.font.SysFont("monospace", 32)
while True:
    temps_precedent = temps_maintenant
    temps_maintenant = pygame.time.get_ticks()
    for t in range(temps_precedent, temps_maintenant, 1):
        mettre_a_jour_position(position_mobile, t / 1000)
        mettre_a_jour_statistique()

    traite_entrees()
    fenetre.fill(couleur_fond)
    dessiner_piste()
    dessiner_mobile(position_mobile)
    afficher_tableau_de_bord()
    pygame.display.flip()
    horloge.tick(images_par_seconde)
