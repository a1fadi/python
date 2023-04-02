from tkinter import *
from ball import *
import time
from user_input import * 

balls = ball_count()
shapes = shapes_color(balls)
canvas = canvas_size()

window = Tk()

WIDTH = canvas["width"]
HEIGHT = canvas["height"]

canvas = Canvas(window, width=WIDTH, height=HEIGHT)
canvas.pack()

#items = [''] #*balls 

i = 0

while i < balls:
    print (shapes[i]["size"])
    if shapes[i]["shape"] == "Rectangle" or shapes[i]["shape"] == "rectangle":
         rectangle = Rectangle(canvas, 0, 0, shapes[i]["size"], shapes[i]["xspeed"], shapes[i]["yspeed"], shapes[i]["color"])
         while True:
            square.move()
            window.update() 
            time.sleep(0.01)

    elif shapes[i]["shape"] == "Oval" or shapes[i]["shape"] == "oval":
         oval = Oval(canvas, 0, 0, shapes[i]["size"], shapes[i]["xspeed"], shapes[i]["yspeed"], shapes[i]["color"])
         while True:
            oval.move()
            window.update() 
            time.sleep(0.01)

    i += 1
   

while True:  

    # oval.move()
    # window.update() 
    # time.sleep(0.01) 
   
    # rectangle.move()
    # window.update() 
    # time.sleep(0.01)

    # bowling_ball.move()
    # window.update() 
    # time.sleep(0.01)

    # text.move()
    # window.update() 
    # time.sleep(0.01)

    window.mainloop()
