import turtle
import matplotlib.colors as col
from HW1 import basic_library


def visualizeWalk(t, walk, stepSize = 15):
    t.color(col.hex2color("#ff0000"))
    rad = 5
    t.hideturtle()
    t.speed(2)
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
walk = basic_library.generate_walk(4)
visualizeWalk(tur, walk, 50)

wn = turtle.Screen()
from sys import platform

if platform == 'win32':
    wn.exitonclick()

turtle.mainloop()