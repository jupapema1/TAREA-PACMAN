import sys
import pygame
from res import MYLIB




class Lector():
	def __init__(self):
		self.tecla1=0
		self.tecla2=0

if __name__=='__main__':

	pantalla=pygame.display.set_mode([MYLIB.ANCHO,MYLIB.ALTO])
	pantalla.fill(BLANCO)
	pygame.init()
	reloj=pygame.time.Clock()

	plano=Cartesiano(pantalla)
	plano.ejes()

