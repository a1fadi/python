def praccy1(letters, n): 
    letters = str(letters)
    new_string = []
    for i in range(letters):
        new_letter = int(letters[i]) + n
        new_string.append(str(new_letter))
    return new_string

if __name__ == "__main__":
    print(praccy1(("asda", 3))
