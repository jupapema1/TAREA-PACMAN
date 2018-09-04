import pygame, sys, os, random
from pygame.locals import *

SCRIPT_PATH=sys.path[0]

TILE_WIDTH=TILE_HEIGHT=24

# NO_GIF_TILES -- tile numbers which do not correspond to a GIF file
# currently only "23" for the high-score list
NO_GIF_TILES=[23]

NO_WX=0 # if set, the high-score code will not attempt to ask the user his name
USER_NAME="User" # USER_NAME=os.getlogin() # the default user name if wx fails to load or NO_WX
                 # Oops! os.getlogin() only works if you launch from a terminal
# constants for the high-score display
HS_FONT_SIZE=14
HS_LINE_HEIGHT=16
HS_WIDTH=408
HS_HEIGHT=120
HS_XOFFSET=48
HS_YOFFSET=384
HS_ALPHA=200

# new constants for the score's position
SCORE_XOFFSET=50 # pixels from left edge
SCORE_YOFFSET=34 # pixels from bottom edge (to top of score)
SCORE_COLWIDTH=13 # width of each character

# Joystick defaults - maybe add a Preferences dialog in the future?
JS_DEVNUM=0 # device 0 (pygame joysticks always start at 0). if JS_DEVNUM is not a valid device, will use 0
JS_XAXIS=0 # axis 0 for left/right (default for most joysticks)
JS_YAXIS=1 # axis 1 for up/down (default for most joysticks)
JS_STARTBUTTON=9 # button number to start the game. this is a matter of personal preference, and will vary from device to device

# See GetCrossRef() -- where these colors occur in a GIF, they are replaced according to the level file
IMG_EDGE_LIGHT_COLOR = (0xff,0xce,0xff,0xff)
IMG_FILL_COLOR = (0x84,0x00,0x84,0xff)
IMG_EDGE_SHADOW_COLOR = (0xff,0x00,0xff,0xff)
IMG_PELLET_COLOR = (0x80,0x00,0x80,0xff)



#//////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////
#PACMAN CLASS
#//////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////

class pacman():
	"""docstring for pacman"""
	def __init__(self):
		self.x = 0
		self.y = 0
		self.velX = 0
		self.velY = 0
		self.speed = 3

		self.homeX = 0
		self.homeY = 0

		self.anim_pacmanL = {}
		self.anim_pacmanR = {}
		self.anim_pacmanU = {}
		self.anim_pacmanD = {}
		self.anim_pacmanS = {}
		self.anim_pacmanCurrent = {}
		
		for i in range(1, 9, 1):
			self.anim_pacmanL[i] = pygame.image.load(os.path.join(SCRIPT_PATH,"res","sprite","pacman-l " + str(i) + ".gif")).convert()
			self.anim_pacmanR[i] = pygame.image.load(os.path.join(SCRIPT_PATH,"res","sprite","pacman-r " + str(i) + ".gif")).convert()
			self.anim_pacmanU[i] = pygame.image.load(os.path.join(SCRIPT_PATH,"res","sprite","pacman-u " + str(i) + ".gif")).convert()
			self.anim_pacmanD[i] = pygame.image.load(os.path.join(SCRIPT_PATH,"res","sprite","pacman-d " + str(i) + ".gif")).convert()
			self.anim_pacmanS[i] = pygame.image.load(os.path.join(SCRIPT_PATH,"res","sprite","pacman.gif")).convert()

		self.pelletSndNum = 0


	def Move(self):
		print ("Move is not implemented yet")

#//////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////
#LEVEL CLASS
#//////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////

class level():

	def __init__(self):

		self.lvlWidth = 0
		self.lvlHeight = 0
		self.edgeLightColor = (255, 255, 0, 255)
		self.edgeShadowColor = (255, 150, 0, 255)
		self.fillColor = (0, 255, 255, 255)
		self.pelletColor = (255, 255, 255, 255)
		
		self.map = {}
		
		self.pellets = 0
		self.powerPelletBlinkTimer = 0

	def drawMap (self,thisGame,tileID):
		
		self.powerPelletBlinkTimer += 1
		if self.powerPelletBlinkTimer == 60:
			self.powerPelletBlinkTimer = 0
		
		for row in range(-1, thisGame.screenTileSize[0] +1, 1):
			outputLine = ""
			for col in range(-1, thisGame.screenTileSize[1] +1, 1):

				# row containing tile that actually goes here
				actualRow = thisGame.screenNearestTilePos[0] + row
				actualCol = thisGame.screenNearestTilePos[1] + col

				useTile = self.getMapTile((actualRow, actualCol))
				if not useTile == 0 and not useTile == tileID['door-h'] and not useTile == tileID['door-v']:
					# if this isn't a blank tile

					if useTile == tileID['pellet-power']:
						if self.powerPelletBlinkTimer < 30:
							screen.blit (tileIDImage[ useTile ], (col * TILE_WIDTH - thisGame.screenPixelOffset[0], row * TILE_HEIGHT - thisGame.screenPixelOffset[1]) )

					elif useTile == tileID['showlogo']:
						screen.blit (thisGame.imLogo, (col * TILE_WIDTH - thisGame.screenPixelOffset[0], row * TILE_HEIGHT - thisGame.screenPixelOffset[1]) )
					
					elif useTile == tileID['hiscores']:
					        screen.blit(thisGame.imHiscores,(col*TILE_WIDTH-thisGame.screenPixelOffset[0],row*TILE_HEIGHT-thisGame.screenPixelOffset[1]))
					
					else:
						screen.blit (tileIDImage[ useTile ], (col * TILE_WIDTH - thisGame.screenPixelOffset[0], row * TILE_HEIGHT - thisGame.screenPixelOffset[1]) )
		


	def setMapTile (self, (row, col), newValue):
		self.map[ (row * self.lvlWidth) + col ] = newValue

	def getMapTile (self, (row, col)):
		if row >= 0 and row < self.lvlHeight and col >= 0 and col < self.lvlWidth:
			return self.map[ (row * self.lvlWidth) + col ]
		else:
			return 0

	
	def loadLevel(self,numNivel,player):

		self.map={}
		self.pellets=0

		f = open(os.path.join(SCRIPT_PATH,"res","levels",str(numNivel) + ".txt"), 'r')
		lineNum=-1
		rowNum = 0
		useLine = False
		isReadingLevelData = False

		for line in f:
			lineNum+=1
			
			while len(line)>0 and (line[-1]=="\n" or line[-1]=="\r"): 
				line=line[:-1]
			while len(line)>0 and (line[0]=="\n" or line[0]=="\r"): 
				line=line[1:]
			str_splitBySpace = line.split(' ')

			j=str_splitBySpace[0]

			if (j=="'" or j==''):
				useLine=False

			elif j=='#':
				useLine = False
					
				firstWord = str_splitBySpace[1]

				if firstWord == "lvlwidth":
					self.lvlWidth = int( str_splitBySpace[2] )
					# print "Width is " + str( self.lvlWidth )
				
				elif firstWord == "lvlheight":
					self.lvlHeight = int( str_splitBySpace[2] )
					# print "Height is " + str( self.lvlHeight )
					
				elif firstWord == "edgecolor":
					# edge color keyword for backwards compatibility (single edge color) mazes
					red = int( str_splitBySpace[2] )
					green = int( str_splitBySpace[3] )
					blue = int( str_splitBySpace[4] )
					self.edgeLightColor = (red, green, blue, 255)
					self.edgeShadowColor = (red, green, blue, 255)
					
				elif firstWord == "edgelightcolor":
					red = int( str_splitBySpace[2] )
					green = int( str_splitBySpace[3] )
					blue = int( str_splitBySpace[4] )
					self.edgeLightColor = (red, green, blue, 255)
				
				elif firstWord == "edgeshadowcolor":
					red = int( str_splitBySpace[2] )
					green = int( str_splitBySpace[3] )
					blue = int( str_splitBySpace[4] )
					self.edgeShadowColor = (red, green, blue, 255)

				elif firstWord == "fillcolor":
					red = int( str_splitBySpace[2] )
					green = int( str_splitBySpace[3] )
					blue = int( str_splitBySpace[4] )
					self.fillColor = (red, green, blue, 255)
					
				elif firstWord == "pelletcolor":
					red = int( str_splitBySpace[2] )
					green = int( str_splitBySpace[3] )
					blue = int( str_splitBySpace[4] )
					self.pelletColor = (red, green, blue, 255)
					
					
				elif firstWord == "startleveldata":
					isReadingLevelData = True
				        # print "Level data has begun"
					rowNum = 0
					
				elif firstWord == "endleveldata":
					isReadingLevelData = False
					# print "Level data has ended"
			else:
			 	useLine=True

			if useLine==True:

				if isReadingLevelData== True:
					for k in range(self.lvlWidth):
						self.setMapTile((rowNum,k),int(str_splitBySpace[k]))
						thisID=int(str_splitBySpace[k])
						if thisID==4:
							print("Iniciando posicion para pacman")
							player.homeX=k*TILE_WIDTH
							player.homeY=rowNum*TILE_HEIGHT
							self.setMapTile((rowNum,k),0)


#//////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////
#GAME CLASS
#//////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////


class game():

	def __init__(self):

		# variables de modos de juego
		# 1 = En espera
		# 2 = Listo
		# 3 = game over
		# 4 = En juego

		self.nivel=0
		self.modo=0
		self.contModo=0
		self.puntaje=0

		self.setMode(1)
		self.screenPixelPos = (0, 0) # absolute x,y position of the screen from the upper-left corner of the level
		self.screenNearestTilePos = (0, 0) # nearest-tile position of the screen from the UL corner
		self.screenPixelOffset = (0, 0) # offset in pixels of the screen from its nearest-tile position
		
		self.screenTileSize = (23, 21)
		self.screenSize = (self.screenTileSize[1] * TILE_WIDTH, self.screenTileSize[0] * TILE_HEIGHT)
		
		# numerical display digits
		self.digit = {}
	def setMode (self, newMode):
		self.modo = newMode
		self.contModo = 0
		print('Ahora el nuevo modo de juego es'+str(newMode))


	def StartNewGame (self,newLevel):
		self.nivel = 1
		self.score = 0
		self.lives = 3
		
		self.SetMode(4)
		newLevel.LoadLevel(self.getLevelNum())

	def getLevelNum(self):
		return self.nivel


def CheckIfCloseButton(events):
	for event in events: 
		if event.type == QUIT: 
			sys.exit(0)

#//////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////
#MAIN
#//////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////

def main():

	# Must come before pygame.init()
	pygame.mixer.pre_init(22050,16,2,512)
	pygame.mixer.init()


	clock = pygame.time.Clock()
	pygame.init()

	window = pygame.display.set_mode((1, 1))
	pygame.display.set_caption("Pacman")

	screen = pygame.display.get_surface()

	img_Background = pygame.image.load(os.path.join(SCRIPT_PATH,"res","backgrounds","1.gif")).convert()


	snd_pellet = {}
	snd_pellet[0] = pygame.mixer.Sound(os.path.join(SCRIPT_PATH,"res","sounds","pellet1.wav"))
	snd_pellet[1] = pygame.mixer.Sound(os.path.join(SCRIPT_PATH,"res","sounds","pellet2.wav"))
	snd_powerpellet = pygame.mixer.Sound(os.path.join(SCRIPT_PATH,"res","sounds","powerpellet.wav"))
	snd_eatgh = pygame.mixer.Sound(os.path.join(SCRIPT_PATH,"res","sounds","eatgh2.wav"))
	snd_fruitbounce = pygame.mixer.Sound(os.path.join(SCRIPT_PATH,"res","sounds","fruitbounce.wav"))
	snd_eatfruit = pygame.mixer.Sound(os.path.join(SCRIPT_PATH,"res","sounds","eatfruit.wav"))
	snd_extralife = pygame.mixer.Sound(os.path.join(SCRIPT_PATH,"res","sounds","extralife.wav"))

	ghostcolor = {}
	ghostcolor[0] = (255, 0, 0, 255)
	ghostcolor[1] = (255, 128, 255, 255)
	ghostcolor[2] = (128, 255, 255, 255)
	ghostcolor[3] = (255, 128, 0, 255)
	ghostcolor[4] = (50, 50, 255, 255) # blue, vulnerable ghost
	ghostcolor[5] = (255, 255, 255, 255) # white, flashing ghost


	#      __________________
	# ___/  main code block  \_____________________________________________________

	# create the pacman
	player1 = pacman()

	tileIDName = {} # gives tile name (when the ID# is known)
	tileID = {} # gives tile ID (when the name is known)
	tileIDImage = {} # gives tile image (when the ID# is known)

	# create game and level objects and load first level
	thisGame = game()

	thisLevel = level()
	thisLevel.loadLevel(thisGame.getLevelNum(),player1)

	window = pygame.display.set_mode( thisGame.screenSize, pygame.HWSURFACE | pygame.DOUBLEBUF )

	# initialise the joystick
	if pygame.joystick.get_count()>0:
	  if JS_DEVNUM<pygame.joystick.get_count(): js=pygame.joystick.Joystick(JS_DEVNUM)
	  else: js=pygame.joystick.Joystick(0)
	  js.init()
	else: js=None

	while True: 

		# variables de modos de juego
		# 1 = En espera
		# 2 = Listo
		# 3 = En juego

		CheckIfCloseButton( pygame.event.get() )
		if thisGame.modo==1:
			print("1 Juego en modo espera")

		elif thisGame.modo==2:
			print("2 Juego en modo listo")

		elif thisGame.modo==1:
			print("3 En modo juego")

		else:
			print("Modo de juego no valido")

		#thisLevel.drawMap(thisGame,tileID)

	
		screen.blit(img_Background, (0, 0))
		pygame.display.flip()
		clock.tick (60)




if __name__=='__main__':
	main()