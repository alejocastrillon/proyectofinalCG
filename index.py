#Final project

import pygame
import random
from math import *

posx = 0
posy = -10
size = width, height = [500, 500]
oleadas = 0
reloj = pygame.time.Clock()
jugadores = pygame.sprite.Group()
agents = pygame.sprite.Group()
todos = pygame.sprite.Group()

#Class of Homero Player
class homerPlayer(pygame.sprite.Sprite):
	"""docstring for homerPlayer"""
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([50, 50])
		self.image.fill([255, 255, 255])
		self.rect = self.image.get_rect()
		self.salud = 10
		self.direction = 0
		self.action = 0

	def update(self):
		if self.direction == 1:
			if self.rect.x <= width - 150:
				self.rect.x += 5
		elif self.direction == 2:
			if self.rect.x >= 30:
				self.rect.x -= 5
		elif self.direction == 3:
			if self.rect.y >= 260:
				self.rect.y -= 5
		elif self.direction == 4:
			if self.rect.y <= height - 60:
				self.rect.y += 5
		if self.action == 1:
			self.action = 0

#Enemy agents class
class agentEnemies(pygame.sprite.Sprite):
	"""docstring for agentEnemies"""
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([50, 50])
		self.image.fill([0, 0, 0])
		self.rect = self.image.get_rect()
		self.salud = 5
		self.direction = 0
		self.action = 0

	def update(self, posHomerX, posHomerY):
		if (abs(self.rect.x - posHomerX) + 20) < (abs(self.rect.y - posHomerY) + 20) and abs(self.rect.x - posHomerX) > 20:
			if self.rect.x > posHomerX:
				self.direction = 1
			elif self.rect.x < posHomerX:
				self.direction = 2
		elif (abs(self.rect.x - posHomerX) + 20) > (abs(self.rect.y - posHomerY) + 20) and abs(self.rect.y - posHomerY) > 20:
			if self.rect.y > posHomerY:
				self.direction = 3
			elif self.rect.y < posHomerY:
				self.direction = 4
		elif abs(self.rect.x - posHomerX) <= 20 and abs(self.rect.y - posHomerY) <= 20:
			self.action = 1
		if self.direction == 1:
			self.rect.x += 5
		elif self.direction == 2:
			self.rect.x -= 5
		elif self.direction == 3:
			if self.rect.y >= 260:
				self.rect.y -= 5
		elif self.direction == 4:
			if self.rect.y <= height - 60:
				self.rect.y += 5

def agentEnemiesGenerator():
	if random.randint(0, 100) == 2:
		agent = agentEnemies()
		agent.rect.x = 510
		agent.rect.y = random.randrange(260, height - 60, 5)
		agent.direction = 2
		agents.add(agent)
		todos.add(agent)


def generateAmbient():
	pantalla.blit(imagenFondo, [posx, posy])

if __name__ == '__main__':
	pygame.init()
	imagenFondo = pygame.image.load('source/springfield.png')
	imagenFondoInfo = imagenFondo.get_rect()
	imagenFondoWidth = imagenFondoInfo[2]
	imagenFondoHeight = imagenFondoInfo[3]
	pantalla = pygame.display.set_mode(size)
	homero = homerPlayer()
	homero.rect.x = 0
	homero.rect.y = 400
	jugadores.add(homero)
	todos.add(homero)
	generateAmbient()
	pygame.display.flip()
	done = False
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:
					homero.direction = 1
				elif event.key == pygame.K_l:
					homero.direction = 2
				elif event.key == pygame.K_UP:
					homero.direction = 3
				elif event.key == pygame.K_b:
					homero.direction = 4
				elif event.key == pygame.K_SPACE:
					homero.direction = 0
				elif event.key == pygame.K_p:
					homero.action = 1

		ls_colhomer_agents= pygame.sprite.spritecollide(homero, agents, False)
		for x in ls_colhomer_agents:
			if homero.action == 1:
				x.salud -= 1
			if x.salud == 0:
				agents.remove(x)
				todos.remove(x)

		if homero.direction == 1 and homero.rect.x >= width - 150 and posx >= width - imagenFondoWidth:
			posx -= 5
			for x in agents:
				x.rect.x -= 5
		elif homero.direction == 2 and homero.rect.x < 30 and posx < 0:
			posx += 5

		pantalla.fill([255, 200, 200])
		agentEnemiesGenerator()
		generateAmbient()
		todos.draw(pantalla)
		jugadores.update()
		agents.update(homero.rect.x, homero.rect.y)
		pygame.display.flip()
		reloj.tick(10)