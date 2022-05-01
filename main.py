import pygame
from sprites import *
from config import *
import sys
from music import *
import math
class Game:

    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = False
        self.character_spritesheet = Spritesheet('img/perso6.png')
        self.terrain_spritesheet = Spritesheet2('img/terrain.png')
        self.tileset_spritesheet = Spritesheet2('img/tileset3.png')
        self.house_spritesheet = Spritesheet3('img/house.png')
        self.statue_spritesheet = Spritesheet3('img/statue.png')
        self.interieur1_spritesheet = Spritesheet3('img/Texture/groundmaison.png')
        self.enemy_spritesheet = Spritesheet3('img/animal1.png')
        self.PNJ_spritesheet =  Spritesheet2('img/perso4.png')
        self.crocduloup_spritesheet= Spritesheet2('img/attack.png')
        self.attack_spritesheet = Spritesheet2('img/attack.png')
        self.noir_spritesheet = Spritesheet3('img/ecran_noir.png')
        self.sorciere_spritesheet = Spritesheet('img/perso8.png')
        self.boule_de_feu_spritesheet = Spritesheet2('img/boule_de_feu.png')


    def createTilemap(self,tilemap):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                if not column=='\n':
                    Ground(self, j, i)
                    if column == 'B':
                        Block(self, j, i)
                    if column == 'P':
                        Player(self, j, i)
                    if column == '*':
                        Herbe(self, j, i)
                    if column == '1':
                        House(self, j, i)
                    if column == '2':
                        House1(self, j, i)
                    if column == '3':
                        House2(self, j, i)
                    if column == 'X':
                        House21(self, j, i)
                    if column == '4':
                        House3(self, j, i)
                    if column == '5':
                        House4(self, j, i)
                    if column == '6':
                        House5(self, j, i)
                    if column == '7':
                        House6(self, j, i)
                    if column == '8':
                        House7(self, j, i)
                    if column == '9':
                        House8(self, j, i)
                    if column == 'E':
                        Enemy(self, j, i)
                    if column == 'U':
                        Chemain(self, j, i)
                    if column == 'O':
                        Chemain1(self, j, i)
                    if column == 'T':
                        Chemain2(self, j, i)
                    if column == 'I':
                        Chemain3(self, j, i)
                    if column == 'R':
                        Chemain4(self, j, i)
                    if column == 'Y':
                        Chemain5(self, j, i)
                    if column == 'A':
                        Chemain6(self, j, i)
                    if column == 'G':
                        Chemain7(self, j, i)
                    if column == 'J':
                        Chemain8(self, j, i)
                    if column == 'F':
                        Chemain9(self, j, i)
                    if column == 'S':
                        Sortie(self, j, i)
                    if column == '{':
                        PNJ(self, j, i)


    def createTilemapMaison(self,tilemap):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                if not column=='\n':
                    GroundMaison(self, j, i)
                    if column == 'B':
                        Block(self, j, i)
                    if column == 'P':
                        Player(self, j, i)
                    if column == 'S':
                        Sortie(self, j, i)
                    if column== '*':
                        Noir(self, j, i)
                    if column== '-':
                        Escalier1(self, j, i)
                    if column== '_':
                        Escalier2(self, j, i)


    def createTilemapDonjon(self,tilemap):

        boss_music()

        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                if not column=='\n':
                    GroundDonjon(self, j, i)
                    if column == 'B':
                        Block(self, j, i)
                    if column == 'P':
                        Player(self, j, i)
                    if column== '*':
                        Noir(self, j, i)
                    if column== '-':
                        Escalier1(self, j, i)
                    if column== '_':
                        Escalier2(self, j, i)
                    if column== '(':
                        Escalier3(self, j, i)
                    if column== ')':
                        Escalier4(self, j, i)
                    if column == 'W':
                        Sorciere(self, j, i)
                    if column== '0':
                        Lave(self, j, i)
                    if column== '1':
                        Lave1(self, j, i)
                    if column== '2':
                        Lave2(self, j, i)
                    if column== '3':
                        Lave3(self, j, i)
                    if column== '4':
                        Lave4(self, j, i)
                    if column== '5':
                        Lave5(self, j, i)
                    if column== '6':
                        Lave6(self, j, i)
                    if column== '7':
                        Lave7(self, j, i)
                    if column== '8':
                        Lave8(self, j, i)
                    if column== '9':
                        Lave9(self, j, i)
                    if column== '&':
                        Lave10(self, j, i)
                    if column== '~':
                        Lave11(self, j, i)
                    if column== '#':
                        Lave12(self, j, i)
                    if column== '{':
                        Lave13(self, j, i)
                    if column== '[':
                        Lave14(self, j, i)
                    if column== 'X':
                        Declenche_Boss(self, j, i)
                    if column == '@':
                        Statue(self, j, i)
                    if column == '$':
                        Statue1(self, j, i)

    def selectionneur(self,num):
        self.selectionneur=num

    def pvdumonstre(self,num):
        self.pvdumonstre=num

    def pvduboss(self,num):
        self.pvduboss = num

    def bouledefeu(self,j,i):
        bouledefeu(self,j,i)

    def croc_pop_item(self,j,i):
        epee(self,j,i)

    def potion_pv_pop_item(self,j,i):
        potion_pv(self,j,i)


    def new(self):

        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.player =  pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.entrer= pygame.sprite.LayeredUpdates()
        self.statue = pygame.sprite.LayeredUpdates()
        self.PNJ = pygame.sprite.LayeredUpdates()
        self.donjon = pygame.sprite.LayeredUpdates()
        self.sorciere = pygame.sprite.LayeredUpdates()
        self.crocduloup = pygame.sprite.LayeredUpdates()
        self.potion_pv = pygame.sprite.LayeredUpdates()
        self.boule_de_feu = pygame.sprite.LayeredUpdates()
        self.declenche_boss = pygame.sprite.LayeredUpdates()
        self.statue1  = pygame.sprite.LayeredUpdates()


    def camera_active(self):
        self.camera_active=False

    def boss_actif(self,num):
        self.boss_actif=num



    def events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:

            self.playing = False
            self.running = False
    def update(self):

        self.all_sprites.update()



    def draw(self):

        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()


    def barredevie(self,position_x_dujoueur,position_y_dujoueur,point_de_vie_actuel,point_de_vie_max):
        if point_de_vie_actuel!=0:
                longueur_barre=point_de_vie_actuel/point_de_vie_max
        elif point_de_vie_actuel<=0:
            longueur_barre=0
        if point_de_vie_actuel<=0.6*point_de_vie_max and point_de_vie_actuel>0.3*point_de_vie_max:
                    pygame.draw.rect(self.screen,(128, 128, 128),[position_x_dujoueur-2,position_y_dujoueur-10,40,5])
                    pygame.draw.rect(self.screen,(255,255,0),[position_x_dujoueur-2,position_y_dujoueur-10,40*longueur_barre,5])
        elif point_de_vie_actuel<=0.30*point_de_vie_max:
                    pygame.draw.rect(self.screen,(128, 128, 128),[position_x_dujoueur-2,position_y_dujoueur-10,40,5])
                    pygame.draw.rect(self.screen,(255,0,0),[position_x_dujoueur-2,position_y_dujoueur-10,40*longueur_barre,5])
        else:
                    pygame.draw.rect(self.screen,(128, 128, 128),[position_x_dujoueur-2,position_y_dujoueur-10,40,5])
                    pygame.draw.rect(self.screen,(0,255,0),[position_x_dujoueur-2,position_y_dujoueur-10,40*longueur_barre,5])



        pygame.display.update()


    def main(self):

        while self.playing:

            self.events()
            self.update()
            self.draw()

        self.running = False

def intro_screen():
         background = pygame.image.load('img/menu.jpg')
         background=  pygame.transform.scale(background, (700,500))
         icon= pygame.image.load('img/icon.png')

         screen.blit(background,(0,0))

         play_button = pygame.image.load('img/bouton_start1.png')
         play_button_rect= play_button.get_rect() #créer un rectangle de collision autour de l'image button

         play_button = pygame.transform.scale(play_button, (150,150))
         play_button_rect.x = math.ceil(screen.get_width() / 2.65)# postionner le button
         play_button_rect.y = math.ceil(screen.get_height() / 2.9 )
         screen.blit(play_button,play_button_rect)
         pygame.display.set_icon(icon)
         pygame.display.flip()

         for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    g.running=True
                    son_clic()
                    music_main2()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


screen = pygame.display.set_mode((400, 600))

pygame.display.set_caption("MOLDAVIA ADVENTURE")



g = Game()
g.selectionneur(0)
g.pvdumonstre(50)
g.boss_actif(0)
g.pvduboss(100)

def jeu_run():
    while g.running==True:
        g.new()
        if g.selectionneur== 0:
            g.createTilemap(tilemap00)
        g.main()


    menu_run()

def menu_run():
    while g.running== False:
        intro_screen()
        play_music()
    if g.running==True:
        jeu_run()


menu_run()
pygame.quit()
sys.exit()
sys.exit()
