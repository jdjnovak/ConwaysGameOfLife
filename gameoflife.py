import os
import time
import random
from pynput.keyboard import Listener

GAMESTATE='PAUSED'

FRAMERATE=100
WIDTH=20
HEIGHT=15

BOARD=[['.' for i in range(WIDTH)] for j in range(HEIGHT)]

def print_board():
    for row in BOARD:
        ROW=''
        for col in row:
            ROW += str(col)
        print(ROW)

def generate_init_board():
    # TODO: Add a more random starting method
    # This is the weird one so I'll just 
    # start with a pattern
    # FIRST: doing this pattern twice, slightly offset
    # 001000
    # 010010
    # 001100
    MID_HEIGHT=int(HEIGHT/2)
    MID_WIDTH=int(WIDTH/2)
    BOARD[MID_HEIGHT][2+MID_WIDTH] = '+'
    BOARD[MID_HEIGHT-1][2+MID_WIDTH+1] = '+'
    BOARD[MID_HEIGHT+1][2+MID_WIDTH+1] = '+'
    BOARD[MID_HEIGHT+1][2+MID_WIDTH+2] = '+'
    BOARD[MID_HEIGHT][2+MID_WIDTH+3] = '+'

    BOARD[1-MID_HEIGHT][2-MID_WIDTH] = '+'
    BOARD[1-MID_HEIGHT-1][2-MID_WIDTH+1] = '+'
    BOARD[1-MID_HEIGHT+1][2-MID_WIDTH+1] = '+'
    BOARD[1-MID_HEIGHT+1][2-MID_WIDTH+2] = '+'
    BOARD[1-MID_HEIGHT][2-MID_WIDTH+3] = '+'

# Returns a count of the neighbours
# of a specific node in the board in
# a tuple object:
#   (zeros,ones), e.g., (1,2)
#  N0 <- starting on N
#  11
# Done in counter-clockwise fashion
def count_neighbours(row,col):
    # NOTE: smaller number rows are higher
    #       on the board and smaller number
    #       cols are more left on the board
    NUM_ZERO=0
    NUM_ONE=0
    # Check UP
    if row > 0:
        if BOARD[row-1][col] == '+':
            NUM_ONE += 1
        else:
            NUM_ZERO += 1

    # Check UP RIGHT
    if row > 0 and col < WIDTH-1:
        if BOARD[row-1][col+1] == '+':
            NUM_ONE += 1
        else:
            NUM_ZERO += 1

    # Check RIGHT
    if col < WIDTH-1:
        if BOARD[row][col+1] == '+':
            NUM_ONE += 1
        else:
            NUM_ZERO += 1

    # Check DOWN RIGHT
    if row < HEIGHT-1 and col < WIDTH-1:
        if BOARD[row+1][col+1] == '+':
            NUM_ONE += 1
        else:
            NUM_ZERO += 1
    
    # Check DOWN
    if row < HEIGHT-1:
        if BOARD[row+1][col] == '+':
            NUM_ONE += 1
        else:
            NUM_ZERO += 1

    # Check DOWN LEFT
    if row < HEIGHT-1 and col > 0:
        if BOARD[row+1][col-1] == '+':
            NUM_ONE += 1
        else:
            NUM_ZERO += 1

    # Check LEFT
    if col > 0:
        if BOARD[row][col-1] == '+':
            NUM_ONE += 1
        else:
            NUM_ZERO += 1

    # Check UP LEFT
    if row > 0 and col > 0:
        if BOARD[row-1][col-1] == '+':
            NUM_ONE += 1
        else:
            NUM_ZERO += 1

    # Return the tuple
    return (NUM_ZERO,NUM_ONE)

def step():
    for row in range(HEIGHT):
        for col in range(WIDTH):
            ZEROS,ONES = count_neighbours(row,col)
            if BOARD[row][col] == '.':
                if ONES == 3:
                    BOARD[row][col] = '+'
            elif ONES < 2 or ONES > 3:
                BOARD[row][col] = '.'

# Get time in ms
def current_time():
    return round(time.time() * 1000)

# Clear screen
def clear_screen():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')

#### Pynput stuff
def on_press(key):
    global GAMESTATE
    try:
        if key.char == 'p':
            if GAMESTATE=='RUNNING':
                GAMESTATE='PAUSED'
            else:
                GAMESTATE='RUNNING'
    except AttributeError:
        pass

# Do nothing
def on_release(key):
    pass

# Game loop over specified frame rate
def loop():
    global GAMESTATE
    listener = Listener(on_press=on_press, on_release=on_release)
    listener.start()
    LAST_FRAME_CHANGE=current_time()
    GAMESTATE = 'RUNNING'
    clear_screen()
    print_board()
    while True:
        if current_time() >= LAST_FRAME_CHANGE + FRAMERATE and GAMESTATE == 'RUNNING':
            clear_screen()
            step()
            print_board()
            LAST_FRAME_CHANGE = current_time()
        elif current_time() >= LAST_FRAME_CHANGE + FRAMERATE and GAMESTATE == 'PAUSED':
            clear_screen()
            print_board()
            print("PAUSED")
            LAST_FRAME_CHANGE = current_time()

if __name__ == "__main__":
    generate_init_board()
    loop()
