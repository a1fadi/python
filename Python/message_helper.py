'''
Author: Charlie Sargent
zID: z5310794
Completes message functions
'''

from pickle import TRUE
from random import randint
from datetime import timezone
import datetime

from src.data_store import data_store
from src.helpers import decode_jwt, get_owner
from src.channel import channel_details_v2
from src.dms import dm_details_v1
from src.error import InputError, AccessError



def get_time():
    '''
    Gets the time the message is sent
    '''
    date_time = datetime.datetime.now(timezone.utc)

    utc_time = date_time.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()

    return(utc_timestamp)

def check_member_channel(token, channel_id):
    '''
    Checks that the user is a member of the channel
    '''
    token_decode = decode_jwt(token)
    user_id = token_decode["u_id"] 
    
    channel_details = channel_details_v2(token, channel_id)

    for user in channel_details['owner_members']:
        if user['u_id'] == user_id:
            return True
    for user in channel_details['all_members']:
        if user['u_id'] == user_id:
            return True

def og_message_id_check(token, message_id):
    '''
    Checks that user has access to the message
    '''
    token_decode = decode_jwt(token)
    user_id = token_decode["u_id"] 

    # Check Channels
    channels = data_store.get()['channels']

    for channel in channels:
        msg_list = channel['messages']
        for i in range(len(msg_list)):
            if msg_list[i]['message_id'] == message_id:
                for user in channel['owner_members']:
                    if user['u_id'] == user_id:
                        return True
                for user in channel['other_members']:
                    if user['u_id'] == user_id:
                        return True
    
    # Check dms
    dms = data_store.get()['dms']

    for dm in dms:
        msg_list = dm['messages']
        for i in range(len(msg_list)):
            if msg_list[i]['message_id'] == message_id:
                for user in dm['owner_members']:
                    if user['u_id'] == user_id:
                        return True
                for user in dm['other_members']:
                    if user['u_id'] == user_id: #TODO TODO TODO TODO TODO TODO TODO 
                        return True

    return False


def get_og_message(message_id):
    '''
    Gets the og_message
    '''
    channels = data_store.get()['channels']

    for channel in channels:
        msg_list = channel['messages']
        for i in range(len(msg_list)):
            if msg_list[i]['message_id'] == message_id:
                return msg_list[i]['message']

    dms = data_store.get()['dms']

    for dm in dms:
        msg_list = dm['messages']
        for i in range(len(msg_list)):
            if msg_list[i]['message_id'] == message_id:
                return msg_list[i]['message']

def check_valid_dm(dm_id):
    '''
    Checks that dm is valid
    '''
    dms = data_store.get()['dms']

    for dm in dms:
        if dm['dm_id'] == dm_id:
            return True
    
    return False

def check_valid_channel(channel_id):
    '''
    Checks that channel id is valid
    '''
    channels = data_store.get()['channels']

    for channel in channels:
        if channel['channel_id'] == channel_id:
            return True
    
    return False

# Message edit helper functions
def check_message_id(message_id):
    '''
    Checks that the message_id refers to valid message
    '''
    channels = data_store.get()['channels']

    for channel in channels:
        msg_list = channel['messages']
        for i in range(len(msg_list)):
            if msg_list[i]['message_id'] == message_id:
                return True
    
    dms = data_store.get()['dms']

    for dm in dms:
        msg_list = dm['messages']
        for i in range(len(msg_list)):
            if msg_list[i]['message_id'] == message_id:
                return True

    return False

# def check_message(token, message_id):
#     '''
#     Checks that the message_id refers to valid message
#     '''
#     channels = data_store.get()['channels']

#     for channel in channels:
#         msg_list = channel['messages']
#         channel_id = channel['channel_id']
#         for i in range(len(msg_list)):
#             if check_member_channel(token, channel_id) == True:
#                 if msg_list[i]['message_id'] == message_id:
#                     return msg_list[i]['message']
    
#     dms = data_store.get()['dms']

#     for dm in dms:
#         msg_list = dm['messages']
#         dm_id = dm['dm_id']
#         for i in range(len(msg_list)):
#             if check_member_dm(token) == True:
#                 if msg_list[i]['message_id'] == message_id:
#                     return msg_list[i]['message']

#     raise InputError
#     return False

def check_user_auth(token, message_id):
    '''
    Checks that the user is either owner in channel or sent the message
    '''
    jwt_decode = decode_jwt(token)
    user_id = jwt_decode['u_id']

    channels = data_store.get()['channels']

    msg_user = 0
    owners = []

    for channel in channels:
        msg_list = channel['messages']
        for i in range(len(msg_list)):
            if msg_list[i]['message_id'] == message_id:
                msg_user = msg_list[i]['u_id']
                owners = channel['owner_members']

    if user_id == msg_user or user_id in owners:
        return True
    
    raise AccessError

def check_member_dm_messages(token, message_id):
    '''
    Checks if person can edit the message of the dm
    '''
    jwt_decode = decode_jwt(token)
    user_id = jwt_decode['u_id']

    dms = data_store.get()['dms']

    msg_user = 0
    owners = []

    for dm in dms:
        msg_list = dm['messages']
        for i in range(len(msg_list)):
            if msg_list[i]['message_id'] == message_id:
                msg_user = msg_list[i]['u_id']
                owners = dm['owner_members']

    if user_id == msg_user or user_id in owners:
        return True
    
    raise AccessError

def check_member_dm(token, dm_id): #TODO TODO TODO TODO TODO
    '''
    Checks that the user is either owner in dm or sent the message
    '''
    dm_details_v1(token, dm_id)

    return True


def check_repeat_msg_id(message_id):
    '''
    Ensures that message_id has not already been used
    '''
    channels = data_store.get()['channels']
    dms = data_store.get()['dms']
    messages_sendlater = data_store.get()['messages_sendlater']

    for channel in channels:
        msg_list = channel['messages']
        for i in range(len(msg_list)):
            if msg_list[i]['message_id'] == message_id:
                return False
    
    for dm in dms:
        msg_list = dm['messages']
        for i in range(len(msg_list)):
            if msg_list[i]['message_id'] == message_id:
                return False
    
    for message in messages_sendlater:
        if message['message_id'] == message_id:
            return False
    
    return True

def get_message_dic(token, message):
    '''
    Produces the message dictionary to be placed in data_store
    '''
    message_id = 0
    while check_repeat_msg_id(message_id) == False:
        message_id += 1
    
    time = get_time()
    
    token_decode = decode_jwt(token)
    u_id = token_decode["u_id"]

    message_dic = {
        'message_id': message_id,
        'u_id': u_id,
        'message': message,
        'time_sent': time,
        'reacts': 0,
        'is_pinned': False,
    }
    
    return message_dic

def check_current_react(message_id):
    '''
    Checks that the message has not already been reacted
    '''
    channels = data_store.get()['channels']

    for channel in channels:
        msg_list = channel['messages']
        for i in range(len(msg_list)):
            if msg_list[i]['message_id'] == message_id:
                return msg_list[i]['reacts']
    
    dms = data_store.get()['dms']

    for dm in dms:
        msg_list = dm['messages']
        for i in range(len(msg_list)):
            if msg_list[i]['message_id'] == message_id:
                return msg_list[i]['reacts']


def check_current_pin(message_id):
    '''
    Checks that the message is not already pinned
    '''
    channels = data_store.get()['channels']

    for channel in channels:
        msg_list = channel['messages']
        for i in range(len(msg_list)):
            if msg_list[i]['message_id'] == message_id:
                return msg_list[i]['is_pinned']
    
    dms = data_store.get()['dms']

    for dm in dms:
        msg_list = dm['messages']
        for i in range(len(msg_list)):
            if msg_list[i]['message_id'] == message_id:
                return msg_list[i]['is_pinned']

def check_user_permissions(token, message_id):
    '''
    Checks if the person pinning the message has owner permissions
    '''
    jwt_decode = decode_jwt(token)
    user_id = jwt_decode['u_id']
    
    owner = get_owner(user_id)
    new_owner = owner.copy()
    new_owner.pop('password')
    new_owner.pop('permission_id')
    new_owner.pop('session_id')
    new_owner.pop('reset_code')
    new_owner.pop('notifications')

    correct_location = 0

    channels = data_store.get()['channels']

    for channel in channels:
        msg_list = channel['messages']
        for i in range(len(msg_list)):
            if msg_list[i]['message_id'] == message_id:
                correct_location = 1
                break
        owner_members = channel['owner_members']
        if correct_location == 1 and new_owner not in owner_members:
            return False


    dms = data_store.get()['dms']

    for dm in dms:
        msg_list = dm['messages']
        for i in range(len(msg_list)):
            if msg_list[i]['message_id'] == message_id:
                correct_location = 1
                break
        owner_members = dm['owner_members']
        if correct_location == 1 and new_owner not in owner_members:
            return False

    return True

def check_sendlater():
    '''
    Checks to see if any messages can be added to the relevant channel or dm
    Checks against the time
    '''
    messages_sendlater = data_store.get()['messages_sendlater']
    info = data_store.get()

    current_time = get_time()

    for message in messages_sendlater:
        if message['time_sent'] <= current_time:
            add_sendlater(message)
            messages_sendlater.remove(message)

    info['messages_sendlater'] = messages_sendlater
    data_store.set(info)

    return

def add_sendlater(message):
    '''
    Adds messages that can be from sendlater to the relevant channel or dm
    '''

    channels = data_store.get()['channels']
    dms = data_store.get()['dms']

    new_message = message.copy()
    new_message.pop('channel')
    new_message.pop('id')

    if message['channel'] == True:
        for channel in channels:
            if message['id'] == channel['channel_id']:
                channel['messages'].insert(0, new_message)
                break

    if message['channel'] == False:
        for dm in dms:
            if message['id'] == dm['dm_id']:
                dm['messages'].insert(0, new_message)
                break

    return