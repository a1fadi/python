from src.data_store import data_store
from src.auth_and_user_profile_helper import is_valid_email, is_valid_name_length, is_email_registered, locate_user_with_u_id
from src.helpers import decode_jwt
from src.error import InputError
import re

def user_profile_v1(token, u_id):
    '''
    For a valid user, returns information about their user_id, email, first name, last name, and handle

    Arguements:
        token (string) - must be a valid jwt
        u_id (int) - must match a u_id in data store

    Exceptions:
        Input Error - Occurs when:
                        - u_id does not refer to a valid user

    Return Value:
        user info as a dictionary 
        '''
    token = str(token)
    u_id = int(u_id)
    
    decode_jwt(token)
    i = locate_user_with_u_id(u_id)
    user = data_store.get()['users']
    user_return = { 'user': {
        'u_id': user[i]['u_id'],
        'email': user[i]['email'],
        'name_first': user[i]['name_first'],
        'name_last': user[i]['name_last'],
        'handle_str': user[i]['handle_str']
    }}

    return user_return

def user_profile_setname_v1(token, name_first, name_last):
    '''
    Update the authorised user's first and last name

    Arguements:
        token (string) - must be a valid jwt
        name_first (string) - must be between 1 and 50 characters
        name_last (string) - must be between 1 and 50 characters

    Exceptions:
        Input Error - Occurs when:
                        - length of names is not between 1 and 50 characters inclusive

    Return Value:
        empty dictionary
    '''

    jwt = decode_jwt(token)
    if is_valid_name_length(name_first) == False:
        raise InputError
    if is_valid_name_length(name_last) == False:
        raise InputError
    if name_first == 'Removed' and name_last == 'user':
        raise InputError

    u_id = jwt['u_id']
    i = locate_user_with_u_id(u_id)
    user = data_store.get()['users']
    user[i]['name_first'] = name_first
    user[i]['name_last'] = name_last
    return {}

def user_profile_setemail_v1(token, email):
    '''
    Update the authorised user's email address

    Arguements:
        token (string) - must be a valid jwt
        email (string) - must be of valid format and not in use

    Exceptions:
        Input Error - Occurs when:
                        - email is of invalid format
                        - email address is already being used by anothr user

    Return Value:
        empty dictionary
    '''
    jwt = decode_jwt(token)
    if is_valid_email(email) == False:
        raise InputError
    if is_email_registered(email) == True:
        raise InputError
    
    u_id = jwt['u_id']
    i = locate_user_with_u_id(u_id)
    user = data_store.get()['users']
    user[i]['email'] = email

    return {}

def user_profile_sethandle_v1(token, handle_str):
    '''
    Update the authorised user's handle (i.e. display name)

    Arguements:
        token (string) - must be a valid jwt
        handle_str (string)

    Exceptions:
        Input Error - Occurs when:
                        - handle_str is not between 3 and 20 characters inclusive
                        - handle_str contains non alphanumeric characters
                        - handle_str is being used by another user

    Return Value:
        empty dictionary
    '''

    user = data_store.get()['users']
    jwt = decode_jwt(token)

    re.sub(r'[^a-zA-Z0-9]', '', handle_str)

    i = 0
    while (i < len(user) and user[i]['handle_str'] != handle_str):
        i = i + 1
    
    u_id = jwt['u_id']
    j = locate_user_with_u_id(u_id)
    user[j]['handle_str'] = handle_str

    return {}

