from base64 import decode
from src.data_store import data_store, SECRET
from src.error import AccessError, InputError
import re
import jwt

'''
A file containing all the helper functions that are used across multiple
functions in the channel.py and channels.py files

This file is a hub for any functions that need to be used across multiple 
functions or files.
'''

'''
JWT HELPER FUNCTIONS

'''
def decode_jwt(token):
    '''
    Helper function to decode the token that we are given and validate that it is real as well as return the payload
    Parameters: token and global variable SECRET
    Return: token payload as {"u_id": xxxxxxx, "session_id": xx}
    '''
    try:
        decoded_jwt = jwt.decode(token, SECRET, algorithms=["HS256"])

    except jwt.InvalidTokenError as invalid_token_passed:
        print(token)
        #print(decoded_jwt)
        raise AccessError("Invalid Token") from invalid_token_passed
    
    check_user_exists = 0

    user_info = data_store.get()['users']
    for user in user_info:
        if decoded_jwt['u_id'] == user['u_id'] and (decoded_jwt['session_id'] not in user['session_id']):
            raise AccessError("Invalid Session")
        elif decoded_jwt['u_id'] == user['u_id']:
            check_user_exists += 1

    if check_user_exists == 0:
        raise AccessError

    return decoded_jwt


'''
CHANNEL HELPER FUNCTIONS
'''

def is_valid_channel(info, channel_id):
    '''
    A helper function to test if the channel id passed into a function is of a 
    channel that already exists
    Parameters: info dictionary containing the data store, channel id as an 
        integer
    Returns: returns true if the user id is a valid one and false if it is 
        invalid

    Functions that use it: 
        Channel_details_v1
        Channel_join_v1
        Channel_invite_v1


    '''

    for channel in info['channels']:
        if channel['channel_id'] == channel_id:
            return (channel, True)

    return None, False

def is_valid_user(info, auth_user_id):
    '''
    A helper function to test if the user id passed into a function is an 
    authorised one
    Parameters: info dictionary containing the data store, auth_user_id as 
        an integer
    Returns: returns true if the user id is a valid one and false if it is 
        invalid

        Functions that use it: 
        Channel_details_v1
        Channel_join_v1
        Channel_invite_v1
        
    '''

    for user in info['users']:
        if user['u_id'] == auth_user_id:
            return True
    return False

def is_valid_message_channel(channel_id):
    '''
    Helper function specifically for message implementation
    Checks if the channel is valid then outputs the channel id if it is
    '''
    channels = data_store.get()['channels']
    
    for channel in channels:
        if (channel['channel_id'] == channel_id):
            return channel 


def check_start_val(info, channel_id, start):
    '''
    Helper function specifically for message implementation
    Checks if the start value inputted refers to an actual message
    If not returns False
    If it does either returns -1 if all the messages are to be displayed or
    it returns the start value plus 50
    '''
    # Finds total number of messages
    result = is_valid_message_channel(channel_id)
    messages_list = result['messages']
    num_messages = len(messages_list)

    # Checks if start value sits in range
    if start < 0 :
        return False
    elif start > num_messages :
        return False
    elif ((num_messages - start) < 50):
        return -1
    else:
        return (start + 50)


def is_user_valid_member(info, auth_user_id, channel_id):
    '''
    Helper function specifically for message implementation
    Checks if the user has access to the channel
    If they do returns true otherwise returns false
    '''
    for channel in info['channels']:
        if channel['channel_id'] == channel_id:
            channel_dic = channel

    for owner in channel_dic['owner_members'] :
        if owner['u_id'] == auth_user_id :
            return True

    for member in channel_dic['other_members']:
        if member['u_id'] == auth_user_id:
            return True
    
    
    return False


'''
CHANNELS HELPER FUNCTIONS
'''
def is_valid_channel_name(string):

    length = len(string)
    return False if length <= 1 or length >= 20 else True

def create_channel_id():
    '''
    Creates a channel id for a new channel
    Parameters: 
    Returns: A channel id as an integer
    '''
    i = len(data_store.get()['channels'])
    channel_id = i + 1
    return channel_id

def get_owner(id):
    '''
    Returns a dictionary of the user who's id is entered
    Parameters: id as an integer
    Returns: A dictionary of a user
    '''
    users = data_store.get()['users']
    for user in users:
        if user['u_id'] == id:
            return user

def get_usr_channels(id, data):
    '''
    Return a list of channels that the id is part of
    Parameters: id as an integer, channels_list as a list
    Returns: A list of channels that the id is in
    '''
    usr_channels = []

    if data['channels'] == []:
        return usr_channels
    
    channels_list = data['channels']
    required_keys = ['channel_id', 'name']

    for channel in channels_list:
        if channel['owner_members'][0]['u_id'] == id:
            channel_info = {key:value for key, value in channel.items() if key in required_keys}
            usr_channels.append(channel_info)
            continue

    return usr_channels


'''
DMS HELPER FUNCTIONS
'''

def user_in_channel(auth_user_id, required_channel):
    
    for user in required_channel['other_members']:
        if user['u_id'] == auth_user_id:
            return False

    for user in required_channel['owner_members']:
        if user['u_id'] == auth_user_id:
            return False
            
    return True 

def user_not_channel(auth_user_id, required_channel):
    verifier = False 
    for user in required_channel['owner_members']:
        if user['u_id'] == auth_user_id:
            verifier = True 
    for user in required_channel['other_members']:
        if user['u_id'] == auth_user_id:
            verifier = True  

    return verifier 

def user_not_dm(auth_user_id, required_dm):

    verifier = False 
    for user in required_dm['owner_members']:
        if user['u_id'] == auth_user_id:
            verifier = True 
    for user in required_dm['other_members']:
        if user['u_id'] == auth_user_id:
            verifier = True  

    return verifier 


def checkIfDuplicates(list):
    '''
    Checks if a list contains duplicates
    Parameters: A list
    Returns: True if there are duplicates, otherwise False
    '''
    if len(list) == len(set(list)):
        return False
    else:
        return True

def create_dm_id():
    '''
    Creates a dm id for a new dm
    Parameters: 
    Returns: A dm id as an integer
    '''
    dms = data_store.get()['dms']
    if len(dms) == 0:
        dm_id = 1
    else:
        last_id = dms[-1]['dm_id']
        dm_id = last_id + 1
    return dm_id

def list_other_members(owner_id, id_list):
    '''
    Creates a list of users excluding the owner
    Parameters: owner_id as int and id_list as list
    Returns: A list of ids
    '''
    id_list.remove(owner_id)
    members_list = []

    for id in id_list:
        user = get_owner(id).copy()
        user.pop('password')
        user.pop('permission_id')
        user.pop('session_id')
        user.pop('reset_code')
        user.pop('notifications')
        members_list.append(user)
        
    return members_list

def create_dm_name(id_list):
    '''
    Creates a dm name using a list of ids.
        The list should be the handles of the ids alphabetically sorted and comma-and-space separated
    Parameters: A list of ids
    Returns: A string for the dm name
    '''

    handle_list = []
    for u_id in id_list:
        user = get_owner(u_id)
        user_handle = user['handle_str']
        handle_list.append(user_handle)


    handle_list.sort()

    dm_name = ', '.join(handle_list)

    return dm_name

def get_usr_dms(u_id, data):
    '''
    Return a list of dms that the id is part of
    Parameters: id as an integer, dms_list as a list
    Returns: A list of dms that the id is in
    '''
    usr_dms = []

    if data['dms'] == []:
        return usr_dms

    dms_list = data['dms']

    for dm in dms_list:
        if dm['owner_members'][0]['u_id'] == u_id:
            dm_id = dm['dm_id']
            dm_name = dm['name']
            dm_info = {'dm_id': dm_id, 'name': dm_name}
            usr_dms.append(dm_info)
            continue
  
        other_member_list = dm['other_members']
        length = len(other_member_list) 
        i = 0
        for i in range(length):
            if u_id == other_member_list[i]['u_id']:
                dm_id = dm['dm_id']
                dm_name = dm['name']
                dm_info = {'dm_id': dm_id, 'name': dm_name}
                usr_dms.append(dm_info)
                continue


    return usr_dms


def is_valid_dm(info, dm_id):
    '''
    A helper function to test if the dm id passed into a function is of a 
    dm group that already exists
    Parameters: info dictionary containing the data store, dm id as an 
        integer
    Returns: returns true if the user id is a valid one and false if it is 
        invalid
    '''
    for dm in info['dms']:
        if dm['dm_id'] == dm_id:
            return (dm, True)
    return None, False

def make_notification(auth_user_id, channel_id, dm_id, notification_message):

    ''' 
    Helper function that helps create a notification for a user, when passed in a user_id, 
    the notification gets stored within that users dictionary, channel_id refers to the channel
    that the notification refers to, similarly with dm_id, lastly notification message stores the 
    message that the notification is going to display
    '''

    '''
    Store values into notification dictionary using auth_user_id as the user value
    '''

    notification = {
        "channel_id": channel_id,
        "dm_id": dm_id, 
        "notification_message": notification_message,
    }
    # raise AccessError
    info = data_store.get()
    user = data_store.get()['users']
    for user_id in user:
        if user_id['u_id'] == auth_user_id:
            user_id['notifications'].insert(0, notification)
            info['users'] = user
            data_store.set(info)
    
    return




