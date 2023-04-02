import random 

def choosing():
    choices = ["rock", "paper", "scissors"]

    computer = random.choice(choices)
    player = None

    while player not in choices:
        player = input("rock, paper, or scissors? ")

    print(f"Computer chose: {computer}")
    print(f"You chose: {player}")

    decisions(player, computer)

    return


def decisions(player, computer):
    if player == computer:
        print("Tie!, go again!")
        choosing()

    elif player == "rock":
        if computer == "paper":
            print("You lose")
        elif computer == "scissors":
            print("You win")

    elif player == "scissors":
        if computer == "rock":
            print("You lose")
        elif computer == "paper":
            print("You win")

    elif player == "paper":
        if computer == "scissors":
            print("You lose")
        elif computer == "rock":
            print("You win")
    ending()
    return

def ending ():
    again = input("Play again? ")
    if again == "yes":
        choosing()
    else:
        print("laters nigga")

choosing()