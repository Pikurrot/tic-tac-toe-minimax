from dis import dis
import pygame
from collections import namedtuple

def main():
	pygame.init()
	size = namedtuple("size", "x y")
	size.x,size.y = (600, 600)
	display = pygame.display.set_mode((size.x,size.y))
	pygame.display.set_caption('Tic-tac-toe')
	display.fill((255,255,255))
	running = True
	while running:
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				running = False
		pygame.display.update()

if __name__ == "__main__":
	main()
