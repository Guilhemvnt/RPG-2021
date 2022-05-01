import pygame

def music_main():# musique du menu
    music_menu = pygame.mixer.Sound('assets_music/musique_menu.ogg')
    pygame.mixer.set_num_channels(3)# on défini sur quel channel jouer le son afin de pour en jouer en meme temps sans interuption du premier
    pygame.mixer.Channel(0).play(music_menu,-1)# l'indice -1 de la fonction sert a jouer la musique en boucle
    

def music_main2():# musique en jeu
    music_menu = pygame.mixer.Sound('assets_music/music_game.ogg')
    pygame.mixer.set_num_channels(2)
    pygame.mixer.Channel(0).play(music_menu,-1)

def play_music():# lancer la musique
     if not pygame.mixer.Channel(0).get_busy():#si il n'y a pas d'autre son dans le channel 0 on lance afin de jouer constament sans avoir a rappeler a chaque la fois la musique
                music_main()

def son_pas():
            pygame.mixer.set_num_channels(2)
            son= pygame.mixer.Sound('assets_music/pas_herbe.ogg')
            pygame.mixer.Channel(1).play(son)
def son_pavé():
        pygame.mixer.Channel(1).play('assets_music/bruit_pavé.ogg')

def son_clic():
            son= pygame.mixer.Sound('assets_music/clic.ogg')
            pygame.mixer.Channel(1).play(son)

def dongeon ():
    
    son= pygame.mixer.Sound('assets_music/music_dongeon.ogg')
    pygame.mixer.Channel(0).play(son)

def boss_music ():
    son= music_menu = pygame.mixer.Sound('assets_music/Desert.ogg')
    pygame.mixer.Channel(0).play(son) 