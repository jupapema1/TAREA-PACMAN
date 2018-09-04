import pygame 
import math

ANCHO=800
ALTO=800
ROJO=[255,0,0]
AZUL=[0,0,255]
VERDE=[0,255,0]
BLANCO=[255,255,255]
NEGRO=[0,0,0]
CENTRO={ANCHO/2,ALTO/2}


class Cartesiano():
	def __init__(self,pantalla):
		self.pan=pantalla


	def Ejes(self):
		pygame.draw.line(self.pan,ROJO,[0,0],[ANCHO,ALTO],1)
        # pygame.draw.line(self.pan,ROJO,[0,c[1]],[ANCHO,c[1]],1)


