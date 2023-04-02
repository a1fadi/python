def new_game():
    guesses = []
    correct_guesses = 0
    question_num = 1

    for key in questions:
        print("------------")
        print(key)
        #for i in options[question_num -1]:
        print(options[question_num - 1])
        guess = input("Enter A, B, C or D: ")
        guess = guess.upper()
        guesses.append(guess)
        correct_guesses += check_answer(questions.get(key), guess)
        question_num += 1
    
    display_score(correct_guesses, guesses)


def check_answer(answer, guess):
    if answer == guess:
        print("Correct")
        return 1
    else:
        print("Wrong")
        return 0

def display_score(correct_guesses, guesses):
    print("-------")
    print("RESULTS")
    print("Answers: ", end = '')

    for i in questions:
        print(questions.get(i), end = ' ')
    print()

    print ("Guesses:", end = ' ')
    for i in guesses:
        print (i, end = ' ')
    print()

    score = int(correct_guesses/len(questions)*100)
    print(f"Your score is {score}%")
    answer = int(input("Would you like to play again? (enter 1 if yes, 0 if no): "))
    play_again(answer)

def play_again(answer):
    if answer == 1:
        new_game()
    else:
        print("Fuck you")

questions = {
    "Who is the best footballer in the world": "A",
    "Who is the best basketballer in the world": "B",
    "Who is the best F1 driver in the world": "A"
}

options = [
    ["A. Messi", "B. Ronaldo", "C. Hernandez"],
["A. Fadi Alhatu", "B. Lebron James", "C. Yao Ming"],
["A. Lewis Hamilton", "B. Max Verstappen", "C. Sebastien Vettel"]
]

new_game()