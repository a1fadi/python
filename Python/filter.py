def filter_string(inp):
    new_string = ""
    if str.isdigit(inp) == True: 
        raise ValueError
    for i in range(len(inp)):
        if ord(inp[i]) == 33 or ord(inp[i]) == 34 or ord(inp[i]) == 63 or ord(inp[i]) == 58 or ord(inp[i]) == 39 or ord(inp[i]) == 44 or ord(inp[i]) == 46:
            new_string += inp[i]

    return new_string
