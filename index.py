#Final project

import pygame
import random
from math import *

ROJO=[255,0,0]
BLANCO=[255,255,255]
NEGRO=[0,0,0]
AMARILLO=[255,255,0]
posx = 0
posy = -10
size = width, height = [800,600]
oleadas = 0
quantityDonuts = 0
reloj = pygame.time.Clock()
jugadores = pygame.sprite.Group()
agents = pygame.sprite.Group()
donuts = pygame.sprite.Group()
beers = pygame.sprite.Group()
letters = pygame.sprite.Group()
todos = pygame.sprite.Group()
groupStewie = pygame.sprite.Group()
imagenFondo = pygame.image.load('source/springfield.png')
nivel = 1
entrar = False

#Option Class
class Opcion:
    def __init__(self, idop, texto, pos):
        self.id=idop
        self.txt=texto
        self.pos=pos
        self.color_def=BLANCO
        self.ver=False
        self.Marco()
        self.Dibujar()
        self.sonido = False
    def color_actual(self):
        if self.ver:
            return AMARILLO
        else:
            return (ROJO)
    def Marco(self):
        self.titulo=fuente.render(self.txt, True, self.color_actual())
        self.rect=self.titulo.get_rect()
        self.rect.topleft=self.pos
    def Dibujar(self):
        self.Marco()
        pantalla.blit(self.titulo,self.rect)

def PantallaInicio():
    pygame.mixer.init()
    panta = pygame.display.set_mode(size)
    pygame.mixer.music.load('source/sounds/menu.mp3')
    pygame.mixer.music.set_volume(10)
    pygame.mixer.music.play(-1)
    fuente=pygame.font.Font(None,40)
    idd=1
    cont=0
    fin=False
    soni = 0
    while not fin:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin=True
                return 2
            if event.type == pygame.MOUSEBUTTONDOWN:
                for op in opciones:
                    if op.rect.collidepoint(pos):
                        return op.id
                        fin = True

        FuenteTitulo = pygame.font.Font('source/menu/Simpsonfont.ttf', 100)
        Titulo = FuenteTitulo.render(" Fat Agent",True, BLANCO)
        Titulo1 = FuenteTitulo.render(" Fat Agent",True, NEGRO)

        image=pygame.image.load('source/menu/menuprov.jpg').convert_alpha()
        panta.blit(image,[0,0])

        cont+=1
        if cont<25 and cont>=15:
            panta.blit(Titulo,[163,103])
            panta.blit(Titulo1,[160,100])

        if cont<15:
            panta.blit(Titulo,[163,100])
            panta.blit(Titulo1,[160,97])
        else:
            cont=0

        opciones=[Opcion(3, "Salir", [380,450]), Opcion(1, "Empezar", [350,400]), Opcion(2, "Controles", [350,500])]
        for op in opciones:
            if op.rect.collidepoint(pos):
                op.ver=True
            else:
                op.ver=False
            op.Dibujar()

        pygame.display.flip()

def Controles():
    panta = pygame.display.set_mode([800,600])
    fin1=False
    while not fin1:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin1=True
        image=pygame.image.load('source/menu/tuto2.png').convert_alpha()
        panta.blit(image,[0,0])
        pygame.display.flip()


#Donut's class
class Donut(pygame.sprite.Sprite):
	"""docstring for Donuts"""
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('source/donnut.png')
		#self.image.fill([240, 39, 200])
		self.rect = self.image.get_rect()

class Letter(pygame.sprite.Sprite):
	"""docstring for Letter"""
	def __init__(self, matrix):
		pygame.sprite.Sprite.__init__(self)
		self.f = matrix
		self.image = self.f[0][0]
		self.rect = self.image.get_rect()
		self.index = 0

	def update(self):
		self.image = self.f[0][self.index]
		self.index += 1
		if self.index >= 5:
			self.index = 0

class Stewie(pygame.sprite.Sprite):
	"""docstring for Stewie"""
	def __init__(self, matrix):
		super(Stewie, self).__init__()
		self.f = matrix
		self.image = self.f[0][0]
		self.rect = self.image.get_rect()
		self.index = 0
		self.direction = 0
		self.action = 0

	def update(self, posHomerX, posHomerY):
		if (abs(self.rect.x - posHomerX) + 20) < (abs(self.rect.y - posHomerY) + 20) and abs(self.rect.x - posHomerX) > 50:
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
			print "entro"
			self.direction = 0
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

		

#Beer Duff class
class beerDuff(pygame.sprite.Sprite):
	"""docstring for beerDuff"""
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('source/duff.png')
		#self.image.fill([240, 39, 72])
		self.rect = self.image.get_rect()
		


#Class of Homero Player
class homerPlayer(pygame.sprite.Sprite):
	"""docstring for homerPlayer"""
	def __init__(self, matrix):
		pygame.sprite.Sprite.__init__(self)
		self.matrix = matrix
		self.image = self.matrix[0][0]
		self.rect = self.image.get_rect()
		self.salud = 10
		self.direction = 0
		self.winner = False
		self.action = 0
		self.index = 0

	'''Acciones
		1. Caminar
		2. Puno
		3. Defenderse '''

	def update(self):
		if self.direction == 1 and self.action == 1:
			if self.rect.x <= width - 214:
				self.rect.x += 5
			if self.salud >= 5:
				self.image = self.matrix[0][self.index]
				self.index += 1
				if self.index >= 6:
					self.index = 0
			else:
				self.image = self.matrix[3][self.index]
				self.index += 1
				if self.index >= 6:
					self.index = 0

		elif self.direction == 2 and self.action == 1:
			if self.rect.x >= 30:
				self.rect.x -= 5
			if self.salud >= 5:
				self.image = self.matrix[0][self.index]
				self.index += 1
				if self.index >= 6:
					self.index = 0
			else:
				self.image = self.matrix[3][self.index]
				self.index += 1
				if self.index >= 6:
					self.index = 0
		elif self.direction == 3 and self.action == 1:
			if self.rect.y >= 260:
				self.rect.y -= 5
			if self.salud >= 5:
				self.image = self.matrix[0][self.index]
				self.index += 1
				if self.index >= 6:
					self.index = 0
			else:
				self.image = self.matrix[3][self.index]
				self.index += 1
				if self.index >= 6:
					self.index = 0
		elif self.direction == 4 and self.action == 1:
			if self.rect.y <= 500 - 120:
				self.rect.y += 5
			if self.salud >= 5:
				self.image = self.matrix[0][self.index]
				self.index += 1
				if self.index >= 6:
					self.index = 0
			else:
				self.image = self.matrix[3][self.index]
				self.index += 1
				if self.index >= 6:
					self.index = 0
		if self.action == 2:
			self.direction = 0
			self.image = self.matrix[2][self.index]
			self.index += 1
			if self.index >= 3:
				if self.salud >= 5:
					self.image = self.matrix[0][0]
				else:
					self.image = self.matrix[3][0]
				self.index = 0
				self.action = 0
		if self.action == 3:
			self.direction = 0
			self.image = self.matrix[1][self.index]
			self.index += 1
			if self.index >= 3:
				if self.salud >= 5:
					self.image = self.matrix[0][0]
				else:
					self.image = self.matrix[3][0]
				self.index = 0
				self.action = 0



#Enemy agents class
class agentEnemies(pygame.sprite.Sprite):
	"""docstring for agentEnemies"""
	def __init__(self, matrix):
		pygame.sprite.Sprite.__init__(self)
		self.f = matrix
		self.image = self.f[0][0]
		#self.image.fill([0, 0, 0])
		self.rect = self.image.get_rect()
		self.salud = 5
		self.direction = 0
		self.action = 0
		self.index = 0

	def update(self, posHomerX, posHomerY):
		if (abs(self.rect.x - posHomerX) + 20) < (abs(self.rect.y - posHomerY) + 20) and abs(self.rect.x - posHomerX) > 50:
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
			print "entro"
			self.direction = 0
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

		if self.direction != 0:
			self.image = self.f[0][self.index]
			self.index += 1
			if self.index >= 5:
				self.index = 0

		if self.action == 1:
			self.image = self.f[1][self.index]
			self.index += 1
			if self.index >= 4:
				self.index = 0

def recortarSprite(nombreArchivo, cantidadX, cantidadY):
	imageSprite = pygame.image.load(nombreArchivo)
	imageInfo = imageSprite.get_rect()
	imageWidth = imageInfo[2]
	imageHeight = imageInfo[3]
	matrix = []
	corteY = (imageHeight / cantidadY)
	corteX = (imageWidth / cantidadX)
	for y in range(cantidadY):
		matrix.append([])
		for x in range(cantidadX):
			cuadro = imageSprite.subsurface(corteX * x, corteY * y, corteX,corteY)
			matrix[y].append(cuadro)
	return matrix

def agentEnemiesGenerator():
	agenteSprite = recortarSprite('source/AgenteSinFondo.png', 6, 3)
	if random.randint(0, 50) == 2:
		agent = agentEnemies(agenteSprite)
		agent.rect.x = width + 10
		agent.rect.y = random.randrange(260, height - 60, 5)
		agent.direction = 2
		agents.add(agent)
		todos.add(agent)

def positionBeerDuff(quantity):
	for x in xrange(quantity):
		b = beerDuff()
		b.rect.y = random.randrange(260, 500 - 60, 5)
		b.rect.x = random.randrange(5, 4080, 5)
		beers.add(b)
		todos.add(b)

def positionDonuts(quantity):
	for x in xrange(quantity):
		d = Donut();
		d.rect.y = random.randrange(260, 500 - 60, 5)
		d.rect.x = random.randrange(5, 4080, 5)
		donuts.add(d)
		todos.add(d)


def generateAmbient():
	pantalla.blit(imagenFondo, [posx, posy])

if __name__ == '__main__':
	pygame.init()
	pantalla = pygame.display.set_mode(size)
	fuente=pygame.font.Font('source/menu/Simpsonfont.ttf',40)
	a = PantallaInicio()
	if a == 1:
		pygame.mixer.init(0)
		pygame.mixer.music.set_volume(0)
		size = width, heigth = [800, 500]
		pantalla = pygame.display.set_mode(size)
		imagenFondo = pygame.image.load('source/springfield.png')
		imagenFondoInfo = imagenFondo.get_rect()
		imagenFondoWidth = imagenFondoInfo[2]
		imagenFondoHeight = imagenFondoInfo[3]
		homeroSprite = recortarSprite('source/Finalizado_SinFondo.png', 8, 6);
		homero = homerPlayer(homeroSprite)
		homero.rect.x = 0
		homero.rect.y = 400
		cartaSprite = recortarSprite('source/cartaunidasinfondo.png', 6, 1)
		carta = Letter(cartaSprite)
		carta.rect.x = 3950
		carta.rect.y = height - 100
		letters.add(carta)
		todos.add(carta)
		jugadores.add(homero)
		todos.add(homero)
		generateAmbient()
		positionDonuts(20)
		positionBeerDuff(10)
		pygame.display.flip()
		done = False
		while not done:
			if nivel == 2 and entrar == True:
				spriteStewie = recortarSprite('source/FinalizadoSinFondo.png', 4, 5)
				stewiePlayer = Stewie(spriteStewie)
				stewiePlayer.rect.x = 0
				stewiePlayer.rect.y = height - 100
				posx = -10
				groupStewie.add(stewiePlayer)
				todos.add(stewiePlayer)
				entrar = False


			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					done = True
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RIGHT:
						homero.action = 1
						homero.direction = 1
					elif event.key == pygame.K_l:
						homero.action = 1
						homero.direction = 2
					elif event.key == pygame.K_UP:
						homero.action = 1
						homero.direction = 3
					elif event.key == pygame.K_b:
						homero.action = 1
						homero.direction = 4
					elif event.key == pygame.K_SPACE:
						homero.action = 1
						homero.direction = 0
					elif event.key == pygame.K_p:
						homero.action = 2
					elif event.key == pygame.K_d:
						homero.action = 3

			#Colicion entre homero y algun agente, descuenta la salud de un agente si Homero esta dando un golpe
			ls_colhomer_agents= pygame.sprite.spritecollide(homero, agents, False)
			for x in ls_colhomer_agents:
				if homero.action == 2:
					x.salud -= 1
				if x.salud == 0:
					agents.remove(x)
					todos.remove(x)

			#Colicion entre agente y homero, descuenta salud de Homero si el agente esta dando un golpe y Homero no se esta defendiendo
			for ae in agents:
				ls_agente_homero = pygame.sprite.spritecollide(ae, jugadores, False)
				for x in ls_agente_homero:
					print "Salud Homero: ", x.salud
					if ae.action == 1 and x.action != 3:
						x.salud -= 1
					if x.salud == 0:
						jugadores.remove(x)
						todos.remove(x)
						done = True

			#Colicion entre Homero y Donnuts
			ls_col_donuts = pygame.sprite.spritecollide(homero, donuts, True)	
			for x in ls_col_donuts:
				donuts.remove(x)
				todos.remove(x)
				quantityDonuts += 1
				print "Cantidad donuts: ", quantityDonuts

			#Colicion entre Homero y las cervezas Duff
			ls_col_beers = pygame.sprite.spritecollide(homero, beers, True)
			for x in ls_col_beers:
				beers.remove(x)
				todos.remove(x)
				homero.salud += 3
				print "Salud homero: ", homero.salud

			#Colicion entre Homero y Carta
			ls_col_letter = pygame.sprite.spritecollide(homero, letters, False)
			for x in ls_col_letter:
				homero.winner = True
				print "Has ganado"
				nivel += 1
				entrar = True

			#Movimiento de fondo
			if homero.direction == 1 and homero.rect.x >= width - 214 and posx >= width - imagenFondoWidth:
				posx -= 5
				for x in agents:
					x.rect.x -= 5
				for x in donuts:
					x.rect.x -= 5
				for x in beers:
					x.rect.x -= 5
				for x in letters:
					x.rect.x -= 5

			elif homero.direction == 2 and homero.rect.x < 30 and posx < 0:
				posx += 5
				for x in agents:
					x.rect.x += 5
				for x in donuts:
					x.rect.x += 5
				for x in beers:
					x.rect.x += 5
				for x in letters:
					x.rect.x += 5

			pantalla.fill([255, 200, 200])
			if homero.winner == False:
				agentEnemiesGenerator()
			generateAmbient()
			todos.draw(pantalla)
			jugadores.update()
			if nivel == 1:
				agents.update(homero.rect.x, homero.rect.y)
			elif nivel == 2:
				groupStewie.update(homero.rect.x, homero.rect.y)
			letters.update()
			pygame.draw.rect(pantalla, BLANCO,(8,8 ,200 ,14))
			pygame.draw.rect(pantalla, NEGRO,(10,10 , homero.salud ,10))
			pygame.display.flip()
			reloj.tick(15)
	elif a == 2:
		Controles()