def ball_count():
    balls = int(input("How many balls would you like?: "))
    return balls 

def shapes_color(balls): 
    shapes = [{
        "shape":" ",
        "color":" ",
        "size": " ",
        "xspeed":0, 
        "yspeed":0,
    }]*balls 
    i = 0
    while (i < balls):
        print(f"BALL {i+1}")
        print("------")
        shapes[i]["shape"] = input("Enter a shape, Rectangle or Oval: ")
        shapes[i]["color"] = input("Enter a color: ")
        shapes[i]["size"] = input("Enter a size (small, medium, big): ")

        if shapes[i]["size"] == "small":
            shapes[i]["size"] = 10 
        elif shapes[i]["size"] == "medium":
            shapes[i]["size"] = 50
        elif shapes[i]["size"] == "big":
            shapes[i]["size"] = 200

        answer = input("Enter '1' if you would like it to move, '0' if not: ")
        if answer == '1':
            shapes[i]["xspeed"] = int(input("Enter sideward speed (e.g. 1) for ball: "))
            shapes[i]["yspeed"] = int(input("Enter downward speed for ball: "))
        i += 1 
    return shapes

def canvas_size():
    dimensions = {
        "width":" ",
        "height":" ",
    }
    dimensions['width'] = input("Enter a canvas width: ")
    dimensions['height'] = input("Enter a canvas height: ")
    return dimensions
