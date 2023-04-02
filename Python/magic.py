import random

x = random.randint(2,12)
y = random.randint(2,12)


while True:
    wagwan = int(input((f"What is {x} x {y}? ")))

    if wagwan == (x * y):
        print("Correct!")
        break
    else:
        print("Incorrect - try again.")
