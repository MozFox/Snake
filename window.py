from tkinter import *
import random
import itertools as it

WIDTH = 600
HEIGHT = 600
SEG_SIZE = 20
IN_GAME = True
RAINBOW_COLORS = it.cycle(["#FF0000", "#FF4500", "#FFFF00", "#008000", "#00BFFF", "#0000FF", "#800080"])


class SegmentSnake:

    def __init__(self, x, y):
        self.segment_snake = canvas.create_rectangle(x, y, x + SEG_SIZE, y + SEG_SIZE, fill=next(RAINBOW_COLORS))


class Snake:

    def __init__(self, segments):
        self.segments = segments
        self.moving = {"Right": (1, 0), "Left": (-1, 0), "Up": (0, -1), "Down": (0, 1)}
        self.vector = self.moving["Right"]

    def move(self):
        for index in range(len(self.segments) - 1):
            segment = self.segments[index].segment_snake
            x1, y1, x2, y2 = canvas.coords(self.segments[index + 1].segment_snake)
            canvas.coords(segment, x1, y1, x2, y2)

        x1, y1, x2, y2 = canvas.coords(self.segments[-2].segment_snake)
        canvas.coords(self.segments[-1].segment_snake,
                      x1 + self.vector[0] * SEG_SIZE,
                      y1 + self.vector[1] * SEG_SIZE,
                      x2 + self.vector[0] * SEG_SIZE,
                      y2 + self.vector[1] * SEG_SIZE)

    def change_direction(self, event):
        if event.keysym in self.moving:
            self.vector = self.moving[event.keysym]

    def add_segment(self):

        last_segment = canvas.coords(self.segments[0].segment_snake)

        x = last_segment[2] - SEG_SIZE
        y = last_segment[3] - SEG_SIZE

        self.segments.insert(0, SegmentSnake(x, y))

    def reset_snake(self):
        for square in self.segments:
            canvas.delete(square.segment_snake)


class Score:

    def __init__(self, score):
        self.score = score

    def add_score(self):
        self.score += 1


def app_score():
    return Score(0)


def apple_for_snake():
    global apple
    pos_x = SEG_SIZE * random.randint(1, (WIDTH - SEG_SIZE) / SEG_SIZE)
    pos_y = SEG_SIZE * random.randint(1, (HEIGHT - SEG_SIZE) / SEG_SIZE)
    apple = canvas.create_oval(pos_x, pos_y, pos_x + SEG_SIZE, pos_y + SEG_SIZE, fill="green")


def create_segment():
    segments = [SegmentSnake(SEG_SIZE, SEG_SIZE),
                SegmentSnake(SEG_SIZE * 2, SEG_SIZE),
                SegmentSnake(SEG_SIZE * 3, SEG_SIZE)]
    return Snake(segments)

def set_state(item, state):
    canvas.itemconfigure(item, state=state)

def clicked():
    global IN_GAME, game_over_text
    canvas.delete(apple)
    IN_GAME = True
    canvas.itemconfigure(game_over_text, state='hidden')
    s.reset_snake()
    start_game()


def start_game():
    global s, score
    apple_for_snake()
    s = create_segment()
    score = app_score()
    canvas.bind("<KeyPress>", s.change_direction)
    main()


def main():
    global IN_GAME
    if IN_GAME:
        s.move()
        head_snake_coords = canvas.coords(s.segments[-1].segment_snake)
        x1, y1, x2, y2 = head_snake_coords
        if x2 > WIDTH or x1 < 0 or y1 < 0 or y2 > HEIGHT:
            IN_GAME = False
        elif head_snake_coords == canvas.coords(apple):
            s.add_segment()
            canvas.delete(apple)
            apple_for_snake()
            score.add_score()
        else:
            for index in range(len(s.segments) - 1):
                if head_snake_coords == canvas.coords(s.segments[index].segment_snake):
                    IN_GAME = False
        window.after(200, main)
        lbl_2 = Label(window,
                      text="Score: {}".format(score.score),
                      font=("Arial Bold", 20, "bold"),
                      bg="#D2691E",
                      fg="#000000")
        lbl_2.place(x=10, y=605)
    else:
        canvas.itemconfigure(game_over_text, state="normal")
        btn = Button(window, text="New game", command=clicked)
        btn.place(x=500, y=615)


window = Tk()
window.title("Snake")
window.geometry("600x650")
window["bg"] = "#D2691E"
window.resizable(0, 0)
canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg='#F4A460')
game_over_text = canvas.create_text(WIDTH/2, HEIGHT/2, text="Game over", font=("Arial Bold", 20, "bold"), state="hidden")
canvas.pack()
canvas.focus_set()
canvas.grid()
start_game()

window.mainloop()
