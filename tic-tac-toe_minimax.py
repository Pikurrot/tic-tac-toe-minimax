import pygame
from collections import namedtuple
import numpy as np
from random import randint

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
test_board = np.array([
	["x","",""],
	["","o",""],
	["o","x","x"]
	])
board = np.copy(empty_board)
end = False

# Board func
def show_board(arg_board):
	str_board = ""
	for lst in arg_board:
		string = "["
		for mark in lst:
			if mark == "": string += " "
			else: string += mark
			string += "  "
		string = string[:-2]
		str_board += string+"]\n"
	str_board = str_board[:-1]
	return str_board

def reset_board():
	global board, turn
	board = np.copy(empty_board)
	turn = "x"

def board_status(arg_board): 
	# Return the status of given board
	# 1 = Win, 0 = Draw, -1 = Lose, None = Players can still move
	for mark in ("x","o"):
		if 	((arg_board[0][0],arg_board[0][1],arg_board[0][2]) == (mark,)*3 or\
			(arg_board[1][0],arg_board[1][1],arg_board[1][2]) == (mark,)*3 or\
			(arg_board[2][0],arg_board[2][1],arg_board[2][2]) == (mark,)*3 or\
			(arg_board[0][0],arg_board[1][0],arg_board[2][0]) == (mark,)*3 or\
			(arg_board[0][1],arg_board[1][1],arg_board[2][1]) == (mark,)*3 or\
			(arg_board[0][2],arg_board[1][2],arg_board[2][2]) == (mark,)*3 or\
			(arg_board[0][0],arg_board[1][1],arg_board[2][2]) == (mark,)*3 or\
			(arg_board[0][2],arg_board[1][1],arg_board[2][0]) == (mark,)*3): 
			if (mark == "o"): return 1
			else: return -1
	if "" not in arg_board: return 0
	else: return None

def move_pos(board1, board2):
	# Return the position of the mark that has changed from board1 to board2
	for row,(lst1,lst2) in enumerate(zip(board1,board2)):
		for col,(val1,val2) in enumerate(zip(lst1,lst2)):
			if val1 != val2:
				return (row,col)
	return None

def possible_boards(arg_tree, arg_turn):
	# Grow arg_tree (a Tree obj) to a Tree of all possible boards
	# Recursive func
	if board_status(arg_tree.val) == None:
		boards = []
		# Possible boards of the given board (arg_tree.val)
		for (row,lst) in enumerate(arg_tree.val):
			for (col,val) in enumerate(lst):
				if val == "":
					temp_board = np.copy(arg_tree.val)
					temp_board[row][col] = arg_turn
					boards.append(temp_board)
		# Repeat algorithm with every child board
		for i,sub_board in enumerate(boards):
			arg_tree.add_child(sub_board)
			if arg_turn == "x": temp_turn = "o"
			else: temp_turn = "x"
			arg_tree.childs[i] = possible_boards(arg_tree.childs[i], temp_turn)
	return arg_tree

def minimax(arg_tree, arg_turn, board_id="board 1"):
	# Return list of points for every possible immediate move
	# Recursive func
	points = []
	if arg_turn == "x": arg_turn = "o"
	else: arg_turn = "x"
	for i,tmp_child in enumerate(arg_tree.childs):
		# Calculate point of child board according to its board status
		point = board_status(tmp_child.val)
		if point == None:
			# If the game is still playable (no win, no lose, no draw), repeat algorithm with child board
			if arg_turn == "x": # opponent move
				point = min(minimax(tmp_child,arg_turn,board_id+"."+str(i)))
			else: # AI move
				point = max(minimax(tmp_child,arg_turn,board_id+"."+str(i)))
		points.append(point)
# 		print(f"""
# {board_id+"."+str(i)}: 
# {show_board(tmp_child.val)}
# turn: {arg_turn}
# points: {points}
# 		""")
	return points

# General func
def move_AI():
	global turn, board
	if np.array_equal(board,empty_board):
		# If the board is empty, start in a random corner (best starting points)
		best_moves = [(0,0),(0,2),(2,0),(2,2)]
		pos = best_moves[randint(0,len(best_moves)-1)]
	else:
		boards = possible_boards(Tree(board),turn) # Grow the Tree to possible boards
		points = minimax(boards,turn) # Calculate points of possible immediate moves
# 		print(f"""
# {"board 1"}: 
# {show_board(boards.val)}
# turn: {turn}
# points: {points}
# 		""")
		best_move = boards.childs[points.index(max(points))].val # Calculate best move
		pos = move_pos(board,best_move)	 # Calculate its position
	board[pos[0],pos[1]] = turn # Move to that position
	if turn == "x":
		turn = "o"
	else:
		turn = "x"
	print(f"AI move: ({pos[0]},{pos[1]})")

def draw_board(x, y, w, h, arg_board=board, draw_marks=True):
	pygame.draw.rect(display, (255,255,255), pygame.Rect(x-w/2,y-h/2,w,h))
	# Draw grid
	for x2 in range(0,4):
		pygame.draw.line(display, (100,100,100), (x-w/2+w*(x2/3),y-h/2), (x-w/2+w*(x2/3),y+h/2), int(w/50))
	for y2 in range(0,4):
		pygame.draw.line(display, (100,100,100), (x-w/2,y-h/2+h*(y2/3)), (x+w/2,y-h/2+h*(y2/3)), int(h/50))
	if draw_marks:
		# Draw marks
		mark_font = pygame.font.SysFont('Calibri', int(w/3))
		for (row,lst) in enumerate(arg_board):
			for (col,mark) in enumerate(lst):
				mark = mark_font.render(mark,True,(0,0,0))
				mark_rect = mark.get_rect(center=(x+w/3*(col-1),y+h/3*(row-1)))
				display.blit(mark,mark_rect)

def draw_GUI():
	display.fill((255,255,255))
	# Draw grid
	draw_board(display_size.x/2,display_size.x/2,display_size.x,display_size.x,draw_marks=False)
	# Draw buttons
	for button in buttons:
		button.draw()
	pygame.display.update()

# Classes
class Tree():
	def __init__(self, val):
		self.val = val
		self.childs = []
		
	def add_child(self, child):
		self.childs.append(Tree(child)) # child --> val

	def __repr__(self):
		return f"""
Val:
{self.val}
Childs:
{self.childs}"""

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
		global turn, end
		mouse_x, mouse_y = pygame.mouse.get_pos()
		if self.rect.collidepoint(mouse_x, mouse_y):
			if type(self.func) == tuple:
				if board[self.func[1],self.func[0]] == "":
					board[self.func[1],self.func[0]] = "x"
					turn = "o"
			elif self.func == "restart":
				end = False
				reset_board()
			elif self.func == "start AI" and self.show:
				turn = "o"
				self.show = False
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
	global end
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
						if (not end or button.func == "restart"):
							button.click()
					draw_GUI()
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_ESCAPE:
					running = False
		status = board_status(board)
		if not end:
			if status == None:
				if turn == "o":
					move_AI()
					draw_GUI()
			else:
				print("Drawing", status)
				if status == -1:
					text_color = (0,255,0)
					end_text ="You win!"
				elif status == 1:
					text_color = (255,0,0)
					end_text ="AI wins!"
				else:
					text_color = (150,150,150)
					end_text ="Draw!"
				text_size = int(display_size.y/7)
				text_font = pygame.font.SysFont('Consolas', text_size)
				end_text = text_font.render(end_text,True,text_color)
				text_rect = end_text.get_rect(center=(display_size.x/2,display_size.x/2))
				display.blit(end_text,text_rect)
				pygame.display.update()
				end = True

if __name__ == "__main__":
	main()
