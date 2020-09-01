import tkinter as tk
import tkinter.font as tkFont
import array
import time
from numpy import random

#Constants
master = tk.Tk()
BORDER_COLOR = "steel blue"
BOX_WIDTH = 2
BOARD_SIZE = 20
START_SIZE = 4
UP = 98
LEFT = 100
RIGHT = 102
DOWN = 104
#globals
curr_dir = RIGHT
score = START_SIZE
board_arr = []
board_val = []
food = []
snake_head = [int(BOARD_SIZE/2), int(BOARD_SIZE/2 + START_SIZE/2)-1]
snake_tail = [int(BOARD_SIZE/2), int(BOARD_SIZE/2-START_SIZE/2)]
snake_main = []
fontStyle = tkFont.Font(family="Lucida Grande", size = 9)
started = False
game_done = False
def key(event):
	global curr_dir, started
	if(not started):
		var = tk.StringVar()
		var.set('			                            ')
		start_label = tk.Label(master, text = var.get(), font = fontStyle,
				bg=BORDER_COLOR, fg = "white")
		start_label.grid(row = BOARD_SIZE+1, column = 1, columnspan = BOARD_SIZE)
		started = True
		if(event.keycode == UP or event.keycode == DOWN or
		  event.keycode == LEFT or event.keycode == RIGHT):
			curr_dir = event.keycode 
		onUpdate()
	if(event.keycode == UP or event.keycode == DOWN or
	  event.keycode == LEFT or event.keycode == RIGHT):
		if(curr_dir == RIGHT and event.keycode != LEFT and event.keycode != RIGHT):
			curr_dir = event.keycode
			move()
		elif(curr_dir == LEFT and event.keycode != LEFT and event.keycode != RIGHT):
			curr_dir = event.keycode
			move()
		elif(curr_dir == UP and event.keycode != DOWN and event.keycode != UP):	
			curr_dir = event.keycode
			move()
		elif(curr_dir == DOWN and event.keycode != DOWN and event.keycode != UP):
			curr_dir = event.keycode
			move()
		else:
			pass	
	else:
		pass
def onUpdate():
	move()
	if(not game_done):
		master.after(125, onUpdate)
def move():
	global snake_head, curr_dir, food
	move_data = hit_wall()
	if(move_data[2]):
		end_game()
	else:
		if(snake_head[0] == food[0] and snake_head[1] == food[1]):
			new_food()
		else:	
			#New Head
			head_change(move_data[0], move_data[1])
			#Remove tail
			tail_change()		
def new_food():
	global score
	score = score + 1
	score_w = tk.Label(master, text = "SCORE: " + str(score), font=fontStyle, bg=BORDER_COLOR, fg = "white")
	score_w.grid(row = 0,column = 0, columnspan=4)
	rand_num1 = random.randint(BOARD_SIZE)
	rand_num2 = random.randint(BOARD_SIZE)
	while(board_val[rand_num1][rand_num2]):
		rand_num1 = random.randint(BOARD_SIZE)
		rand_num2 = random.randint(BOARD_SIZE)
	food[0] = rand_num1
	food[1] = rand_num2
	board_arr[rand_num1][rand_num2].config(bg = "white")
	move_data = hit_wall()
	if(move_data[2]):
		end_game()
	else:
		#Only adding head makes snake longer
		head_change(move_data[0], move_data[1])
def hit_wall():
	global curr_dir
	dir = curr_dir
	if(dir == RIGHT):
		new_pos = snake_head[1]+1
		old_pos = snake_head[0]
		#Check game over
		if(new_pos >= BOARD_SIZE or board_val[old_pos][new_pos]):
			return [old_pos, new_pos, True]
		else:
			return [old_pos, new_pos, False]
	elif(dir == LEFT):
		new_pos = snake_head[1]-1
		old_pos = snake_head[0]
		#Check game over
		if(new_pos < 0 or board_val[old_pos][new_pos]):
			return [old_pos, new_pos, True]
		else:
			return [old_pos, new_pos, False]
	elif(dir == UP):
		new_pos = snake_head[0]-1 
		old_pos = snake_head[1]
		#Check game over
		if(new_pos < 0 or board_val[new_pos][old_pos]):
			return [new_pos, old_pos, True]
		else:
			return [new_pos, old_pos, False]
	elif(dir == DOWN):
		new_pos = snake_head[0]+1 
		old_pos = snake_head[1]   
		#Check game over
		if(new_pos >= BOARD_SIZE or board_val[new_pos][old_pos]):
			return [new_pos, old_pos, True]
		else:
			return [new_pos, old_pos, False]
def head_change(loc_x, loc_y):
	if(not game_done):
		global snake_head, board_val, board_arr, longer
		snake_head = [loc_x, loc_y]
		snake_main.insert(0, [loc_x, loc_y])
		snake_main[1].append([loc_x, loc_y])
		board_arr[loc_x][loc_y].config(bg = "blue")
		board_val[loc_x][loc_y] = True
def tail_change():
	if(not game_done):
		global snake_tail, board_val
		tail_x = snake_tail[0]
		tail_y = snake_tail[1]
		if (tail_x+tail_y)%2 == 0:
			board_arr[tail_x][tail_y].config(bg="light slate gray")
		else:
			board_arr[tail_x][tail_y].config(bg="cornflower blue")
		board_val[tail_x][tail_y] = False
		snake_main.pop()
		snake_tail = snake_main[len(snake_main)-1].copy()
def end_game():
	global game_done
	game_done = True
	restart_w = tk.Button(master, text = "Restart", font = fontStyle, bg = BORDER_COLOR, fg = "white", command = restart)
	restart_w.grid(row = 0, column = BOARD_SIZE-5, columnspan = 4)
def restart():
	global score, started, game_done, snake_head, snake_tail
	snake_head = [int(BOARD_SIZE/2), int(BOARD_SIZE/2 + START_SIZE/2)-1]
	snake_tail = [int(BOARD_SIZE/2), int(BOARD_SIZE/2-START_SIZE/2)]
	score = START_SIZE
	started = False
	game_done = False
	restart_w = tk.Label(master, text = "         ",
			font = fontStyle, bg = BORDER_COLOR, fg = "white")
	restart_w.grid(row = 0, column = BOARD_SIZE-5, columnspan = 4)
	board_draw()
	master.mainloop()
def board_draw():
	frame = tk.Frame(master, bg=BORDER_COLOR)
	#KeyListener
	frame.bind("<Key>", key)
	frame.grid(row = 0, column = 0)
	frame.focus_set() 
	#Top and bottom border
	for horiz in range(BOARD_SIZE+2):
		top_w = tk.Label(master, bg=BORDER_COLOR, height = 4, width = BOX_WIDTH)
		bot_w = tk.Label(master, bg=BORDER_COLOR, width = BOX_WIDTH)
		top_w.grid(row = 0, column = horiz)
		bot_w.grid(row = BOARD_SIZE+1, column = horiz)
	#Left and right border
	for vert in range(BOARD_SIZE):
		left_w = tk.Label(master, bg=BORDER_COLOR, width = BOX_WIDTH)
		right_w = tk.Label(master, bg=BORDER_COLOR, width = BOX_WIDTH)
		left_w.grid(row = vert+1, column = 0)
		right_w.grid(row = vert+1, column = BOARD_SIZE+1)

	#Title	
	title_w = tk.Label(master, text = "SNAKE GAME", font=fontStyle, bg=BORDER_COLOR, fg = "white")
	middle = int(BOARD_SIZE/2)
	title_w.grid(row = 0, column = middle-3, columnspan = 7)
	#Score
	score_w = tk.Label(master, text = "SCORE: " + str(START_SIZE), font=fontStyle, bg=BORDER_COLOR, fg = "white")
	score_w.grid(row = 0, column = 0, columnspan=4)	
	#Quit game
	quit_w = tk.Button(master, text = "Quit", font = fontStyle, bg = BORDER_COLOR, fg = "white", command = master.destroy)
	quit_w.grid(row = 0, column = BOARD_SIZE-1, columnspan = 3)
	#Start Instructions
	start_w = tk.Label(master, text = 'Press Any Key to Continue', font = fontStyle,
                                bg=BORDER_COLOR, fg = "white")
	start_w.grid(row = BOARD_SIZE+1, column = 1, columnspan = BOARD_SIZE)
	#Board Array of Labels and boolean array
	global board_arr, board_val
	board_arr.clear()
	board_val.clear()
	for r in range(BOARD_SIZE):
		new_board = []
		new_val = []
		for c in range(BOARD_SIZE):
			if (r+c)%2 == 0:
				w = tk.Label(master, bg="light slate gray", width = BOX_WIDTH)
			else:
				w = tk.Label(master, bg="cornflower blue", width = BOX_WIDTH)
			w.grid(row = r+1, column = c+1)
			new_board.append(w)
			new_val.append(False)
		board_arr.append(new_board)
		board_val.append(new_val)
	#Draw snake
	global snake_main
	snake_main.clear()
	if START_SIZE >= BOARD_SIZE:
		print("snake cannot be larger than board size")
		sys.exit()
	for foo in range(START_SIZE):
		snake_main.append([ int(BOARD_SIZE/2), int(BOARD_SIZE/2+START_SIZE/2)-foo-1 ])
		if(foo != 0):
			snake_main[foo].append([snake_main[foo-1]])
		#Color board and adjust where snake is
		board_arr[int(BOARD_SIZE/2)][int(BOARD_SIZE/2+START_SIZE/2)-foo-1].config(bg="blue")
		board_val[int(BOARD_SIZE/2)][int(BOARD_SIZE/2+START_SIZE/2)-foo-1] = True
	#Generate Food
	global food
	food.clear()
	rand_num1 = random.randint(BOARD_SIZE)
	rand_num2 = random.randint(BOARD_SIZE)
	while(board_val[rand_num1][rand_num2]):
		rand_num1 = random.randint(BOARD_SIZE)
		rand_num2 = random.randint(BOARD_SIZE)
	food.append(rand_num1)
	food.append(rand_num2)
	board_arr[rand_num1][rand_num2].config(bg = "white")
#Draw the start screen
board_draw()
try:
	master.mainloop()
except KeyboardInterrupt:
	exit()
