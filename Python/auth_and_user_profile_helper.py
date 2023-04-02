import re
from src.data_store import data_store, SECRET, TOTAL_NUMBER_OF_SESSIONS
import hashlib
import jwt
from src.error import InputError, AccessError



#check email is actually an email
def is_valid_email(email):
    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

#checks password is at least six characters
def is_valid_password_length(password):
    if(len(password) < 6):
        return False
    else:
        return True

#checks that the length of a name is between 1 and 50 characters inclusive
def is_valid_name_length(name):
    if(len(name) >= 1 and len(name) <= 50):
        return True
    else:
        return False

#checks if email is registered, used by both login and register functions
def is_email_registered(email):
    user = data_store.get()['users']
    
    #iterates through data store looking for an id with matching email, 
    #breaks if matching email is found or counter excedes list length
    i = 0
    while(i < len(data_store.get()['users']) and email != user[i]["email"]):
       i = i + 1
    
    #checks if previous while loop broke from matching email or from exceeding list length
    if (i < len(data_store.get()['users'])):
        return True
    else:
        return False

#creates user handle
def create_handle(name_first, name_last):

    #remove non alpha-numeric characters
    name_first = re.sub(r'[^a-zA-Z0-9]', '', name_first)
    name_last = re.sub(r'[^a-zA-Z0-9]', '', name_last)

    #cast to lower case
    name_first = name_first.lower()
    name_last = name_last.lower()

    #combine first and last name into one string
    handle = name_first + name_last

    #truncate string to a maximum of 20 characters
    handle = handle[:20]

    #iterate through list and check there are no matching handles,
    #if there is a matching handle an integer is added to the end of the string
    #starting at zero and increasing by one
    handle_check = handle
    other_user = data_store.get()['users']
    
    j = 0
    i = 0
    while(j < len(data_store.get()['users'])):
        if(handle_check == other_user[j]['handle_str']):
            handle_check = handle
            handle_check = handle_check + str(i) 
            i = i + 1
            j = 0
        j = j + 1
        
    
    handle = handle_check

    return handle

#creates user id
def create_auth_user_id():
    i = len(data_store.get()['users'])
    if i < 2**31 - 6000000:
        #user id starts at 6000000 and increases by one for each additional user
        auth_user_id = i + 6000000
        return auth_user_id
    else:
        raise AccessError

#encrypts password
def encrypt_password(password):
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed_password

#creates jwt token
def create_token(u_id, session_id):
    payload_data = {
        'u_id': u_id,
        'session_id': session_id,
    }

    token = jwt.encode(payload_data, SECRET, algorithm = "HS256")
    return token

#create session id
def create_session_id():
    global TOTAL_NUMBER_OF_SESSIONS
    if TOTAL_NUMBER_OF_SESSIONS < 2**31: 
        TOTAL_NUMBER_OF_SESSIONS += 1
    else:
        TOTAL_NUMBER_OF_SESSIONS = 1
    return TOTAL_NUMBER_OF_SESSIONS

#returns users position in list when given a user id 
def locate_user_with_u_id(u_id):
    user = data_store.get()['users']
    i = 0
    while i <  len(user) and user[i]['u_id'] != u_id:
        i = i + 1
    if i == len(user):
        raise InputError
    else:
        return i
