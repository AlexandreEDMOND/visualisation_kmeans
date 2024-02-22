import pygame
from random import randint, random
import math


class Rond:
    def __init__(self, rayon, position, couleur):
        self.rayon = rayon
        self.position = position
        self.couleur = couleur
        self.clustter_associe = None
    
    def change_cluster_associe(self, new_cluster):
        self.clustter_associe = new_cluster
        self.change_couleur(new_cluster.couleur)

    def change_couleur(self, new_couleur):
        self.couleur = new_couleur

    def dessiner_rond(self, fenetre):
        pygame.draw.circle(fenetre, self.couleur, self.position, self.rayon)

    def find_cluster(self, list_cluster):
        min_distance = calcul_distance(self.position, list_cluster[0].position)
        min_cluster = list_cluster[0]

        for cluster in list_cluster:
            new_distance = calcul_distance(self.position, cluster.position)
            if new_distance < min_distance:
                min_cluster = cluster
                min_distance = new_distance

        min_cluster.list_rond_associe.append(self)
        self.change_cluster_associe(min_cluster)


class Cluster:
    def __init__(self, couleur, position, largeur):
        self.couleur = couleur
        self.position = position
        self.largeur = largeur
        self.list_rond_associe = []
        self.epaisseur_bordure = 3
        self.couleur_bordure = (255, 255, 255)

    def change_position(self, new_position):
        self.position = new_position
    
    def dessiner_cluster(self, fenetre):
        pygame.draw.rect(fenetre, self.couleur_bordure, (self.position[0] - self.epaisseur_bordure, self.position[1] - self.epaisseur_bordure, self.largeur + 2*self.epaisseur_bordure, self.largeur+ 2*self.epaisseur_bordure))
        pygame.draw.rect(fenetre, self.couleur, (self.position[0], self.position[1], self.largeur, self.largeur))

    def print_len_list_rond(self):
        print("Longueur : ", len(self.list_rond_associe))
    
    def change_inertie(self):
        somme_1 = 0
        somme_2 = 0
        for rond in self.list_rond_associe:
            somme_1 += rond.position[0]
            somme_2 += rond.position[1]
        if len(self.list_rond_associe) != 0:
            somme_1 = int(somme_1/len(self.list_rond_associe))
            somme_2 = int(somme_2/len(self.list_rond_associe))
        else:
            somme_1 = self.position[0]
            somme_2 = self.position[1]
        self.change_position((somme_1, somme_2))
        self.list_rond_associe = []

def calcul_distance(dist_1, dist_2):
    somme_carres = (dist_1[0] - dist_2[0]) ** 2 + (dist_1[1] - dist_2[1]) ** 2
    distance = math.sqrt(somme_carres)
    return distance

def ajout_point_random():
    global list_point
    list_point = []
    for _ in range(nmbre_points):
        random_position = (randint(0, largeur), randint(0, hauteur))
        list_point.append(Rond(taille_point, random_position, (255, 255, 255)))

def ajout_point_groupe_rond(nmbre_groupe):
    global list_point
    list_point = []
    nmbre_point_par_groupe = nmbre_points//nmbre_groupe
    ecart_bord = min(largeur, hauteur)/10
    for _ in range(nmbre_groupe):
        random_center = (randint(ecart_bord, largeur - ecart_bord), randint(ecart_bord, hauteur - ecart_bord))
        for _ in range(nmbre_point_par_groupe):
            random_position = (random_center[0] + (random() - 0.5)*2*ecart_bord, random_center[1] + (random() - 0.5)*2*ecart_bord)
            list_point.append(Rond(taille_point, random_position, (255, 255, 255)))

def generate_color_spectrum(num_squares):
    colors_rgb = []  # Liste pour stocker les codes couleur RGB
    for i in range(num_squares):
        hue = i / num_squares  # Variation de la teinte de 0 à 1
        color = pygame.Color(0)  # Initialisation de la couleur
        color.hsla = (hue * 360, 100, 50, 100)  # Réglage de la teinte, de la saturation et de la luminosité
        colors_rgb.append((color.r, color.g, color.b))  # Ajouter le code couleur RGB à la liste
    return colors_rgb

# Fonction permettant d'initier les clusters
# Modifie la liste "List_cluster" en ajoutant nmbre_cluster d'éléments dans la list
def init_cluster(nmbre_cluster):

    # Génération de la liste des code couleurs RGB pour les clusters
    list_color_cluster = generate_color_spectrum(nmbre_cluster)

    global List_cluster
    
    # Initialisation de la liste des clusters
    # Permet d'effacer les anciens clusters lors de réinitialisation 
    List_cluster = []

    # Ajout des nouveaux clusters dans la liste des clusters
    for i in range(nmbre_cluster):
        List_cluster.append(Cluster(list_color_cluster[i], (randint(0, largeur), randint(0, hauteur)), taille_cluster))

# Fonction permettant d'initialiser la simulation (Liste de points et de clusters)
def init_simulation():

    # Ajout des points de manière aléatoire sur la fenêtre Pygame
    # ajout_point_random()

    # Ajout des points par groupe de carré de manière aléatoire sur la fenêtre Pygame
    ajout_point_groupe_rond(100)

    # Création des clusters
    init_cluster(nmbre_cluster)
  
##################
# VARIABLE GLOBAL
##################
    
# Taille de la fenêtre pygame
largeur = 800
hauteur = 600

# Paramètre sur les points
nmbre_points = 2000
taille_point = 5
list_point = []

# Paramètre sur les clusters
nmbre_cluster = 20
taille_cluster = 20
List_cluster = []

  
# Fonction principal
def main():

    # Création de la fenêtre pygame
    pygame.init()
    taille_fenetre = (largeur, hauteur)
    fenetre = pygame.display.set_mode(taille_fenetre)

    # Initialisation des listes de points et de clusters
    init_simulation()


    running = True
    anim = False    # anim représentation si oui ou non l'animation des déplacements des clusters est faite
    # Boucle principale
    while running:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:      # Vérifier si une touche est enfoncée
                if event.key == pygame.K_RETURN:    # Vérifier si la touche enfoncée est ENTREE
                    anim = True                     # Activation de l'animation
                if event.key == pygame.K_r:         # Vérifier si la touche enfoncée est r
                    init_simulation()               # On réinitialise la simulation
                    # anim = False                  # L'animation est désactivé lors de la réinitialisation

        # Efface l'écran avec un fond noir
        fenetre.fill((0, 0, 0))

        # Dessine l'ensemble des points
        for point in list_point:
            point.dessiner_rond(fenetre)

        # Dessine l'ensemble des clusters
        for cluster in List_cluster:
            cluster.dessiner_cluster(fenetre)

        # Animation des clusters
        if anim:
            # Chaque point est attribué au nouveau cluster le plus proche
            for point in list_point:
                point.find_cluster(List_cluster)
            # Chaque clusters change de position en fonction du barycentre des points
            # qui lui sont attribués
            for cluster in List_cluster:
                cluster.change_inertie()

        # Mettre à jour l'affichage
        pygame.display.flip()

if __name__ == "__main__":
    main()