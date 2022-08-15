import pygame
from collections import namedtuple
import numpy as np

pygame.init()
display_size = namedtuple("display_size", "x y")
display_size.x,display_size.y = (400, 500)
display = pygame.display.set_mode((display_size.x,display_size.y))
pygame.display.set_caption('Tic-tac-toe')
buttons = []
turn = "x"
empty_board = np.array([
	["","",""],
	["","",""],
	["","",""]
	])

# Board func
def reset_board():
	global board, turn
	board = np.copy(empty_board)
	turn = "x"

def board_status(arg_board):
	for mark in ("x","o"):
		if 	(arg_board[0,0],arg_board[0,1],arg_board[0,2]) == (mark,)*3 or\
			(arg_board[1,0],arg_board[1,1],arg_board[1,2]) == (mark,)*3 or\
			(arg_board[2,0],arg_board[2,1],arg_board[2,2]) == (mark,)*3 or\
			(arg_board[0,0],arg_board[1,0],arg_board[2,0]) == (mark,)*3 or\
			(arg_board[0,1],arg_board[1,1],arg_board[2,1]) == (mark,)*3 or\
			(arg_board[0,2],arg_board[1,2],arg_board[2,2]) == (mark,)*3 or\
			(arg_board[0,0],arg_board[1,1],arg_board[2,2]) == (mark,)*3 or\
			(arg_board[0,2],arg_board[1,1],arg_board[2,0]) == (mark,)*3: return mark
		elif "" not in arg_board: return "draw"
		else: return "none"

def possible_boards(arg_tree, arg_turn):
	if board_status(arg_tree.val) == "none":
		boards = []
		for (row,lst) in enumerate(arg_tree.val):
			for (col,val) in enumerate(lst):
				if val == "":
					temp_board = np.copy(arg_tree.val)
					temp_board[row][col] = arg_turn
					boards.append(temp_board)
		for i,sub_board in enumerate(boards):
			arg_tree.add_node(sub_board)
			if arg_turn == "x": next_turn = "o"
			else: next_turn = "x"
			possible_boards(arg_tree.nodes[i], next_turn)
	else: 
		return

# General func
def move_AI():
	boards = Tree(board)
	possible_boards(boards, "o")
	print(boards)

def draw_GUI():
	width = 10
	display.fill((255,255,255))
	# Draw grid
	for x in range(0,4):
		pygame.draw.line(display, (100,100,100), (display_size.x*(x/3),0), (display_size.x*(x/3),display_size.x), width)
	for y in range(0,4):
		pygame.draw.line(display, (100,100,100), (0,display_size.x*(y/3)), (display_size.x,display_size.x*(y/3)), width)
	# Draw buttons
	for button in buttons:
		button.draw()
	pygame.display.update()

# Classes
class Tree():
	def __init__(self, val):
		self.val = val
		self.nodes = []
		
	def add_node(self, val):
		self.nodes.append(Tree(val))

	def __repr__(self):
		return f"""
Parent:
{self.val}
Childs:
{self.nodes}"""

class Button():
	def __init__(self, pos, w, h, func, border=0, radius=0, show=False, text="", color1=(255,255,255), color2=(0,0,0)):
		self.x, self.y = pos
		self.w = w
		self.h = h
		self.border = border
		self.radius = radius
		self.show = show
		self.text = text
		self.func = func # if it's a tile, func must be (x,y) --> position in "board"
		self.rect = pygame.Rect(self.x-self.w/2,self.y-self.h/2,self.w,self.h)
		self.color1 = (color1[0],color1[1],color1[2],show)
		self.color2 = (color2[0],color2[1],color2[2],show)
		self.clicked = False
		self.text_size = int(display_size.y/15)
		self.text_font = pygame.font.SysFont('Calibri', self.text_size)
		self.tile_font = pygame.font.SysFont('Calibri', int(display_size.x/3))

	def click(self):
		global turn
		mouse_x, mouse_y = pygame.mouse.get_pos()
		if self.rect.collidepoint(mouse_x, mouse_y):
			if type(self.func) == tuple:
				if board[self.func[1],self.func[0]] == "":
					board[self.func[1],self.func[0]] = "x"
			elif self.func == "restart":
				reset_board()
			elif self.func == "start AI" and self.show:
				turn = "o"
		if self.func == "start AI":
			self.show = np.array_equal(board,empty_board)

	def draw(self):
		if type(self.func) == tuple:
			self.text = board[self.func[1],self.func[0]]
			text = self.tile_font.render(self.text,True,(0,0,0))
			text_rect = text.get_rect(center=(self.x,self.y))
			display.blit(text,text_rect)
		elif self.show:
			pygame.draw.rect(display, self.color1, self.rect, border_radius=self.radius)
			if self.border!=0:
				pygame.draw.rect(display, self.color2, self.rect, int(self.border), self.radius)
			text = self.text_font.render(self.text,True,(0,0,0))
			text_rect = text.get_rect(center=(self.x,self.y))
			display.blit(text,text_rect)

def main():
	reset_board()
	for (row,lst) in enumerate(board):
		for (col,val) in enumerate(lst):
			x = display_size.x*((col+1)/3)-display_size.x/6
			y = display_size.x*((row+1)/3)-display_size.x/6
			button = Button((x,y),display_size.x/3,display_size.x/3,(col,row))
			buttons.append(button)
	b_sep_x = display_size.x/10
	b_sep_y = display_size.y/10
	b_w = display_size.x/2
	b_h = (display_size.y-display_size.x)
	b_color = (30,144,255)
	buttons.append(Button((display_size.x/4, display_size.y-b_h/2), b_w-b_sep_x, b_h-b_sep_y, "restart", display_size.x/50, 10, True, "Restart", b_color))
	buttons.append(Button((display_size.x/4*3, display_size.y-b_h/2), b_w-b_sep_x, b_h-b_sep_y, "start AI", display_size.x/50, 10, True, "Start AI", b_color))
	running = True
	draw_GUI()
	while running:
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				if pygame.mouse.get_pressed()[0]:
					for button in buttons:
						button.click()
					draw_GUI()
	move_AI()

if __name__ == "__main__":
	main()
