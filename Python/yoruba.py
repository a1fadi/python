import random

Yoruba = {
        "greetings" : {
            'What is happening?': 'kilo n sele',
            'How are things?': 'ba wo ni',
            'Are you good?': 'sho wa dada',
            'Good morning': 'e ka ro',
            'Good afternoon': 'e ka san',
            'Good evening': 'e ka le',
            'Welcoming to your home': 'e ku le',
            'Good night': 'o da ro',
            'Good bye': 'o da bo',
            'Its been a while': 'o tojo met',
            'What is your name': 'ki lo ru ko e',
            'My name is Fadi': 'druko mi ni Fadi',
            'Where did you come from?': 'ni bo lo ti wa',
            'I come from': 'mo wa la ti',
            'Can I see you again?': 'se mo le tun ri e si',

        },
        "verbs" : {

        },

        "numbers" : {
            '0': 'odo',
            '1': 'okan',
            '2': 'eji',
            '3': 'eta',
            '4': 'erin',
            '5': 'arun',
            '6': 'efa',
            '7': 'eje',
            '8': 'ejo',
            '9': 'esan',
            '10': 'ewa'

        },

        "days" : {
            'Monday': 'ojo aiku',
            'Tuesday': 'ojo aje',
            'Wednesday': 'ojo isegun',
            'Thursday': 'ojo ojoru',
            'Friday': 'ojo ojobo',
            'Saturday': 'ojo eti',
            'Sunday': 'ojo abameta'
        },  

        "months" : {
            'January': 'osu sere',
            'February': 'osu erele',
            'March': 'osu erena',
            'April': 'osu igbe',
            'May': 'osu ebibi',
            'June': 'osu okudu',
            'July': 'osu agemo',
            'August': 'osu ogun',
            'September': 'osu owere',
            'October': 'osu owara',
            'November': 'osu belu',
            'December': 'osu ope',

        },

        "vocab" : {
            'Talk Slower': 'rora ma soro',
            'I am sorry': 'ma binu',
            'I didnt hear you': 'mi o gbo inkan to so',
            'How do they say': 'bawo no se man so ni yoruba',
            'I am 3 years old': 'omo odun meta ni mi'
        }
    }

def topic():
    topica = input("What topic would you like to be tested on?: ")
    topica = topica.lower()
    if topica not in Yoruba.keys():
        print("Topic not available, please pick another topic")
        topic()
    else:
        return topica

def tester(topica):
    score = 0
    word = random.choice(list(Yoruba[topica]))

    answer = input(f'{word} in Yoruba: ')
    answer = answer.lower()

    if (Yoruba[topica][word] == answer):
        print("Well Done\n")
        score = 1
    else:
        if answer in Yoruba[topica].values():
            print("That actually means: ", list(Yoruba[topica].keys())
        [list(Yoruba[topica].values()).index(answer)])
            print(f'Correct answer was {Yoruba[topica][word]}\n')
        else:
            print("Incorrect")
            print(f'Correct answer was {Yoruba[topica][word]}\n')
    return score

if __name__ == "__main__":
    loop, count, score = 0, 0, 0
    answer = input("Short, Medium or Long test? ")
    answer = answer.lower()
    topica = topic()
    print("\n\n\nNew Test \n\n\n")
    if answer == 'short':
        loop = 5
    elif answer == "medium":
        loop = 10
    else: 
        loop = 25

    while (count < loop):
        score = score + tester(topica)
        count = count + 1

    print(f'You got {score}/{loop}')

