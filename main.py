import pygame as pg
import sys
import time
from pygame.locals import *
from backend import * 
from qiskit_aer import AerSimulator

width = 400
height = 400
extraheight = 200
textboxheight = 80
fps = 15
running_time = pg.time.Clock()

MEASURE_COLOR = (43, 43, 43)
colors = [(255, 255, 255), (236, 224, 209), (145, 116, 103), (166, 197, 224), (170, 195, 147)]

# Board structure: [state_string, color_tuple]
board = [[None, None] for _ in range(9)]

color = 1
choice_1 = -1
choice_2 = -1
twoq_gate = ""
steps = 0
gates = []
game_over = False  # Track if the game has ended

pg.init()
screen = pg.display.set_mode((width, height + extraheight + textboxheight), 0, 32)
pg.display.set_caption("Quantum Tic Tac Toe")

# --- IMAGE LOADING ---
try:
    initiating_window = pg.image.load("plus.png")
    x_img = pg.image.load("x.png")
    o_img = pg.image.load("o.png")
    ox_img = pg.image.load("ox.png")
    xo_img = pg.image.load("xo.png")
    plus_img = pg.image.load("plus.png")
    plus2o_img = pg.image.load("plus2o.png")
    empty_img = pg.image.load("empty.png")
    plus2x_img = pg.image.load("plus2x.png")
    teleport_img = pg.image.load("teleport.png")
    cnot_img = pg.image.load("cnot.png")
    measure_img = pg.image.load("measure.png")
    swap_img = pg.image.load("swap.png")

    # Rescale images
    initiating_window = pg.transform.scale(initiating_window, (width, height + extraheight + textboxheight))
    x_img = pg.transform.scale(x_img, (90, 90))
    o_img = pg.transform.scale(o_img, (90, 90))
    ox_img = pg.transform.scale(ox_img, (90, 90))
    xo_img = pg.transform.scale(xo_img, (90, 90))
    plus_img = pg.transform.scale(plus_img, (90, 90))
    empty_img = pg.transform.scale(empty_img, (90, 90))
except FileNotFoundError as e:
    print(f"Error loading images: {e}")
    sys.exit()

def game_initiating_window():
    screen.blit(initiating_window, (0, 0))
    pg.display.update()
    time.sleep(0.1)
    screen.fill((255, 255, 255))
    pg.display.update()

    # Draw grid lines
    pg.draw.line(screen, (0, 0, 0), (width / 3, 0), (width / 3, height), 7)
    pg.draw.line(screen, (0, 0, 0), (width / 3 * 2, 0), (width / 3 * 2, height), 7)
    pg.draw.line(screen, (0, 0, 0), (0, height / 3), (width, height / 3), 7)
    pg.draw.line(screen, (0, 0, 0), (0, height / 3 * 2), (width, height / 3 * 2), 7)
    pg.draw.line(screen, (0, 0, 0), (0, height), (width, height), 9)
    
    # Control panel lines
    pg.draw.line(screen, (0, 0, 0), (width/3, height), (width/3, height+extraheight), 7)
    pg.draw.line(screen, (0, 0, 0), (width/3*2, height), (width/3*2, height+extraheight), 7)
    pg.draw.line(screen, (0, 0, 0), (0, height+extraheight/2), (width, height+extraheight/2), 7)
    pg.draw.line(screen, (0, 0, 0), (0, height+extraheight), (width, height+extraheight), 9)

    pg.display.update()
    time.sleep(0.1)

    # Initialize board
    for i in range(9):
        board[i] = ["ox", (255, 255, 255)]
        draw_img(i, "ox", (255, 255, 255))
    
    update_message("Welcome to Quantum Tic Tac Toe")

def draw_img(index, img, color):
    global board
    x_coord = index % 3
    y_coord = index // 3
    posx = x_coord * width/3 + 20
    posy = y_coord * height/3 + 20
    
    commit_img = empty_img
    if img == "x":
        commit_img = x_img
    elif img == "o":
        commit_img = o_img
    elif img == "ox":
        if color == (255, 255, 255):
            commit_img = plus_img
        else:
            commit_img = ox_img
    elif img == "xo":
        commit_img = xo_img
    elif img == "":
        commit_img = empty_img

    pg.draw.rect(screen, color, pg.Rect(posx-15, posy-15, 125, 125))
    screen.blit(commit_img, (posx, posy))
    pg.display.update()

def draw_button(gate, hovered=False):
    btn_img = None
    btn_coords = (0, 0)

    if gate == "plus2o":
        btn_img = plus2o_img
        btn_coords = (0, height)
    elif gate == "plus2x":
        btn_img = plus2x_img
        btn_coords = (width/3, height)
    elif gate == "cnot":
        btn_img = cnot_img
        btn_coords = (width/3*2, height)
    elif gate == "teleport":
        btn_img = teleport_img
        btn_coords = (0, height+extraheight/2)
    elif gate == "measure":
        btn_img = measure_img
        btn_coords = (width/3, height+extraheight/2)
    elif gate == "swap":
        btn_img = swap_img
        btn_coords = (width/3*2, height+extraheight/2)
    
    btn_bg_color = (200, 200, 0) if hovered else (150, 150, 0)
    
    if btn_img:
        pg.draw.rect(screen, btn_bg_color, pg.Rect(btn_coords[0]+4, btn_coords[1]+4, 125, 90))
        screen.blit(btn_img, (btn_coords[0], btn_coords[1]))
    pg.display.update()

def clear():
    coords = [(0, height), (width/3, height), (width/3*2, height), 
              (0, height+extraheight/2), (width/3, height+extraheight/2), (width/3*2, height+extraheight/2)]
    for btn_coords in coords:
        pg.draw.rect(screen, (255, 255, 255), pg.Rect(btn_coords[0]+4, btn_coords[1]+4, 125, 90))
    pg.display.update()

# --- MOVES ---

def plus2o(i):
    global gates, steps
    if board[i][0] == "ox" and board[i][1] == (255, 255, 255):
        board[i][0] = "o"
        draw_img(i, board[i][0], board[i][1])
        steps += 1
        gates += [("hadamard", i)]

def plus2x(i):
    global gates, steps
    if board[i][0] == "ox" and board[i][1] == (255, 255, 255):
        board[i][0] = "x"
        draw_img(i, board[i][0], board[i][1])
        steps += 1
        gates += [("sigmaz", i), ("hadamard", i)]

def teleport(i, j):
    global gates, steps
    if board[i][0] != "" and board[j][0] != "":
        # Darken entangled pairs if they exist elsewhere
        for idx, b in enumerate(board):
            if idx != i and idx != j and b[1] == board[j][1] and board[j][1] != (255, 255, 255):
                board[idx] = ["", MEASURE_COLOR]
                draw_img(idx, board[idx][0], board[idx][1])
        
        board[j] = board[i][:]
        board[i] = ["", MEASURE_COLOR]
        draw_img(i, board[i][0], board[i][1])
        draw_img(j, board[j][0], board[j][1])
        steps += 1
        gates += [("teleport", i, j)]

def measure(i):
    global gates
    if board[i][0] != "":
        # 1. Mark Entangled Pairs as "Collapsed" (Dark Grey)
        if board[i][1] != (255, 255, 255):
            for idx, b in enumerate(board):
                if idx != i and b[1] == board[i][1]:
                    # Mark partner as measured/collapsed
                    board[idx] = ["", MEASURE_COLOR] 
        
        # 2. Mark clicked square as "Collapsed"
        board[i] = ["", MEASURE_COLOR]

        # 3. Run simulation immediately
        # We need to know the state of the WHOLE board now
        temp_gates = gates + [("measure", i)]
        print(f"Measuring square {i}...")
        results = send(temp_gates) # returns list [0, 1, 0, 1...] for all 9 squares
        
        # 4. Update Visuals for ALL collapsed squares
        # This fixes the "delay" - if A forces B, B reveals immediately
        for k in range(9):
            if board[k][1] == MEASURE_COLOR:
                # Update the text (X or O) based on simulation result
                if results[k] == 0:
                    board[k][0] = "o"
                    draw_img(k, "o", MEASURE_COLOR)
                else:
                    board[k][0] = "x"
                    draw_img(k, "x", MEASURE_COLOR)
        
        # 5. Lock in the result for the clicked square
        measured_val = results[i]
        gates += [("force", i, measured_val)]
        
        # 6. Check for winner immediately
        check_winner(results)

def swap(i, j):
    global gates
    if board[i][0] != "" and board[j][0] != "":
        board[i], board[j] = board[j][:], board[i][:]
        gates += [("swap", i, j)]
        draw_img(i, board[i][0], board[i][1])
        draw_img(j, board[j][0], board[j][1])

def flip_(state):
    if state == "o": return "x"
    elif state == "x": return "o"
    return state

def cnot(j, i):
    global color, gates, steps
    if board[i][0] != "" and board[j][0] != "":
        if (len(board[j][0]) == 1): # Check if target is definite state
            if board[i][0] == "x":
                board[j][0] = flip_(board[j][0])
            else:
                if board[j][0] == "x":
                    board[j][0] = flip_(board[i][0])
                else:
                    board[j][0] = board[i][0]

                if board[i][1] == (255, 255, 255):
                    if color < len(colors):
                        board[i][1] = colors[color]
                        board[j][1] = colors[color]
                        color += 1
                    draw_img(i, board[i][0], board[i][1])
                else:
                    board[j][1] = board[i][1][:]
            
            draw_img(j, board[j][0], board[j][1])
            steps += 1
            gates += [("cnot", i, j)]

def user_click():
    global choice_1, twoq_gate, choice_2
    x, y = pg.mouse.get_pos()
    
    col, row = None, None
    
    if y < height:
        if x < width/3: col = 1
        elif x < width/3*2: col = 2
        elif x < width: col = 3
        
        if y < height/3: row = 1
        elif y < height/3*2: row = 2
        elif y < height: row = 3
        
        if col and row:
            i = (col-1) + (row-1)*3
            
            if not twoq_gate:
                choice_1 = i
                if board[i] == ["ox", (255, 255, 255)]:
                    draw_button("plus2o")
                    draw_button("plus2x")
                    draw_button("teleport")
                    draw_button("measure")
                    draw_button("swap")
                elif board[i][0] in ["o", "x"]:
                    draw_button("cnot")
                    draw_button("teleport")
                    draw_button("measure")
                    draw_button("swap")
                elif board[i][0] != "":
                    draw_button("teleport")
                    draw_button("measure")
                    draw_button("swap")
                    
            elif choice_1 >= 0:
                choice_2 = i
                if twoq_gate == "teleport":
                    teleport(choice_1, choice_2)
                elif twoq_gate == "cnot":
                    cnot(choice_1, choice_2)
                elif twoq_gate == "swap":
                    swap(choice_1, choice_2)
                
                clear()
                choice_1 = -1
                choice_2 = -1
                twoq_gate = ""

    elif choice_1 >= 0:
        if y < height + extraheight/2:
            if x < width/3:
                plus2o(choice_1)
                clear(); choice_1 = -1
            elif x < width/3*2:
                plus2x(choice_1)
                clear(); choice_1 = -1
            else:
                twoq_gate = "cnot"
                print("Selected CNOT")
        else:
            if x < width/3:
                twoq_gate = "teleport"
                print("Selected Teleport")
            elif x < width/3*2:
                measure(choice_1)
                clear(); choice_1 = -1
            else:
                twoq_gate = "swap"
                print("Selected Swap")

def send(gates): 
    backend = AerSimulator()
    qc = instruction(gates, backend)
    result = qc.simulate(1) 
    record = get_the_final_state(result)
    return record

def update_message(message):
    global message_text
    message_text = message
    font = pg.font.SysFont('Arial', 20)
    text = font.render(message_text, True, (255, 105, 205))
    pg.draw.rect(screen, (255, 255, 255), pg.Rect(0, height+extraheight, width, textboxheight))
    text_rect = text.get_rect(center=(width/2, height+extraheight+textboxheight/2))
    screen.blit(text, text_rect)
    pg.display.update()

def draw_status(winner):
    global game_over
    if winner != "draw":
        mes = winner.upper() + " wins!"
    else:
        mes = "Game Draw!"
    update_message(mes)
    game_over = True # Stop the game

def check_winner(res):
    # res is list of 0s and 1s representing state of all 9 qubits
    # But wait! We only want to check squares that are definitely collapsed (MEASURED)
    # We can check board state for color. 
    # Or simplified: Check the 'res' assuming current collapse is final.
    
    cnts = [0, 0] # [O count, X count]
    
    # Check lines
    lines = [
        (0,1,2), (3,4,5), (6,7,8), # Rows
        (0,3,6), (1,4,7), (2,5,8), # Cols
        (0,4,8), (2,4,6)           # Diags
    ]
    
    winning_symbol = None
    
    for l in lines:
        a, b, c = l
        # Check if these 3 squares are MEASURED (collapsed) and match
        # We check board[i][1] == MEASURE_COLOR to confirm they are "real" Xs or Os
        if (board[a][1] == MEASURE_COLOR and 
            board[b][1] == MEASURE_COLOR and 
            board[c][1] == MEASURE_COLOR):
            
            if res[a] == res[b] == res[c]:
                if res[a] == 0: winning_symbol = "o"
                else: winning_symbol = "x"
                break

    if winning_symbol:
        draw_status(winning_symbol)

def check_done():
    cnt = 0
    for b in board:
        if b[0] == "":
            cnt += 1
    return cnt == 9

# --- Main Loop ---
game_initiating_window()
run = True

while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            pg.quit()
            sys.exit()
        
        # Only check done at the very end if no winner found yet
        elif check_done() and not game_over:
            draw_status("draw")
            
        elif event.type == pg.MOUSEBUTTONDOWN and not game_over:
            user_click()
    
    pg.display.update()
    running_time.tick(fps)