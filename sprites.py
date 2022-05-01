import pygame
from config import *
import math
import random
from music import *
import time



class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        sprite.set_colorkey(FOND_VERT)
        return sprite

class Spritesheet2:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite

class Spritesheet3:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        sprite.set_colorkey(FOND_VERT2)
        return sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.player
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)

        self.health = 50
        self.max_health=50
        self.defence= 1
        self.attack= 0.5

        self.inventaire=[["couteau"],[],[]]

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.time = 0

        self.level=0
        self.experience=0
        self.vie_statue=100
    def update(self):
        if  self.rect.y >= 322 and self.rect.x >= 435:
                PNJ.dialogue(self,'img/dialogue_suivre.png')

        self.movement()
        self.collide_statue()
        self.animate()
        self.collide_enemy()
        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        self.x_change = 0
        self.y_change = 0
        self.player_inventaire()
        self.game.barredevie(self.rect.x,self.rect.y,self.health,self.max_health)


    def player_inventaire(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e] and len(self.inventaire[2])>0:
            self.inventaire[2].pop()
            self.health=self.max_health
        if keys[pygame.K_a]:
            self.game.screen.blit(pygame.image.load("img\inventaire.jpg"),(200,10))
            x=0
            y=0
            for objet in range(len(self.inventaire[0])):
                if self.inventaire[0][objet]=="couteau":

                    image=pygame.transform.scale(pygame.image.load("img\couteau.png"), (20,20))
                    self.game.screen.blit(image,(213+x,23+y))
                    x=x+30
                if self.inventaire[0][objet]=="croc du loup":

                    image=pygame.transform.scale(pygame.image.load("img\crocduloup.png"), (20,20))
                    self.game.screen.blit(image,(213+x,23+y))
                    x=x+30
            for objet in range(len(self.inventaire[2])):
                if self.inventaire[2][objet]=="potion pv max":

                    image=pygame.transform.scale(pygame.image.load("img\crocduloup.png"), (20,20))
                    self.game.screen.blit(image,(213+x,23+y))
                    x=x+30

            pygame.display.update()





    def movement(self):
        keys = pygame.key.get_pressed()
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        hits_enemy = pygame.sprite.spritecollide(self, self.game.enemies, False)

        if keys[pygame.K_q]:

            self.x_change -= PLAYER_SPEED
            self.facing = 'left'

            if not pygame.mixer.Channel(1).get_busy():
                    son_pas()
            if self.game.camera_active==True:
                for sprite in self.game.all_sprites:
                    sprite.rect.x += PLAYER_SPEED



        elif keys[pygame.K_d]:
            self.facing = 'right'
            self.x_change += PLAYER_SPEED

            if not pygame.mixer.Channel(1).get_busy():
                    son_pas()

            if self.game.camera_active==True:
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= PLAYER_SPEED

        elif keys[pygame.K_z]:
            self.facing = 'up'
            self.y_change -= PLAYER_SPEED

            if not pygame.mixer.Channel(1).get_busy():
                    son_pas()

            if self.game.camera_active==True:
                for sprite in self.game.all_sprites:
                    sprite.rect.y += PLAYER_SPEED

        elif keys[pygame.K_s]:

            self.facing = 'down'
            self.y_change += PLAYER_SPEED

            if not pygame.mixer.Channel(1).get_busy():
                    son_pas()

            if self.game.camera_active==True:
                for sprite in self.game.all_sprites:
                    sprite.rect.y -= PLAYER_SPEED

        else:
            pygame.mixer.Channel(1).stop()



    def collide_statue (self):
            keys = pygame.key.get_pressed()
            hits_statue = pygame.sprite.spritecollide(self, self.game.statue, False)
            if hits_statue:
               print(self.vie_statue)
               if keys[pygame.K_SPACE]:
                        self.vie_statue -= 1
                        self.game.screen.blit(pygame.image.load('img/attack1.png'),(self.rect.x,self.rect.y))
                        pygame.display.update()
            if self.vie_statue<= 0:
                self.game.pvduboss=self.game.pvduboss-self.attack*110
                self.vie_statue +=100

                pygame.sprite.spritecollide(self, self.game.statue, True)
                pygame.sprite.spritecollide(self, self.game.statue1, True)
            if self.game.pvduboss <= 0:
                pygame.sprite.spritecollide(self, self.game.sorciere, True)
                self.game.new()
                self.game.createTilemapDonjon(tilemapdonjon)
                self.game.camera_active=True



    def collide_enemy(self):
        keys = pygame.key.get_pressed()
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width

            if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
            if keys[pygame.K_SPACE]:
                    self.game.pvdumonstre=self.game.pvdumonstre-self.attack
                    self.animate1()
                    self.game.screen.blit(pygame.image.load('img/attack1.png'),(self.rect.x,self.rect.y))

                    pygame.display.update()

            self.health=self.health-0.1


            if self.game.pvdumonstre<=0:
                self.experience=15
                if self.experience>self.level*10:
                    self.level=self.level+1
                    self.health=0.75*self.max_health
                    self.max_health=50+self.level*10
                    self.attack=self.attack+0.25
                    self.experience=0
                else:
                    self.experience+=self.experience
        if self.health <=0:
                self.game_over()
                pygame.mixer.Channel(1).stop()




    def game_over(self):

        keys = pygame.key.get_pressed()
        ecran_gameover = pygame.image.load('img/game_over.png')
        self.game.screen.blit(ecran_gameover,(200,100))

        pygame.mixer.Channel(1).stop()
        self.time += 1
        print(self.time)
        if self.time >= 100:
            self.game.playing = False




    def collide_blocks(self, direction):
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        hits_enemy=pygame.sprite.spritecollide(self, self.game.enemies, False)
        hits_sorciere=pygame.sprite.spritecollide(self, self.game.sorciere, False)
        if direction == 'x':

            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    if self.game.camera_active==True:
                        for sprite in self.game.all_sprites:
                            sprite.rect.x += PLAYER_SPEED

                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    if self.game.camera_active==True:
                        for sprite in self.game.all_sprites:
                            sprite.rect.x -= PLAYER_SPEED


            else:
                hits2 = pygame.sprite.spritecollide(self, self.game.entrer, False)
                if hits2:
                    self.game.new()
                    self.game.createTilemapMaison(tilemapmaison)
                else:
                        hits = pygame.sprite.spritecollide(self, self.game.crocduloup, False)
                        if hits:
                            hits = pygame.sprite.spritecollide(self, self.game.crocduloup, True)
                            self.inventaire[0].append("croc du loup")
                        else:
                            hits = pygame.sprite.spritecollide(self, self.game.potion_pv, False)
                            if hits:
                                hits = pygame.sprite.spritecollide(self, self.game.potion_pv, True)
                                self.inventaire[2].append("potion pv max")

                            else:
                                hits4 = pygame.sprite.spritecollide(self, self.game.donjon, False)
                                if hits4:
                                    self.game.new()
                                    self.game.createTilemapDonjon(tilemapdonjon)
                                    self.game.camera_active=True
                                else:
                                    hits=pygame.sprite.spritecollide(self, self.game.declenche_boss, False)
                                    if hits:

                                        self.game.boss_actif=1

                                    else:
                                        hits4 = pygame.sprite.spritecollide(self, self.game.boule_de_feu,False)
                                        if hits4:
                                            pygame.sprite.spritecollide(self, self.game.boule_de_feu,True)
                                            self.health-=5
                                            if self.health <=0:
                                                self.game_over()

                                                pygame.mixer.Channel(1).stop()





        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)

            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    if self.game.camera_active==True:
                        for sprite in self.game.all_sprites:
                            sprite.rect.y += PLAYER_SPEED

                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    if self.game.camera_active==True:
                        for sprite in self.game.all_sprites:
                            sprite.rect.y -= PLAYER_SPEED
            else:
                hits2 = pygame.sprite.spritecollide(self, self.game.entrer, False)
                if hits2:

                    self.game.new()
                    self.game.createTilemapMaison(tilemapmaison)


                else:
                        hits = pygame.sprite.spritecollide(self, self.game.crocduloup, False)
                        if hits:
                            hits = pygame.sprite.spritecollide(self, self.game.crocduloup, True)
                            self.inventaire[0].append("croc du loup")
                        else:
                            hits = pygame.sprite.spritecollide(self, self.game.potion_pv, False)
                            if hits:
                                hits = pygame.sprite.spritecollide(self, self.game.potion_pv, True)
                                self.inventaire[2].append("potion pv max")

                            else:
                                hits4 = pygame.sprite.spritecollide(self, self.game.donjon, False)
                                if hits4:

                                    self.game.new()
                                    self.game.createTilemapDonjon(tilemapdonjon)
                                    self.game.camera_active=True
                                else:
                                    hits=pygame.sprite.spritecollide(self, self.game.declenche_boss, False)
                                    if hits:
                                        self.game.boss_actif=1
                                    else:
                                        hits4 = pygame.sprite.spritecollide(self, self.game.boule_de_feu,False)
                                        if hits4:
                                            pygame.sprite.spritecollide(self, self.game.boule_de_feu,True)
                                            self.health-=5
                                            if self.health <=0:
                                                self.game_over()

                                                pygame.mixer.Channel(1).stop()




    def animate(self):
        down_animations = [self.game.character_spritesheet.get_sprite(224, 128, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(192, 128, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(256, 128, self.width, self.height)]

        left_animations = [self.game.character_spritesheet.get_sprite(224, 160, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(192, 160, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(256, 160, self.width, self.height)]

        up_animations = [self.game.character_spritesheet.get_sprite(224, 224, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(192, 224, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(256, 224, self.width, self.height)]

        right_animations = [self.game.character_spritesheet.get_sprite(224, 192, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(192, 192, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(256, 192, self.width, self.height)]

        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(224, 160, self.width, self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(224, 192, self.width, self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(224, 224, self.width, self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(224, 128, self.width, self.height)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 3:
                    self.animation_loop = 1


    def animate1(self):
        down_animations = [self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height)]

        left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
                          self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
                          self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
                          self.game.attack_spritesheet.get_sprite(96, 95, self.width, self.height),
                          self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height)]

        up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height)]

        right_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height)]


        if self.facing == "left":
            self.image = left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.2
            if self.animation_loop >= 5:
                self.animation_loop = 1

        if self.facing == "right":
            self.image = right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.2
            if self.animation_loop >= 5:
                self.animation_loop = 1

        if self.facing == "up":
            self.image = up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.2
            if self.animation_loop >= 5:
                self.animation_loop = 1

        if self.facing == "down":
            self.image = down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.2
            if self.animation_loop >= 5:
                self.animation_loop = 1


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.facing = 'left'
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(30, 30)

        self.image = self.game.enemy_spritesheet.get_sprite(32, 0, self.width, self.height)

        self.x_change = 0
        self.y_change = 0

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.health = 10
        self.drop_item=0


    def update(self):
        self.game.barredevie(self.rect.x,self.rect.y,self.game.pvdumonstre,50)
        if self.game.pvdumonstre>0:
            self.movement()
            self.animate()

            self.rect.x += self.x_change
            self.rect.y += self.y_change

            self.x_change = 0
            self.y_change = 0

        else:
            if self.drop_item==0:
                pygame.sprite.spritecollide(self, self.game.enemies, True)
                self.game.croc_pop_item(10,12)
                rng=random.randint(11,15)
                if rng>10:
                    self.game.potion_pv_pop_item(11,12)


                self.drop_item=1

    def movement(self):
        hits = pygame.sprite.spritecollide(self, self.game.player,False)
        if not hits:
            if self.facing == "left":
                self.x_change -= ENEMY_SPEED
                self.movement_loop -= 1
                if self.movement_loop <= - self.max_travel:
                    self.facing = 'right'

            if self.facing == "right":
                self.x_change += ENEMY_SPEED
                self.movement_loop += 1
                if self.movement_loop >= self.max_travel:
                    self.facing = 'left'

        else:
                self.x_change=0
                self.y_change=0



    def animate(self):
        down_animations = [self.game.enemy_spritesheet.get_sprite(224, 128, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(192, 128, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(256, 128, self.width, self.height)]

        left_animations = [self.game.enemy_spritesheet.get_sprite(224, 160, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(192, 160, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(256, 160, self.width, self.height)]

        up_animations = [self.game.enemy_spritesheet.get_sprite(224, 224, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(192, 224, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(256, 224, self.width, self.height)]

        right_animations = [self.game.enemy_spritesheet.get_sprite(224, 192, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(192, 192, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(256, 192, self.width, self.height)]

        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(224, 160, self.width, self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(224, 192, self.width, self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(224, 224, self.width, self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(224, 128, self.width, self.height)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 3:
                    self.animation_loop = 1

class PNJ(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PNJ_LAYER
        self.groups = self.game.all_sprites, self.game.PNJ, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.PNJ_spritesheet.get_sprite(320, 128, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.x_change = 0
        self.y_change = 0

        self.facing = 'left'
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = 10
        self.compteur_stop_mvt=0
        self.compteur = 0

    def update(self):
        hits = pygame.sprite.spritecollide(self, self.game.player,False)
        if hits:
            self.compteur_stop_mvt+=1
            self.facing = 'down'
        if self.game.pvdumonstre <= 0 :
                self.deplacment_maison()

        if self.compteur_stop_mvt==0:
            self.movement()
            self.animate()
            self.rect.x += self.x_change
            self.rect.y += self.y_change
            self.x_change = 0
            self.y_change = 0
        self.dialogue('img/dialogue_rencontre.png')

    def movement(self):
        hits = pygame.sprite.spritecollide(self, self.game.player,False)
        if not hits:
            if self.facing == "left":
                self.x_change -= PNJ_SPEED
                self.movement_loop -= 1
                if self.movement_loop <= - self.max_travel:
                    self.facing = 'right'

            if self.facing == "right":
                self.x_change += PNJ_SPEED
                self.movement_loop += 1
                if self.movement_loop >= self.max_travel:
                    self.facing = 'left'
        if hits:
            self.x_change=0

    def deplacment_maison(self):# le pnj se déplace vers la maison
        hits = pygame.sprite.spritecollide(self, self.game.entrer,False)
        hits_player = pygame.sprite.spritecollide(self, self.game.player,False)
        max_travel_up = 1
        max_travel_right = -130
        max_travel_down = 30
        down_animations = [self.game.PNJ_spritesheet.get_sprite(224, 128, self.width, self.height),
                           self.game.PNJ_spritesheet.get_sprite(192, 128, self.width, self.height),
                           self.game.PNJ_spritesheet.get_sprite(256, 128, self.width, self.height)]
        up_animations = [self.game.PNJ_spritesheet.get_sprite(224, 224, self.width, self.height),
                           self.game.PNJ_spritesheet.get_sprite(192, 224, self.width, self.height),
                           self.game.PNJ_spritesheet.get_sprite(256, 224, self.width, self.height)]
        right_animations = [self.game.PNJ_spritesheet.get_sprite(224, 192, self.width, self.height),
                            self.game.PNJ_spritesheet.get_sprite(192, 192, self.width, self.height),
                            self.game.PNJ_spritesheet.get_sprite(256, 192, self.width, self.height)]

        if self.facing == "down":

            self.rect.y += PNJ_SPEED
            self.movement_loop += 1
            self.animate()
            self.image = down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.15
            if self.animation_loop >= 3:
                self.animation_loop = 1
            if self.movement_loop == max_travel_down:
                self.facing = 'right'

        if self.facing == 'right':

            self.rect.x += PNJ_SPEED
            self.movement_loop -= 1
            self.animate()
            self.image = right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.15
            if self.animation_loop >= 3:
                self.animation_loop = 1
            if self.movement_loop == max_travel_right:
                self.facing = 'up'
                self.movement_loop += 10


        if self.facing == 'up':

            self.rect.y -= PNJ_SPEED
            self.movement_loop += 1
            self.animate()
            self.image = up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.15
            if self.animation_loop >= 3:
                 self.animation_loop = 1
            if self.movement_loop ==  max_travel_up:
                self.facing = 'up'
                self.game.pvdumonstre+=1


        if hits:
            pygame.sprite.spritecollide(self, self.game.blocks,True)


    def dialogue(self, image):
        hits= pygame.sprite.spritecollide(self, self.game.player, False)
        if hits:
            self.game.screen.blit(pygame.image.load(image),(160,270))#fenetre de dialogue
            pygame.display.update()

    def animate(self):
        down_animations = [self.game.PNJ_spritesheet.get_sprite(224, 128, self.width, self.height),
                           self.game.PNJ_spritesheet.get_sprite(192, 128, self.width, self.height),
                           self.game.PNJ_spritesheet.get_sprite(256, 128, self.width, self.height)]

        left_animations = [self.game.PNJ_spritesheet.get_sprite(224, 160, self.width, self.height),
                         self.game.PNJ_spritesheet.get_sprite(192, 160, self.width, self.height),
                         self.game.PNJ_spritesheet.get_sprite(256, 160, self.width, self.height)]

        up_animations = [self.game.PNJ_spritesheet.get_sprite(224, 224, self.width, self.height),
                           self.game.PNJ_spritesheet.get_sprite(192, 224, self.width, self.height),
                           self.game.PNJ_spritesheet.get_sprite(256, 224, self.width, self.height)]

        right_animations = [self.game.PNJ_spritesheet.get_sprite(224, 192, self.width, self.height),
                            self.game.PNJ_spritesheet.get_sprite(192, 192, self.width, self.height),
                            self.game.PNJ_spritesheet.get_sprite(256, 192, self.width, self.height)]

        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.PNJ_spritesheet.get_sprite(224, 160, self.width, self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.PNJ_spritesheet.get_sprite(224, 192, self.width, self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.PNJ_spritesheet.get_sprite(224, 224, self.width, self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.PNJ_spritesheet.get_sprite(224, 128, self.width, self.height)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 3:
                    self.animation_loop = 1

class bouledefeu(pygame.sprite.Sprite)  :
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PNJ_LAYER
        self.groups = self.game.all_sprites, self.game.boule_de_feu
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.boule_de_feu_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.x_change = 0
        self.y_change = 0

    def update(self):
        self.movement()

    def movement(self):
        rng=random.randint(1,3)
        if rng==1:
            self.rect.x-=BOULE_DE_FEU_SPEED
            self.rect.y-=0.25
        elif rng==2:
            self.rect.x-=BOULE_DE_FEU_SPEED
            self.rect.y+=0.5
        elif rng==3:
            self.rect.x-=BOULE_DE_FEU_SPEED






class Sorciere(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PNJ_LAYER
        self.groups = self.game.all_sprites, self.game.sorciere, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.sorciere_spritesheet.get_sprite(0, 128, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.x_change = 0
        self.y_change = 0

        self.lance_boule_de_feu=0
        self.attack_player = 0

        self.facing = 'down'
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = 100
        self.compteur= 0

    def update(self):
            self.game.barredevie(self.rect.x,self.rect.y,self.game.pvduboss,100)
            if self.game.boss_actif==1 or self.attack_player==1:
                    self.lance_boule_de_feu+=1
                    self.attack_player=1
                    self.stop_movement()
                    self.hostile()


            else:

                self.movement()
                self.animate()
                self.rect.x += self.x_change
                self.rect.y += self.y_change
                self.x_change = 0
                self.y_change = 0



    def movement(self):
        hits = pygame.sprite.spritecollide(self, self.game.player,False)
        if not hits:
            if self.facing == "up":
                self.y_change -= 1
                self.movement_loop -= 1
                if self.movement_loop <= - self.max_travel:
                    self.facing = 'down'

            if self.facing == "down":
                self.y_change += 1
                self.movement_loop += 1
                if self.movement_loop >= self.max_travel:
                    self.facing = 'up'
        if hits:
            self.x_change=0

    def stop_movement(self):
        self.x_change=0
        self.y_change=0
        self.facing="left"
        self.animate()

    def hostile(self):

        temps_dattaque= 75
        if temps_dattaque==self.lance_boule_de_feu:
            self.lance_boule_de_feu=0
            rng=random.randint(1,3)
            if rng==1:
                self.game.bouledefeu(15,6)
                self.game.bouledefeu(15,9)
            elif rng==2:
                self.game.bouledefeu(15,6)
                self.game.bouledefeu(15,9)
            elif rng==3:
                self.game.bouledefeu(15,6)
                self.game.bouledefeu(15,9)







    def animate(self):
            down_animations = [self.game.sorciere_spritesheet.get_sprite(0, 128, self.width, self.height),
                               self.game.sorciere_spritesheet.get_sprite(32, 128, self.width, self.height),
                               self.game.sorciere_spritesheet.get_sprite(64, 128, self.width, self.height)]

            left_animations = [self.game.sorciere_spritesheet.get_sprite(0, 160, self.width, self.height),
                             self.game.sorciere_spritesheet.get_sprite(32, 160, self.width, self.height),
                             self.game.sorciere_spritesheet.get_sprite(64, 160, self.width, self.height)]

            up_animations = [self.game.sorciere_spritesheet.get_sprite(0, 224, self.width, self.height),
                               self.game.sorciere_spritesheet.get_sprite(32, 224, self.width, self.height),
                               self.game.sorciere_spritesheet.get_sprite(64, 224, self.width, self.height)]

            right_animations = [self.game.sorciere_spritesheet.get_sprite(0, 192, self.width, self.height),
                                self.game.sorciere_spritesheet.get_sprite(32, 192, self.width, self.height),
                                self.game.sorciere_spritesheet.get_sprite(64, 192, self.width, self.height)]

            if self.facing == "left":
                if self.x_change == 0:
                    self.image = self.game.sorciere_spritesheet.get_sprite(0, 160, self.width, self.height)
                else:
                    self.image = left_animations[math.floor(self.animation_loop)]
                    self.animation_loop += 0.15
                    if self.animation_loop >= 3:
                        self.animation_loop = 1

            if self.facing == "right":
                if self.x_change == 0:
                    self.image = self.game.sorciere_spritesheet.get_sprite(0, 192, self.width, self.height)
                else:
                    self.image = right_animations[math.floor(self.animation_loop)]
                    self.animation_loop += 0.15
                    if self.animation_loop >= 3:
                        self.animation_loop = 1

            if self.facing == "up":
                if self.y_change == 0:
                    self.image = self.game.sorciere_spritesheet.get_sprite(0, 224, self.width, self.height)
                else:
                    self.image = up_animations[math.floor(self.animation_loop)]
                    self.animation_loop += 0.15
                    if self.animation_loop >= 3:
                        self.animation_loop = 1

            if self.facing == "down":
                if self.y_change == 0:
                    self.image = self.game.sorciere_spritesheet.get_sprite(0, 128, self.width, self.height)
                else:
                    self.image = down_animations[math.floor(self.animation_loop)]
                    self.animation_loop += 0.15
                    if self.animation_loop >= 3:
                        self.animation_loop = 1

class Statue(pygame.sprite.Sprite):
   def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites,self.game.statue
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.statue_spritesheet.get_sprite(96, 128, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y










class Statue1(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = UP_LAYER
        self.groups = self.game.all_sprites, self.game.statue1
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.statue_spritesheet.get_sprite(96, 96, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class epee(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = HERBE_LAYER
        self.groups = self.game.all_sprites,self.game.crocduloup
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.crocduloup_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class potion_pv(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = HERBE_LAYER
        self.groups = self.game.all_sprites,self.game.potion_pv
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.crocduloup_spritesheet.get_sprite(32, 32, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y




class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.tileset_spritesheet.get_sprite(78, 104.5, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(64, 160, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class GroundMaison(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(384 ,608 , self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class GroundDonjon(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(448 ,160 , self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Declenche_Boss(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites,self.game.declenche_boss
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(448 ,160 , self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Herbe(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = HERBE_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(480, 352, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Noir(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.noir_spritesheet.get_sprite(10, 10, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Escalier1(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites,
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(288, 640, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Escalier2(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.donjon
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(320, 640, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Escalier3(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.donjon
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(288, 608, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Escalier4(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.donjon
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(320, 608, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class House(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = UP_LAYER
        self.groups = self.game.all_sprites,
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.house_spritesheet.get_sprite(248, 98, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class House1(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = HERBE_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.house_spritesheet.get_sprite(248, 130, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class House2(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = HERBE_LAYER
        self.groups = self.game.all_sprites,self.game.entrer
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.house_spritesheet.get_sprite(248, 162, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class House21(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = HERBE_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.house_spritesheet.get_sprite(248, 162, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class House3(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = UP_LAYER
        self.groups = self.game.all_sprites,
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.house_spritesheet.get_sprite(280, 98, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class House4(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = HERBE_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.house_spritesheet.get_sprite(280, 130, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class House5(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = HERBE_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.house_spritesheet.get_sprite(280, 162, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class House6(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = UP_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.house_spritesheet.get_sprite(312, 98, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class House7(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = HERBE_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.house_spritesheet.get_sprite(312, 130, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class House8(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = HERBE_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.house_spritesheet.get_sprite(312, 162, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Chemain(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(608, 96, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Chemain1(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(576, 96, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Chemain2(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(640, 96, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Chemain3(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites,
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(576, 128, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Chemain4(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(608, 32, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Chemain5(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites,
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(608, 128, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Chemain6(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(608, 64, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Chemain7(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(640, 64, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Chemain8(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(576, 64, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Chemain9(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites,
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(640, 128, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Sortie(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites,self.game.sortie
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(640, 128, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Lave(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = HERBE_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(480, 64, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Lave1(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = HERBE_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(512, 64, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Lave2(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = HERBE_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(544, 64, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Lave3(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = HERBE_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(480, 96, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Lave4(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = HERBE_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(512, 96, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Lave5(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = HERBE_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(544, 96, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Lave6(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = HERBE_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(480, 128, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Lave7(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = HERBE_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(512, 128, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Lave8(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = HERBE_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(544, 128, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Lave9(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = HERBE_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(480, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Lave10(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = HERBE_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(480, 32, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Lave11(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = HERBE_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(512, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Lave12(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = HERBE_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(544, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Lave13(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = HERBE_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(512, 32, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Lave14(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = HERBE_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(544, 32, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y