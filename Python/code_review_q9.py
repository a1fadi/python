from helpers import password_score
import random
import hashlib

usernames = []
passwords = []

def get_random_number(x, y):
    # Gets a random number between two numbers
    return random.randint(x, y)

def add_user(username, password):
    '''
    Adds a user to our data store.
    If the username matches an existing username, it adds numbers to avoid having the same username

    Returns 1 the password not strong enough
    Returns 0 in success case, because I just took COMP1511 and coding in Python is just like C right?
    '''

    if password_score(password) < 5:
        return 1

    for x in range(len(usernames)):
        if usernames[x] == username:
            username += str(get_random_number(1, 10))

            # Loop through again to check we haven't changed it to the same username
            for x in range(len(usernames)):
                if usernames[x] == username:
                    username += str(get_random_number(1, 10))

    # Hash the password
    hashedPassword = hashlib.sha256(password.encode()).hexdigest()

    usernames.append(username)
    passwords.append(hashedPassword)

    return 0

def does_user_exist(username):
    # Checks if a username exists in the list of usernames
    return len(list(filter(usernames, lambda u_name: u_name == username))) > 0
