from src.data_store import data_store
from src.error import InputError
from src.helpers import is_valid_channel_name, create_channel_id, get_owner, get_usr_channels, decode_jwt



'''
Channels functions
'''


def channels_list_v2(token):
    '''
    Provides a list of all channels (and their associated details)
    that the authorised user is part of.
    Parameters: auth user id as an integer
    Return: A dictionary containing a list of dictionaries with the name and
        id of channels the authorised user is a part of
    '''
    token = str(token)

    # Checking for a valid id
    decoded_jwt = decode_jwt(token)
    auth_user_id = decoded_jwt['u_id']

    all_data = data_store.get()
    usr_channels = get_usr_channels(auth_user_id, all_data)

    # return usr_channels
    return {'channels': usr_channels}


def channels_listall_v2(token):
    '''
    A function to list the channel id and name of every single channel in the
    data store given that the inputting user id is a valid one
    Parameters: auth user id as an integer
    Return:  A dictionary containing a list of dictionaries with the name and
        id of all channels
    '''
    token = str(token)
    
    decode_jwt(token)
    
    required_keys = ['channel_id', 'name']
    channels = []
    channel_store = data_store.get()
    for channel in channel_store['channels']:
        '''
        For every channel in the data store it creates a dictionary with only 
        the channel id and channel name using dict comprehension
        Then it appends this dictionary to the list of channels
        '''
        channel_info = {key:value for key, value in channel.items() if key in required_keys}
        channels.append(channel_info)

    return {'channels': channels}


def channels_create_v2(token, name, is_public):
    '''
    Creates a new channel with the given name that is either 
    a public or private channel. The user who created it 
    automatically joins the channel.
    Parameters: auth user id as an integer, name as a string, is_public
        as a bool
    Returns: A dictionary containing the channel id 
    '''

    # Initial checks
    info = data_store.get()
    decoded_jwt = decode_jwt(token)
    auth_user_id = decoded_jwt['u_id']

    if is_valid_channel_name(name) == False:
        raise InputError("Channel name is too long")

    # Put data in new channels section
    channel = data_store.get()['channels']
    channel_id = create_channel_id()

    owner = get_owner(auth_user_id)
    new_owner = owner.copy()
    new_owner.pop('password')
    new_owner.pop('permission_id')
    new_owner.pop('session_id')
    new_owner.pop('reset_code')
    new_owner.pop('notifications')

    new_channel = {
        'channel_id': channel_id,
        'name': name,
        'is_public': is_public,
        'owner_members': [new_owner],
        'other_members': [],
        'messages': [],
    }

    channel.append(new_channel)  
    info['channels'] = channel
    data_store.set(info)
    return {'channel_id': channel_id}
    
    
