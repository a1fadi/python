class Rectangle:

    def __init__(self, canvas, x, y, diameter, xVelocity, yVelocity, color):
        self.canvas = canvas
        self.image = canvas.create_rectangle(x,y,diameter, diameter, fill = color)
        self.xVelocity = xVelocity 
        self.yVelocity = yVelocity 
    
    def move(self): 
        coordinates = self.canvas.coords(self.image)
        print(coordinates)
        if (coordinates[2] >= (self.canvas.winfo_width()) or coordinates[0]<0):
            self.xVelocity = -self.xVelocity
        if (coordinates[3] >= (self.canvas.winfo_height()) or coordinates[1]<0):
            self.yVelocity = -self.yVelocity
        self.canvas.move(self.image, self.xVelocity, self.yVelocity)
    
class Oval:

    def __init__(self, canvas, x, y, diameter, xVelocity, yVelocity, color):
        self.canvas = canvas
        self.image = canvas.create_oval(x,y,diameter, diameter, fill = color)
        self.xVelocity = xVelocity 
        self.yVelocity = yVelocity 
    
    def move(self): 
        coordinates = self.canvas.coords(self.image)
        print(coordinates)
        if (coordinates[2] >= (self.canvas.winfo_width()) or coordinates[0]<0):
            self.xVelocity = -self.xVelocity
        if (coordinates[3] >= (self.canvas.winfo_height()) or coordinates[1]<0):
            self.yVelocity = -self.yVelocity
        self.canvas.move(self.image, self.xVelocity, self.yVelocity)
    
class Text:

    def __init__(self, canvas, x, y, xVelocity, yVelocity):
        self.canvas = canvas
        self.text = canvas.create_text(x, y, text='A wonderful story', anchor='nw', font='TkMenuFont', fill='red')
        self.xVelocity = xVelocity 
        self.yVelocity = yVelocity 


    def move(self): 
        coordinates = self.canvas.coords(self.text)
        print(coordinates)
        if (coordinates[1] >= (self.canvas.winfo_width()) or coordinates[0]<0):
            self.xVelocity = -self.xVelocity
        if (coordinates[0] >= (self.canvas.winfo_height()) or coordinates[1]<0):
             self.yVelocity = -self.yVelocity
        self.canvas.move(self.text, self.xVelocity, self.yVelocity)
    
   
