from src.data_store import data_store
from src.error import InputError
from src.auth_and_user_profile_helper import is_valid_email, is_valid_password_length, is_valid_name_length, is_email_registered, create_handle, create_auth_user_id, encrypt_password, create_token, create_session_id 
from src.helpers import decode_jwt
import string    
import random
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def auth_login_v2(email, password):
    '''
    finds user info in data store from given email

    Arguements:
        email (string) - must match a previously registerd email
        password (string) - must match password associated with given email in data_store

    Exceptions:
        Input Error - Occurs when:
                        - email has not been previously registered
                        - password does not match that stored in data_store for the given email

    Return Value:
        Returns auth_user_id as a dictionary containing u_id 
        '''
    if(is_email_registered(email) == False):
        raise InputError ("Email is not yet registered")

    #iterate through data store looking for user id that matches the email
    user = data_store.get()['users']
    i = 0
    while email != user[i]["email"]:
        i = i + 1 
    
    #compare password to password found in data store
    if(encrypt_password(password) != user[i]['password']):
        raise InputError ("Incorrect password")
    else:
        session_id = create_session_id()
        token = create_token(user[i]['u_id'], session_id )
        user[i]['session_id'].append(session_id)
        return {'token': token, 'auth_user_id': user[i]['u_id']}


def auth_register_v2(email, password, name_first, name_last):
    '''
    takes new users info and creates dictionary in list users in the data_store for them containing their email, password, name_first, name_last, handle and   
    user_id

    Arguements:
        email (string) - must be unique and of the correct format
        password (string) - must be at least six characters long
        name_first (string) -  must be between one and fifty characters long inclusive
        name_last (string) - must be between one and fifty characters long inclusive

    Exceptions:
        Input Error - Occurs when:
                        - email has been previously registered
                        - email is of invalid format
                        - password is less than six characters long
                        - name_first is not between one and fifty characters long inclusive
                        - name_last is not between one and fifty characters long inclusive

    Return Value:
        Returns auth_user_id as a dictionary containing u_id 
        
    '''
    #check all possible errors
    if(is_valid_email(email) == False):
        raise InputError ("Email is invalid")
    if(is_email_registered(email) == True):
        raise InputError ("Email is already in use")
    if(is_valid_password_length(password) == False):
        raise InputError ("Password is too short")
    if(is_valid_name_length(name_first) == False):
        raise InputError ("Name is either too long or too short")
    if(is_valid_name_length(name_last) == False):
        raise InputError ("Name is either too long or too short") 
    if(name_first == 'Removed' and name_last == 'user'):
        raise InputError ("Cannot register as Removed user")

    password_encrypted = encrypt_password(password)
    
    #create u_id    
    u_id = create_auth_user_id()

    #create permissions
    if u_id == 6000000:
        permission = 1
    else:
        permission = 2

    #create session id 
    session_id = create_session_id()

    #token creation
    token = create_token(u_id, session_id)

    #create new dictionary for new user
    users = data_store.get()['users']
    
    new_user = {
        'u_id': u_id,
        'email': email,
        'password': password_encrypted,
        'name_first': name_first,
        'name_last': name_last, 
        'handle_str': create_handle(name_first, name_last),
        'session_id': [session_id],
        'permission_id': permission,
        'reset_code': '',  
        'notifications': [],  
    }
    print(f"int auth: session id: {session_id}")
    users.append(new_user)

    return  {'token': token, 'auth_user_id': u_id}

def auth_logout_v1(token):
    '''
    if given a valid token will invalidate session id associated with that token

    Arguements:
        token - a jwt string with u_id and session_id as payload

    Exceptions:
        Access Error - when given an invalid token

    Return Value:
        {}
        
    '''
    payload = decode_jwt(token)
    user = data_store.get()['users']
    i = 0
    while (payload['u_id'] != user[i]['u_id'] and i < len(user)):
        i = i + 1
    
    user[i]['session_id'].remove(payload['session_id'])
    
    return {}

def auth_passwordreset_request_v1(email):
    '''
    if given a valid email address will send an email to that address with a code that allows the user to reset their password
    also logs the user out of all active sessions

    Arguements:
        email (string) - must match a previously registerd email

    Exceptions:
        None for security reasons

    Return Value:
        {}
        
    '''
    reset_code = ''
    if (is_email_registered(email) == True):
        #locate user in data_store
        user = data_store.get()['users']
        i = 0
        while(email != user[i]['email'] and i < len(user)):
            i = i + 1

        #remove session id, i.e. log them out
        user[i]['session_id'] = '' 

        #create reset code 
        S = 6  
        reset_code = ''.join(random.choices(string.ascii_letters + string.digits, k = S))
        user[i]['reset_code'] = reset_code   

        

    return reset_code
        
def auth_passwordreset_reset_v1(reset_code, new_password):
    '''
    if given a reset code and password will change the user associated with the reset code's password.

    Arguements:
        reset_code (string) - must match a reset_code associated with a user in datastore
        new_password (string) - must be at least six characters long

    Exceptions:
        Input error - reset_code is not a valid reset code
                    - password entered is less than 6 characters long

    Return Value:
        {}
        
    '''
    user = data_store.get()['users']
    i = 0
    while i < len(user) and  reset_code != user[i]['reset_code']:
        i += 1

    if (i == len(user)):
        raise InputError ("Invalid reset code.")
    else:
        if (is_valid_password_length(new_password) == False):
            raise InputError ("Password is too short.")
        else:
            new_encrypted_password = encrypt_password(new_password)
            user[i]['password'] = new_encrypted_password
            user[i]['reset_code'] = ''

    
    return 

    

    

    
    
    
