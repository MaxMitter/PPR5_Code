# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 09:05:51 2021

@author: maxmi
"""
import turtle

t = turtle.Turtle()

t.forward(50)
t.left(90)

t.forward(50)
t.left(90)

t.forward(50)
t.left(90)

t.forward(50)
t.left(90)


wn = turtle.Screen()
from sys import platform
if platform=='win32':
    wn.exitonclick()
    
turtle.mainloop()