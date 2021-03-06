#-------------------------------------------------------------------------------
# Name:        Players
#
# Author:      sl-prog
#
# Licence:     <GNU GENERAL PUBLIC LICENSE>
#-------------------------------------------------------------------------------

import pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):

    def __init__(self, decor, fichier, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.decor = decor
        self.fichier = fichier
        self.x = x
        self.y = y
        self.image = pygame.image.load(self.fichier).convert_alpha()
        self.image_retourne = pygame.transform.flip(self.image, 1, 0)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.mask = pygame.mask.from_surface(self.image)
        self.parterre = False

        self.depart_timer, self.fin_timer = False, False
        self.sauter = 0

    def affiche(self, fenetre):
        fenetre.blit(self.image, self.rect)

#afficher pos perso - TEST
        char_x = str(self.rect.x)
        char_y = str(self.rect.y)
        font = pygame.font.Font(None, 50)
        xx = font.render(char_x, 1, (0,0,0))
        fenetre.blit(xx, (10,10))
        yy = font.render(char_y, 1, (0,0,0))
        fenetre.blit(yy, (10,50))

    def mouvement(self, vitesse_x, vitesse_y, gravite, saut, gauche, droite, debug, vitesse_saut):

        if debug == True:
            self.rect.x = 300
            self.rect.y = 150

        if droite == True:
            self.rect.x += vitesse_x
            self.image = pygame.image.load(self.fichier).convert_alpha()
            self.mask = pygame.mask.from_surface(self.image)

        if gauche == True:
            self.rect.x -= vitesse_x
            self.image = self.image_retourne
            self.mask = pygame.mask.from_surface(self.image)

        if saut and self.parterre:
            self.depart_timer = True
            self.fin_timer = False
            self.rect.y -= vitesse_saut

        if not saut:
            self.fin_timer = True

        if self.depart_timer == True:
            self.sauter = pygame.time.get_ticks() + 400
            self.depart_timer = False
        if pygame.time.get_ticks() > self.sauter:
            self.fin_timer = True

        if not self.parterre:
            if self.fin_timer:
                vitesse_y += gravite  #appliquer la gravite
			 #attraction maximale
                if vitesse_y > 30:
                    vitesse_y = 30
                self.rect.y += vitesse_y
            if not self.fin_timer:
                self.rect.y -= vitesse_saut #sauter



		# faire la collision avec les x
        self.collision(vitesse_x, 0, gauche, droite, False)
        if saut == False:
            self.rect.y += vitesse_y
		#en l'air
        self.parterre = False
		# faire la collision avec les y
        self.collision(0, vitesse_y, False, False, saut)

    def collision(self, vitesse_x, vitesse_y, gauche, droite, saut):
        while (pygame.sprite.collide_mask(self, self.decor)):
            #empeche le perso d'etre blitte dans la map
            if gauche == True: self.rect.x += vitesse_x
            if droite == True: self.rect.x -= vitesse_x

            if saut == False:
                #pour que le perso reste sur le sol
                while (pygame.sprite.collide_mask(self, self.decor)):
                    self.rect.y -= 1
                self.parterre = True
                vitesse_y = 0
            if saut == True:
                while (pygame.sprite.collide_mask(self, self.decor)):
                    self.rect.y += vitesse_saut
                vitesse_saut = 0