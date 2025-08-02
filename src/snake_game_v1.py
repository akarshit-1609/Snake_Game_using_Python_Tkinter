import tkinter as tk
import random

window = tk.Tk()
window_width = 650
window_height = 450
window.geometry(f"{window_width}x{window_height}+300+20")
window.title("Snake Game")
window.iconbitmap("icons/favicon.ico") # For windows only
window.iconphoto(True, tk.PhotoImage(file="icons/icon.png"))

window.update_idletasks()
canvas_width = window_width
canvas_height = window_height

canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="white", highlightbackground="black")
canvas.pack(side=tk.LEFT)
canvas.place(relx=0, rely=0.5, anchor="w", x=5)

box_size = 20
direction = "right"
boxes_when_start = 3
game_speed = 100 # milliseconds
game_board_size = 50
boxes = []
direction_of_each_box = []
box_place = []
score = 0
x = 0
y = 0
out = False
def restart_game(e):
    global window_width, window_height, canvas, options, options_width, options_height, boxes, box_size, direction_of_each_box, direction, canvas_width, canvas_height, box_place, food, score, score_output, out
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    if (window_width<=window_height):
        canvas_width = int(window_width*9/10)
    else :
        canvas_width = int(window_height*9.5/10)
    box_size = canvas_width/game_board_size
    canvas_height = canvas_width
    canvas.config(width=canvas_width, height=canvas_height)
    score = 0
    out = False
    direction = "right"
    canvas.itemconfig(score_output, text="")
    canvas.delete(food)
    food = canvas.create_rectangle(0,0,0,0, fill="green", outline="white")
    for i in range(len(boxes)):
        canvas.delete(boxes[i])
    box_place.clear()
    direction_of_each_box.clear()
    boxes.clear()
    for j in range(boxes_when_start):
        boxes.append(canvas.create_rectangle(box_size*j,box_size*0,box_size*(j+1),box_size, fill="red", outline="white"))
        box_place.append([j,0])
        direction_of_each_box.append("right")

def move_snake():
    global boxes, box_size, direction_of_each_box, direction, box_place, canvas_width, canvas_height, x, y, score, score_output, out
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
        boxes.append(canvas.create_rectangle(box_size*x,box_size*y,box_size*(x+1),box_size*(y+1), fill="red", outline="white"))
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
        canvas.coords(score_output,canvas_width/2, (canvas_width/50)+30)
        canvas.itemconfig(score_output, text=("Score: " + str(score)), fill="blue", font=("Arial", int((canvas_width/25)+10), "bold"), anchor="center")
        canvas.tag_raise(score_output)

def create_food():
    global food, box_size, canvas_width, canvas_height, x, y
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
    food = canvas.create_rectangle(box_size*x,box_size*y,box_size*(x+1),box_size*(y+1), fill="green", outline="white")


    
for i in range(boxes_when_start):
    boxes.append(canvas.create_rectangle(box_size*i,box_size*0,box_size*(i+1),box_size, fill="red", outline="white"))
    direction_of_each_box.append("right")
    box_place.append([i,0])

food = canvas.create_rectangle(0,0,0,0, fill="green", outline="white")
score_output = canvas.create_text(canvas_width/2, box_size, text="", fill="blue", font=("Arial", 20, "bold"), anchor="center")


window.bind("<Configure>", restart_game)

def start(e):
    restart_game(None)
    move_snake()
    create_food()

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

window.bind("<F1>",start)
window.bind("<Left>",left)
window.bind("<Right>",right)
window.bind("<Up>",up)
window.bind("<Down>",down)

window.mainloop()