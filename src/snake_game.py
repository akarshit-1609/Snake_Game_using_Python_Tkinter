import tkinter as tk
import random
import webbrowser

window = tk.Tk()
window_width = 650
window_height = 450
window_background_color = "#686aff"
window.geometry(f"{window_width}x{window_height}+300+20")
window.title("Snake Game")
window.configure(bg=window_background_color)
window.iconbitmap("icons/favicon.ico")   # For Windows only
window.iconphoto(True, tk.PhotoImage(file="icons/icon.png"))

window.update_idletasks()
canvas_width = window_width
canvas_height = window_height
canvas_board_color = "#bcf5ff"

options_field_width = canvas_width
options_field_height = canvas_height

canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg=canvas_board_color, highlightbackground="black")
canvas.pack(side=tk.LEFT)
canvas.place(relx=0, rely=0.5, anchor="w", x=5)

options_field = tk.Frame(window, width=options_field_width, height=options_field_height, bg=window_background_color)
options_field.pack(side=tk.TOP, fill="x")
options_field.place(relx=1.0, rely=0.5, anchor="e", x=-10)
options_field.pack_propagate(False)

box_size = 20
direction = "right"
boxes_when_start = 3
game_speed = 200
game_board_cell = 50
boxes = []
direction_of_each_box = []
box_place = []
score = 0
x = 0
y = 0
out = False

options = ["Start", "Board Size", "Speed", "Score", "About", "Quit"]
board_cells = [10, 25, 50, 75, 100, 200]
speeds = [1000, 500, 200, 100, 50, 20]
speeds_description = ["Too Slow", "Slow", "Normal", "Intermediate", "Fast", "Ultra Fast"]

option_rect = []
option_text = []
stat_records = {}
active_index = 1
default_bg = "#dddddd"
hover_bg = "#ffff00"
active_option_bg = "#ff5555"
score_label_color = "#000000"
current_board_cells = 0
current_speed = 0

for i, j in  enumerate(board_cells):
    if (j == game_board_cell):
        current_board_cells = i
for i, j in  enumerate(speeds):
    if (j == game_speed):
        current_speed = i

def restart_game(e):
    global window_width, window_height, canvas, canvas_board_color, options_field, options_field_width, options_field_height, boxes, box_size, direction_of_each_box, direction, canvas_width, canvas_height, box_place, food, score, score_label, out, option_rect, option_text, stat_records
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    if (window_width<=window_height):
        canvas_width = int(window_width*9/10)
    else :
        canvas_width = int(window_height*9.5/10)
    box_size = canvas_width/game_board_cell
    canvas_height = canvas_width
    options_field_width = window_width - canvas_width - 40
    options_field_height = canvas_height
    if (e != None):
        canvas.config(width=canvas_width, height=canvas_height)
        options_field.config(width=options_field_width, height=options_field_height)
        for i, text in enumerate(options):
            option_rect[i].pack_configure(padx=int(options_field_width-(options_field_width*0.96)), pady=int(options_field_height-(options_field_height*0.99)))
            option_text[i].config(font=("monospace", int(options_field_height/25), "bold"))
            if (text == "Board Size" or text == "Speed"):
                for j in range(1,4):
                    stat_records[text][j].config(font=("monospace", int(options_field_height/30), "bold"))
            elif (text == "Score"):
                stat_records[text][0].pack_configure(padx=int(options_field_width-(options_field_width*0.8)))
                stat_records[text][1].config(font=("monospace", int(options_field_height/30), "bold"))
    score = 0
    out = False
    direction = "right"
    stat_records["Score"][1].config(text=str(score))
    canvas.itemconfig(score_label, text="")
    canvas.delete(food)
    food = canvas.create_rectangle(0,0,0,0, fill="green", outline=canvas_board_color)
    for i in range(len(boxes)):
        canvas.delete(boxes[i])
    box_place.clear()
    direction_of_each_box.clear()
    boxes.clear()
    for j in range(boxes_when_start):
        boxes.append(canvas.create_rectangle(box_size*j,box_size*0,box_size*(j+1),box_size, fill="red", outline=canvas_board_color))
        box_place.append([j,0])
        direction_of_each_box.append("right")

def move_snake():
    global boxes, box_size, direction_of_each_box, direction, box_place, canvas_width, canvas_height, x, y, score, score_label, out
    if (direction != direction_of_each_box[-1]):
        if (
            direction == "left" and direction_of_each_box[-1] == "right" or
            direction == "right" and direction_of_each_box[-1] == "left" or
            direction == "up" and direction_of_each_box[-1] == "down" or
            direction == "down" and direction_of_each_box[-1] == "up"
        ):
            pass
        else:
            direction_of_each_box[-1] = direction
    
    for i in range(len(box_place)):
        if (direction_of_each_box[i] == "right"):
            box_place[i][0] = box_place[i][0] + 1
        elif (direction_of_each_box[i] == "left"):
            box_place[i][0] = box_place[i][0] - 1
        elif (direction_of_each_box[i] == "up"):
            box_place[i][1] = box_place[i][1] - 1
        elif (direction_of_each_box[i] == "down"):
            box_place[i][1] = box_place[i][1] + 1

    if (box_place[-1][0] < 0 or box_place[-1][1] < 0 or box_place[-1][0] > int(canvas_width/box_size)-1 or box_place[-1][1] > int(canvas_height/box_size)-1):
        out = True
    for k in range(len(box_place)-1):
        if (box_place[-1][0] == box_place[k][0] and box_place[-1][1] == box_place[k][1]):
            out = True

    if (box_place[-1][0] == x and box_place[-1][1] == y):
        score = score + 1
        for i in range(len(box_place)):
            if (direction_of_each_box[i] == "right"):
                box_place[i][0] = box_place[i][0] - 1
            elif (direction_of_each_box[i] == "left"):
                box_place[i][0] = box_place[i][0] + 1
            elif (direction_of_each_box[i] == "up"):
                box_place[i][1] = box_place[i][1] + 1
            elif (direction_of_each_box[i] == "down"):
                box_place[i][1] = box_place[i][1] - 1
        boxes.append(canvas.create_rectangle(box_size*x,box_size*y,box_size*(x+1),box_size*(y+1), fill="red", outline=canvas_board_color))
        if (
            direction == "left" and direction_of_each_box[-1] == "right" or
            direction == "right" and direction_of_each_box[-1] == "left" or
            direction == "up" and direction_of_each_box[-1] == "down" or
            direction == "down" and direction_of_each_box[-1] == "up"
        ):
            direction_of_each_box.append(direction_of_each_box[-1])
        else:
            direction_of_each_box.append(direction)
        box_place.append([x,y])
        create_food()
        stat_records["Score"][1].config(text=str(score))
    elif (out == False):
        for i in range(len(boxes)):
            if (direction_of_each_box[i] == "right"):
                canvas.move(boxes[i], box_size, 0)
            elif (direction_of_each_box[i] == "left"):
                canvas.move(boxes[i], -1*box_size, 0)
            elif (direction_of_each_box[i] == "up"):
                canvas.move(boxes[i], 0, -1*box_size)
            elif (direction_of_each_box[i] == "down"):
                canvas.move(boxes[i], 0, box_size)
        for j in range(len(direction_of_each_box)-1):
            if (direction_of_each_box[j] != direction_of_each_box[j+1]):
                direction_of_each_box[j] = direction_of_each_box[j+1]
    if (out == False):
        window.after(game_speed, move_snake)
    else:
        canvas.coords(score_label,canvas_width/2, (canvas_width/50)+30)
        canvas.itemconfig(score_label, text=("Score: " + str(score)), font=("Arial", int((canvas_width/25)+10), "bold"), anchor="center")
        canvas.tag_raise(score_label)
        window.bind("<Up>",on_key_press)
        window.bind("<Down>",on_key_press)
        window.bind("<Left>",on_key_press)
        window.bind("<Right>",on_key_press)
        window.bind("<Return>",on_key_press)

def create_food():
    global food, box_size, box_place, canvas_width, canvas_height, x, y
    x = random.randint(0,int(canvas_width/box_size)-1)
    y = random.randint(0,int(canvas_height/box_size)-1)
    food_match = True
    while food_match:
        food_match = False
        for i in range(len(box_place)):
            if (box_place[i][0] == x and box_place[i][1] == y):
                food_match = True
                x = random.randint(0,int(canvas_width/box_size)-1)
                y = random.randint(0,int(canvas_height/box_size)-1)
    canvas.delete(food)
    food = canvas.create_rectangle(box_size*x,box_size*y,box_size*(x+1),box_size*(y+1), fill="green", outline=canvas_board_color)

for i in range(boxes_when_start):
    boxes.append(canvas.create_rectangle(box_size*i,box_size*0,box_size*(i+1),box_size, fill="red", outline=canvas_board_color))
    direction_of_each_box.append("right")
    box_place.append([i,0])

food = canvas.create_rectangle(0,0,0,0, fill="green", outline=canvas_board_color)
score_label = canvas.create_text(canvas_width/2, box_size, text="", fill=score_label_color, font=("Arial", 20, "bold"), anchor="center")

def deactivate_button():
    global options, active_index
    option_text[active_index].config(bg=hover_bg)
    option_rect[active_index].config(bg=hover_bg)

def on_button_click(index):
    option_text[index].config(bg=active_option_bg)
    option_rect[index].config(bg=active_option_bg)
    if (options[index] == "Start"):
        start(None)
    elif (options[index] == "About"):
        webbrowser.open("https://github.com/akarshit-1609/Snake_Game_using_Python_Tkinter")
    elif (options[index] == "Quit"):
        window.quit()
    window.after(15, deactivate_button)

def update_hover(before_active_index ,index):
    global active_index
    if (index != active_index):
        for i in range(len((options))):
            if (i == before_active_index):
                option_text[i].config(bg=default_bg)
                option_rect[i].config(bg=default_bg)
                if (options[i] == "Board Size" or options[i] == "Speed"):
                    for j in stat_records[options[i]]:
                        j.config(bg=default_bg)
            if (i == index):
                option_text[i].config(bg=hover_bg)
                option_rect[i].config(bg=hover_bg)
                if (options[i] == "Board Size" or options[i] == "Speed"):
                    for j in stat_records[options[i]]:
                        j.config(bg=hover_bg)
    active_index = index

def on_key_press(event):
    global active_index, options, stat_records, current_board_cells, current_speed,game_board_cell, game_speed
    if event.keysym == 'Down':
        new_index = (active_index + 1) % len(options)
        update_hover(active_index, new_index)
    elif event.keysym == 'Up':
        new_index = (active_index - 1) % len(options)
        update_hover(active_index, new_index)
    elif event.keysym == 'Left':
        if (options[active_index] == "Board Size"):
            current_board_cells = (current_board_cells - 1) % len(board_cells)
            stat_records[options[active_index]][2].config(text=str(board_cells[current_board_cells]))
            game_board_cell = board_cells[current_board_cells]
            restart_game(None)
        elif (options[active_index] == "Speed"):
            current_speed = (current_speed - 1) % len(speeds)
            stat_records[options[active_index]][2].config(text=speeds_description[current_speed])
            game_speed = speeds[current_speed]
    elif event.keysym == 'Right':
        if (options[active_index] == "Board Size"):
            current_board_cells = (current_board_cells + 1) % len(board_cells)
            stat_records[options[active_index]][2].config(text=str(board_cells[current_board_cells]))
            game_board_cell = board_cells[current_board_cells]
            restart_game(None)
        elif (options[active_index] == "Speed"):
            current_speed = (current_speed + 1) % len(speeds)
            stat_records[options[active_index]][2].config(text=speeds_description[current_speed])
            game_speed = speeds[current_speed]
    elif event.keysym == 'Return':
        on_button_click(active_index)

def on_enter(event, idx):
    update_hover(active_index, idx)

def on_leave(event, idx):
    update_hover(0,active_index)
   
for i, option in enumerate(options):
    btn = tk.Frame(options_field, bg=default_bg)
    btn.pack(fill="x", padx=10, pady=10)
    lbtn = tk.Label(btn, text=option, bg=default_bg, fg="black", font=("monospace", 15, "bold"))
    lbtn.pack()
    if (option == "Board Size" or option == "Speed"):
        stat_box = tk.Frame(btn, bg=default_bg)
        stat_box.pack(fill="x", padx=10, pady=2)
        stat_box.grid_columnconfigure(0, weight=1)
        stat_box.grid_columnconfigure(1, weight=1)
        stat_box.grid_columnconfigure(2, weight=1)
        stat0 = tk.Label(stat_box, text="<", bg=default_bg, fg="black", font=("monospace", 10, "bold"))
        stat0.grid(row=0, column=0, sticky="w")
        if (option == "Board Size"):
            stat1 = tk.Label(stat_box, text=str(board_cells[current_board_cells]), bg=default_bg, fg="black", font=("monospace", 10, "bold"))
            stat1.grid(row=0, column=1, sticky="nsew")
        elif (option == "Speed"):
            stat1 = tk.Label(stat_box, text=str(speeds_description[current_speed]), bg=default_bg, fg="black", font=("monospace", 10, "bold"))
            stat1.grid(row=0, column=1, sticky="nsew")
        stat2 = tk.Label(stat_box, text=">", bg=default_bg, fg="black", font=("monospace", 10, "bold"))
        stat2.grid(row=0, column=2, sticky="e")
        stat_records[option] = [stat_box, stat0, stat1, stat2]
    elif (option == "Score"):
        stat_box = tk.Frame(btn, bg="white")
        stat_box.pack(fill="x", padx=40, pady=2)
        stat0 = tk.Label(stat_box, text="0", bg="white", fg="black", font=("monospace", 10, "bold"))
        stat0.pack()
        stat_records[option] = [stat_box, stat0]
    btn.bind("<Button-1>", lambda e, idx=i: on_button_click(idx))
    lbtn.bind("<Button-1>", lambda e, idx=i: on_button_click(idx))
    btn.bind("<Enter>", lambda e, idx=i: on_enter(e, idx))
    btn.bind("<Leave>", lambda e, idx=i: on_leave(e, idx))
    option_rect.append(btn)
    option_text.append(lbtn)

window.bind("<Configure>", restart_game)

def start(e):
    window.bind("<Left>",left)
    window.bind("<Right>",right)
    window.bind("<Up>",up)
    window.bind("<Down>",down)
    window.unbind("<Return>")
    restart_game(None)
    move_snake()
    create_food()

def resign(e):
    global out
    out = True

def left(e):
    global direction
    direction = "left"
def right(e):
    global direction
    direction = "right"
def up(e):
    global direction
    direction = "up"
def down(e):
    global direction
    direction = "down"
    
sizedata = True
def winsize(e):
    global sizedata
    if (sizedata):
        window.attributes("-fullscreen",True)
        sizedata = False
    else:
        window.attributes("-fullscreen",False)
        sizedata = True
window.bind("<F11>",winsize)

window.bind("<Escape>",resign)
window.bind("<Up>",on_key_press)
window.bind("<Down>",on_key_press)
window.bind("<Left>",on_key_press)
window.bind("<Right>",on_key_press)
window.bind("<Return>",on_key_press)

update_hover(0,0)

window.mainloop()