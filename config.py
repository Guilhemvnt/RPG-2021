WIN_WIDTH = 640
WIN_HEIGHT = 480
TILESIZE = 32

FPS = 60

PNJ_LAYER = 6
UP_LAYER = 5
PLAYER_LAYER = 4
ENEMY_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1
HERBE_LAYER = 1

PLAYER_SPEED = 3
ENEMY_SPEED = 3
PNJ_SPEED = 2
BOULE_DE_FEU_SPEED = 2


BLACK = (0, 0, 0)
FOND_VERT = (120, 195, 128)
FOND_VERT2 = (70, 235, 125)



tilemap00 = open("map/map00.txt","r")
tilemap01 = open("map/map01.txt","r")
tilemapmaison = open("map/maison.txt","r")
tilemapdonjon = open("map/donjon.txt","r")

tilemap00= tilemap00.readlines()
tilemap01= tilemap01.readlines()
tilemapmaison = tilemapmaison.readlines()
tilemapdonjon = tilemapdonjon.readlines()
