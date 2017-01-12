from Tkinter import *
import random

square_side = 20
square_color = "red"
canvas_height = 30
canvas_width = 20
score = 0

def init(height, width):
    score = 0
    squares = []
    for i in range(height):
        row = []
        for j in range(width):
            row.append(False)
        squares.append(row)
    return squares

squares = init(canvas_height,canvas_width)



class Square:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = None

    def fall(self, dy):
        self.y += dy

    def translate(self, dx):
        self.x += dx

    def paint(self, canvas, side, color):
        self.image = canvas.create_rectangle(self.x, self.y, self.x + side, self.y + side, fill=color)


class Pattern:

    def __init__(self, is_random = True, side = square_side, center = canvas_width * square_side/2):
        self.four_square = set()
        self.x = center
        self.y = -1 * side
        if is_random:
            r = random.randrange(7)
        else:
            r = 0
        if r == 0:
            self.four_square.add(Square(center - side, -2 * side))
            self.four_square.add(Square(center, -2 * side))
            self.four_square.add(Square(center - side, -1 * side))
            self.four_square.add(Square(center, -1 * side))
        elif r == 1:

            self.four_square.add(Square(center - side, -1 * side))
            self.four_square.add(Square(center, -2 * side))
            self.four_square.add(Square(center, -1 * side))
            self.four_square.add(Square(center + side, -1 * side))
        elif r == 2:

            self.four_square.add(Square(center - side, -2 * side))
            self.four_square.add(Square(center, -2 * side))
            self.four_square.add(Square(center, -1 * side))
            self.four_square.add(Square(center + side, -1 * side))
        elif r == 3:

            self.four_square.add(Square(center - side, -1 * side))
            self.four_square.add(Square(center, -2 * side))
            self.four_square.add(Square(center, -1 * side))
            self.four_square.add(Square(center + side, -2 * side))
        elif r == 4:

            self.four_square.add(Square(center - 2 * side, -1 * side))
            self.four_square.add(Square(center - side, -1 * side))
            self.four_square.add(Square(center, -1 * side))
            self.four_square.add(Square(center, -2 * side))
        elif r == 5:

            self.four_square.add(Square(center - side, -2 * side))
            self.four_square.add(Square(center - side, -1 * side))
            self.four_square.add(Square(center, -1 * side))
            self.four_square.add(Square(center + side, -1 * side))
        elif r == 6:

            self.four_square.add(Square(center - 2 * side, -1 * side))
            self.four_square.add(Square(center - side, -1 * side))
            self.four_square.add(Square(center, -1 * side))
            self.four_square.add(Square(center + side, -1 * side))

    def fall(self, dy, squares = squares, side = square_side, height = canvas_height):
        can_fall = True
        for square in self.four_square:
            if int(square.y / side) + 1 >= height or (int(square.y / side) + 1 >= 0 and squares[int(square.y / side) + 1][int(square.x / side)]):
                can_fall = False
        if can_fall:
            for square in self.four_square:
                square.fall(dy)
            self.y += dy
        return can_fall

    def fall_to_botton(self, squares = squares, side = square_side, height = canvas_height):
        distance = canvas_height * side
        for square in self.four_square:
            j = square.y
            while not (int(j / side) + 1 >= height or squares[int(j / side) + 1][int(square.x / side)]):
                j += side
            d = j - square.y
            if d < distance:
                distance = d
        for square in self.four_square:
            square.fall(distance)
        self.y += distance


    def translate(self, dx, squares = squares, side = square_side, width = canvas_width, height = canvas_height):
        can_translate = True
        if dx > 0:
            for square in self.four_square:
                if int(square.x / side) + 1 >=  width or squares[int(square.y / side)][int(square.x / side) + 1] \
                        or (int(square.y / side) + 1 < height and squares[int(square.y / side) + 1][int(square.x / side) + 1]):
                    can_translate = False
        if dx < 0:
            for square in self.four_square:
                if int(square.x / side) - 1 <  0 or squares[int(square.y / side)][int(square.x / side) - 1] \
                        or (int(square.y / side) + 1 < height and squares[int(square.y / side) + 1][int(square.x / side) - 1]):
                    can_translate = False
        if can_translate:
            for square in self.four_square:
                square.translate(dx)
            self.x += dx
        return can_translate


    def can_rotate_clockwise(self, squares, side, width, height):
        for square in self.four_square:
            i = square.x
            j = square.y
            i, j = self.y - j + self.x - side, i - self.x + self.y
            if (i < 0 or int(i / side) + 1 > width or int(j / side) + 1 > height or
                    squares[int(j / side)][int(i / side)] or squares[int(j / side) + 1][int(i / side)]):
                return False
        return True

    def rotate_clockwise(self, squares = squares, side = square_side, width = canvas_width, height = canvas_height):
        if self.can_rotate_clockwise(squares, side, width, height):
            for square in self.four_square:
                i = square.x
                j = square.y
                square.x, square.y = self.y - j + self.x - side, i - self.x + self.y

    def paint(self, canvas, side = square_side, color = square_color):
        for square in self.four_square:
            square.paint(canvas,side, color)
        # canvas.create_oval(self.x - 3, self.y - 3, self.x + 3, self.y + 3, fill="blue")

    def destroy(self, canvas):
        for square in self.four_square:
            canvas.delete(square.image)

    def repaint(self, canvas, side = square_side, color = square_color):
        self.destroy(canvas)
        self.paint(canvas,side,color)

def paint(canvas, score, squares = squares, side = square_side, color = square_color):
    canvas.create_text(canvas.winfo_width() / 2 + 150, canvas.winfo_height() / 2 - 290,
                              text="score: " + str(score))
    for j in range(len(squares)):
        for i in range(len(squares[j])):
            if squares[j][i]:
                x = i * side
                y = j * side
                canvas.create_rectangle(x, y, x + side, y + side, fill=color)


def can_eliminate (y, squares = squares):
    for i in squares[y]:
        if not i:
            return False
    return True

def eliminate (squares = squares):
    row = []
    for i in range(len(squares[len(squares) - 1])):
        row.append(False)
    down = 0
    dictionary = {}
    for j in range(len(squares) - 1,-1,-1):
        dictionary[j] = down
        if can_eliminate(j):
            for i in range(len(squares[j])):
                squares[j][i] = False
            down += 1
            global score
            score += 1
    for j in range(len(squares) - 1, -1, -1):
        if dictionary[j] > 0:
            squares[j], squares[j + dictionary[j]] = squares[j + dictionary[j]], squares[j]

def reach_end(canvas, side = square_side, squares = squares):
    global pattern
    for square in pattern.four_square:
        squares[int(square.y / side)][int(square.x / side)] = True

    eliminate(squares)
    pattern = Pattern()
    canvas.delete(ALL)
    paint(canvas, score)


def fall():
    if pattern.fall(5):
        pattern.repaint(canvas)
    else:
        reach_end(canvas)
    tk.after(50, fall)

def key_action(event):
    if event.keycode == 8189699:
        pattern.translate(square_side)
        pattern.repaint(canvas)
    elif event.keycode == 8124162:
        pattern.translate(-square_side)
        pattern.repaint(canvas)
    elif event.keycode == 8255233:
        pattern.fall_to_botton()
    elif event.keycode == 8320768:
        pattern.rotate_clockwise()
        pattern.repaint(canvas)

pattern = Pattern()

tk = Tk()
tk.title("Tetris")
canvas = Canvas(tk, width=square_side * canvas_width,
                height=square_side * canvas_height)
pattern.paint(canvas)
canvas.focus_set()
canvas.bind("<Key>", key_action)
canvas.pack()
fall()
paint(canvas, score)
tk.mainloop()


