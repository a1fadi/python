from lib2to3.refactor import FixerError
from src.data_store import data_store
from src.error import AccessError, InputError
from src.helpers import decode_jwt, is_valid_dm

'''
Functions that deal with the dms that are created between users and perform various user operations pertaining to these dms
This includes showing the details of a dm, leaving a dm and removing a dm completely
'''


def dm_details_v1(token, dm_id):
    '''
    A function that prints the details of a given dm
    Parameters: authorised user's token, dm_id
    Return: A dictionary of the dm's details of name and members {}
    '''
    token = str(token)
    dm_id = int(dm_id)
    
    token_info = decode_jwt(token)

    info = data_store.get()
    required_dm, valid_dm = is_valid_dm(info, dm_id)
    user_in_group = False

    '''
    Following are the tests to make sure the correct errors are raised
    '''

    if valid_dm == False:
        raise InputError("Please Enter a Valid DM Id")

    # If the user is an owner member return true
    for member in required_dm['owner_members']:
        if member['u_id'] == token_info['u_id']:
            user_in_group = True
    
    # If the user is an ordinary member return true
    for member in required_dm['other_members']:
        if member['u_id'] == token_info['u_id']:
            user_in_group = True

    # If the user does not exist in the dm return an Access Error
    if user_in_group == False:
        raise AccessError("User is not a Member of this DM Group")
    
    details = required_dm.copy()  
    # Makes a copy of the dm information
    details.pop('dm_id')  
    # Removes the unnecessary fields of dm_id and messages
    details.pop('messages')
    details['members'] = []
    for item in details['owner_members']:
        details['members'].append(item)
    for item in details['other_members']:
        details['members'].append(item)
    # Makes sure all members contains correct information
    details.pop('other_members') # Removes the other and owner members fields
    details.pop('owner_members')

    return details


def dm_remove_v1(token, dm_id):
    '''
    removes a dm completely from the data store and deletes everything inside it

    Arguements:
        token (string) - must be a valid token
        dm_id (integer) - must be a valid dm id (i.e channel exists)

    Exceptions:
        Input Error - Occurs when:
                        - token is invalid
                        - dm id doesn't exist 
                        
        Access Error - Occurs when:
                        - dm_id is valid and the authorised user is not the original DM creator
                        - dm_id is valid and the authorised user is no longer in the DM

    Return Value:
        Returns empty dictionary
    '''
    info = data_store.get()
    user_info = data_store.get()['users']
    token_info = decode_jwt(token)
    dm_info = data_store.get()['dms']
    
    #Check if valid dm 
    required_dm, valid_dm = is_valid_dm(info, dm_id)

    #check if session is valid
    for user in user_info:
        if token_info['u_id'] == user['u_id'] and token_info['session_id'] not in user['session_id']:
            raise AccessError("Invalid Session")

    #checking valid dm 
    if valid_dm == False:
        raise InputError("Please Enter a Valid DM Id")
    
    #check to see user is an owner 
    user_is_owner = False
    for member in required_dm['owner_members']:
        if member['u_id'] == token_info['u_id']:
            user_is_owner = True
        
    if user_is_owner == False:
        raise AccessError

    #remove all users 
    for dm in dm_info:
        user_list = dm['owner_members']
        i = 0
        for i in range(len(user_list)):
            del user_list[i]

    for dm in dm_info:
        user_list = dm['other_members']
        i = 0
        for i in range(len(user_list)):
            del user_list[i]

    #remove the dm from the list of dms
    for dm in dm_info:
        if dm['dm_id'] == dm_id: 
            dm_info.remove(dm)


def dm_leave_v1(token, dm_id):
    '''
    removes a user from a dms member lists (either owner or other)

    Arguements:
        token (string) - must be a valid token
        dm_id (integer) - must be a valid dm id (i.e channel exists)

    Exceptions:
        Input Error - Occurs when:
                        - token is invalid
                        - dm id doesn't exist 
                        
        Access Error - Occurs when:
                        - user isnt already a member 

    Return Value:
        Returns empty dictionary
    '''
    
    #getting the data 
    user_info = data_store.get()['users']
    token_info = decode_jwt(token)
    dm_info = data_store.get()['dms']

    #seeing if a session is valid 
    for user in user_info:
        if token_info['u_id'] == user['u_id'] and token_info['session_id'] not in user['session_id']:
            raise AccessError("Invalid Session")

    #checking if dm_id is valid 
    dm_exists = False
    for id in dm_info:
        if id['dm_id'] == dm_id:
            dm_exists = True 

    if dm_exists == False:
        raise InputError
    
    #making sure user provided exists as either an owner or member
    user_exists = False
    for dm in dm_info:
        for user in dm['owner_members']: 
            if user['u_id'] == token_info['u_id']: 
                user_exists = True
    
    for dm in dm_info:
        for user in dm['other_members']:
            if user['u_id'] == token_info['u_id']:
                user_exists = True
        
    if user_exists == False:
        raise AccessError


    #if everything has passed then find the dm_id
    for dm in dm_info:
        if dm['dm_id'] == dm_id: 
            dm_leave = dm

    #go through the other members and remove them if not remove them from owner members
    for user in dm_leave['other_members']:
        if user['u_id'] == token_info['u_id']:
            dm_leave['other_members'].remove(user)
    
    for user in dm_leave['owner_members']:
        if user['u_id'] == token_info['u_id']:
            dm_leave['owner_members'].remove(user)
    
    return {}

    

