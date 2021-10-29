import turtle

tur = turtle.Turtle()

def drawKochLine(t, len):
    if len < 5:
        t.forward(len)
        return
    seg = len / 3
    #t.forward(seg)
    drawKochLine(t, seg)
    t.right(60)
    #t.forward(seg)
    drawKochLine(t, seg)
    t.left(120)
    #t.forward(seg)
    drawKochLine(t, seg)
    t.right(60)
    #t.forward(seg)
    drawKochLine(t, seg)


def drawSnowflake(t, initialLenght = 90):
    drawKochLine(t, initialLenght)
    t.left(120)
    drawKochLine(t, initialLenght)
    t.left(120)
    drawKochLine(t, initialLenght)
    t.left(120)


tur.speed(100)
tur.hideturtle()
drawSnowflake(tur, 180)
#drawKochLine(tur, 90)

wn = turtle.Screen()
from sys import platform

if platform == 'win32':
    wn.exitonclick()

turtle.mainloop()
