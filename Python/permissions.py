from src.data_store import data_store
from src.error import InputError
from src.error import AccessError
from src.helpers import is_valid_user, decode_jwt

'''
Functions that interpret or modify the global permissions of a user
'''

def admin_change_user_perms_v1(token, u_id, permission_id):
    '''
    A function that allows an admin to change the permissions of a user
    Parameters: admin's token, target's u_id, permission_id wanted
    Return: An empty dictionary (POST)
    '''

    # Gets user id, tests the token validity and extracts information from the jwt payload
    user_info = data_store.get()['users']
    decoded_jwt = decode_jwt(token)
    info = data_store.get()

    auth_u_id = decoded_jwt['u_id']

    # If permission Id is invalid raise Input Error
    if permission_id not in [1, 2]:
        raise InputError("Invalid Permission Id") 
    
    # If target user doesn't exist or is invalid then raise Input Error
    if is_valid_user(info, u_id) == False:
        raise InputError("Target is not a valid user")

    # If JWT is invalid or user is not logged in then raise Access Error
    for user in user_info:
        if user['u_id'] == auth_u_id and user['permission_id'] != 1:
            raise AccessError("Authorised User is not an Admin")
    
    global_owners = 0

    # Count number of global owners
    for user in user_info:
        if user['permission_id'] == 1:
            global_owners += 1

    # If target user is the only admin or already has wanted permissions then raise Input Error otherwise update their permissions
    for user in user_info:
        if u_id == user['u_id'] and user['permission_id'] == 1 and global_owners == 1 and permission_id == 2:
            raise InputError("Cannot demote only admin to member")
        elif u_id == user['u_id'] and user['permission_id'] == permission_id:
            raise InputError("Target user already has those permissions")
        elif u_id == user['u_id']:
            user['permission_id'] = permission_id
    
    return {}

def admin_remove_user_v1(token, u_id):

    '''
    removes a user completely from SEAMS, changes their name/handle and access permisions (can only be done by a global member) 

    Arguements:
        token (string) - must be a valid token
        u_id(integer) - must be a valid user id

    Exceptions:
        Input Error - Occurs when:
                        - token is invalid
                        - u_id isnt a valid user
                        - u_id is the only global owner 
                        
        Access Error - Occurs when:
                        - auth user isn't a global owner

    Return Value:
        Returns empty dictionary
    '''

    info = data_store.get()
    user_info = data_store.get()['users']
    channel_info = data_store.get()['channels']
    
    token_info = decode_jwt(token)

    # If target user doesn't exist or is invalid then raise Input Error
    if is_valid_user(info, u_id) == False:
        raise InputError
    
    # If JWT is invalid or user is not logged in then raise Access Error
    
    for user in user_info:
        if token_info['u_id'] == user['u_id']:
            if user['permission_id'] != 1:
                raise AccessError("Authorised User is not an Admin")
            break
    
    global_owners = 0
    # Count number of global owners

    for user in user_info:
        if user['permission_id'] == 1:
            global_owners += 1

    for user in user_info:
        if u_id == user['u_id'] and user['permission_id'] == 1 and global_owners == 1:
            raise InputError

    
    #remove the user from seams and replace their messages with 'removed user'
    #change users 'name'
    for user in user_info:
        if user['u_id'] == u_id:
            user['name_first'] = "Removed"
            user['name_last'] = "user"
            user['handle_str'] = " "
            user['email'] = " "
    # Change all their messages to "Removed User"
    
    for channel in channel_info:
        message_list = channel['messages']
        for i in range(len(message_list)):
            if message_list[i]['u_id'] == u_id:
                message_list[i]['message'] = "Removed user"
            
    #remove their user id from any member lists within the channel (owner and other members)
    for channel in channel_info:
        user_list = channel['owner_members']
        i = 0
        for i in range(len(user_list)):
            if user_list[i]['u_id'] == u_id:
                del user_list[i]
                

    for channel in channel_info:
        user_list = channel['other_members']
        i = 0
        for i in range(len(user_list)):
            if user_list[i]['u_id'] == u_id:
                del user_list[i]
 
    

    #Remove the messages they have sent in dms and replace with 'removed user' 
    dm_info = data_store.get()['dms']

    for dm in dm_info:
        message_list = dm['messages']
        i = 0
        for i in range(len(message_list)):
            if message_list[i]['u_id'] == u_id:
                message_list[i]['message'] = "Removed user"

    #Find which dms they are in and remove them from it (either owner or other members)
    for dm in dm_info:
        user_list = dm['owner_members']
        i = 0
        for i in range(len(user_list)):
            if user_list[i]['u_id'] == u_id:
                del user_list[i]
                
    for dm in dm_info:
        user_list = dm['other_members']
        i = 0
        for i in range(len(user_list)):
            if user_list[i]['u_id'] == u_id:
                del user_list[i]
                
    
