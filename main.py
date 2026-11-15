import tkinter as tk
from random import choice

WIDTH = 700
HEIGHT = 400

root = tk.Tk()
root.title("Ping-Pong!")


canvas = tk.Canvas(width=WIDTH,
                   height=HEIGHT,
                   bg="#1a192c",
                   highlightthickness=0)
canvas.pack()

score = [0, 0]
positions = [HEIGHT/2]*2
ball_tail = []
ball_pos = [WIDTH/2, HEIGHT/2]
ball_v = [0, 0]
BALL_R = 15
BALL_COLOR = "#00756F"
PADDING_PADS = 15
PAD_LEN = 40

COLOR_X = {"RED": PADDING_PADS, "BLUE": WIDTH-PADDING_PADS}
COLOR_HEX = {"RED": "#850021", "BLUE": "#1800A1"}

MAX_V = 16
move_me = 0
keys_now = {"Up": False, "Down": False}


def get_move():
    global move_me
    if keys_now["Up"] == keys_now["Down"]:
        move_me = 0
    elif keys_now["Up"]:
        move_me = -8
    elif keys_now["Down"]:
        move_me = 8


def press(e):
    if e.keysym in ["Up", "Down"]:
        keys_now[e.keysym] = True
        get_move()


def release(e):
    if e.keysym in ["Up", "Down"]:
        keys_now[e.keysym] = False
        get_move()


root.bind("<KeyPress>", press)
root.bind("<KeyRelease>", release)


def label():
    canvas.create_text(WIDTH//2-30, 30,
                       text=score[0],
                       fill=COLOR_HEX["RED"],
                       font=("Arial", 36, "bold"))
    canvas.create_text(WIDTH//2+30, 30,
                       text=score[1],
                       fill=COLOR_HEX["BLUE"],
                       font=("Arial", 36, "bold"))


def pad(y, color):
    canvas.create_line(
        COLOR_X[color], y-PAD_LEN,
        COLOR_X[color], y+PAD_LEN,
        fill=COLOR_HEX[color],
        width=10,
        capstyle="round"
    )


def start():
    global ball_pos, positions, ball_tail
    ball_tail = []
    ball_pos = [WIDTH/2, HEIGHT/2]
    positions = [HEIGHT/2]*2
    ball_v[0] = choice([-8, 8])
    ball_v[1] = choice([-4, 4])


def ball(x, y, r):
    canvas.create_oval(x+r, y+r, x-r, y-r,
                       fill=BALL_COLOR)


def is_hit(pad_y):
    return abs(ball_pos[1] - pad_y) < PAD_LEN + BALL_R


def draw():
    canvas.delete('all')
    tail_r = BALL_R - 2
    for i in ball_tail:
        ball(*i, BALL_R-tail_r)
        tail_r = max(1, tail_r-1)
    canvas.create_line(WIDTH//2, 0, WIDTH//2, HEIGHT,
                       dash=(20, 25),
                       width=4,
                       fill="#242347")
    pad(positions[1], "BLUE")
    pad(positions[0], "RED")
    label()
    ball(*ball_pos, BALL_R)


def step():
    ball_tail.append((ball_pos[0], ball_pos[1]))
    del ball_tail[:-13]
    print(len(ball_tail))
    positions[0] = min(
        max(positions[0] + move_me, 50),
        HEIGHT-(PAD_LEN+10))
    positions[1] = min(
        max(50, positions[1] + max(-5, min(5, ball_pos[1]-positions[1]))),
        HEIGHT-(PAD_LEN+10))

    ball_pos[0] += ball_v[0]
    ball_pos[1] += ball_v[1]

    if ball_pos[0] <= PADDING_PADS+BALL_R:
        if is_hit(positions[0]) and ball_v[0] < 0:
            ball_v[0] = min(ball_v[0] * -1.06, MAX_V)
            ball_v[1] = (ball_pos[1] - positions[0]) / 6
    if ball_pos[0] >= WIDTH-PADDING_PADS-BALL_R:
        if is_hit(positions[1]) and ball_v[0] > 0:
            ball_v[0] = min(ball_v[0] * -1.06, MAX_V)
            ball_v[1] = (ball_pos[1] - positions[1]) / 6

    if ball_pos[1] > HEIGHT-BALL_R or ball_pos[1] < BALL_R:
        ball_v[1] = -ball_v[1]

    if ball_pos[0] < 0:
        score[1] += 1
        start()
    if ball_pos[0] > WIDTH:
        score[0] += 1
        start()

    draw()
    root.after(10, step)


start()
step()

root.mainloop()
