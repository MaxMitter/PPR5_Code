import turtle
import matplotlib.pyplot as plt
import matplotlib.colors as col
from HW1 import basic_library

def get_random_color(index, name='hsv'):
    return plt.cm.get_cmap(name, index)


def visualizeWalk(t, walk, color, stepSize = 15, startPos = (0, 0)):
    t.pensize(5)
    t.color(col.to_hex(color))
    rad = 8
    t.hideturtle()
    t.penup()
    t.setpos(startPos)
    t.pendown()
    #t.speed(2)
    print(walk)
    for w in walk:
        if w == "N":
            t.setheading(90)
        elif w == "E":
            t.setheading(0)
        elif w == "S":
            t.setheading(270)
        elif w == "W":
            t.setheading(180)

        t.forward(stepSize)
    t.penup()
    t.back(rad)
    t.right(90)
    t.pendown()
    t.begin_fill()
    t.circle(radius=rad)
    t.end_fill()


tur = turtle.Turtle()
walk_dict = basic_library.monte_carlo_walk_analysis(5, 10)

cmap = get_random_color(10)

for i in range(10):
    startPos = (-6 * i, -6 * i)
    walk = basic_library.generate_walk(5)
    visualizeWalk(tur, walk, cmap(i), 50, startPos)

wn = turtle.Screen()
from sys import platform

if platform == 'win32':
    wn.exitonclick()

turtle.mainloop()