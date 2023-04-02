'''
Author: Charlie Sargent
zID: z5310794
Completes message functions:
 - message_send_v1
 - message_senddm_v1
 - message_edit_v1
 - message_remove_v1
 - message_react_v1
 - message_unreact_v1
 - message_pin_v1
 - message_unpin_v1
 - message_sendlater_v1
 - message_sendlaterdm_v1
'''

from random import randint
from datetime import timezone
import datetime

from src.data_store import data_store
from src.error import InputError, AccessError
from src.helpers import make_notification, decode_jwt, is_valid_dm, is_valid_channel
from src.message_helper import check_member_channel, check_valid_dm, check_message_id, check_user_auth, check_member_dm, get_message_dic
from src.message_helper import check_current_react, check_current_pin, check_user_permissions, get_time, check_valid_channel, check_repeat_msg_id
from src.message_helper import check_valid_dm,check_member_dm_messages
from src.message_helper import check_valid_dm, og_message_id_check, get_og_message, check_sendlater 
from src.dms import dm_details_v1
from src.helpers import decode_jwt
from src.channel import channel_details_v2

def message_send_v1(token, channel_id, message):
    '''
    Send a message from authorised user to specified channel
    '''

    message_length = len(message)
    # check_member = check_member_channel(token, channel_id)
    check_member_channel(token, channel_id)

    token_result = decode_jwt(token)
    user_id = token_result["u_id"]

    sender_users = data_store.get()['users']
    for user in sender_users:
        if user_id == user['u_id']:
            sender_handle = user['handle_str']

    # Error checks
    # if check_member == False: #TODO doesnt run
    #     raise AccessError
    if message_length < 1 or message_length > 1000:
        raise InputError
    
    message_dic = get_message_dic(token, message)

    channels = data_store.get()['channels']

    for channel in channels:
        if channel['channel_id'] == channel_id:
            channel['messages'].insert(0, message_dic)
            break

    all_members = channel_details_v2(token, channel['channel_id'])['all_members']

    for user in all_members:
        target_handle = user['handle_str']
        if f'@{target_handle}' in message:
            channel_name = channel['name']
            notification_message = f'{sender_handle} tagged you in {channel_name}'
            make_notification(user["u_id"], channel_id, -1, notification_message)
            

    return {'message_id': message_dic['message_id']}

def message_senddm_v1(token, dm_id, message):
    '''
    Send a message from authorised user to dm
    '''

    # valid_dm = check_valid_dm(dm_id)
    message_length = len(message)
    # member_dm = check_member_dm(token, dm_id)
    check_member_dm(token, dm_id)

    token_result = decode_jwt(token)
    user_id = token_result["u_id"]

    sender_users = data_store.get()['users']
    for user in sender_users:
        if user_id == user['u_id']:
            sender_handle = user['handle_str']

    # Error checks
    # if valid_dm == False: #TODO doesnt run
    #     raise InputError
    if message_length < 1 or message_length > 1000:
        raise InputError
    # if member_dm == False: #TODO Doesnt run
    #     raise AccessError 
    
    message_dic = get_message_dic(token, message)

    dms = data_store.get()['dms']

    for dm in dms:
        if dm['dm_id'] == dm_id:
            dm['messages'].insert(0, message_dic)
            break
    
    dm_users = dm_details_v1(token, dm_id)["members"]

    #make notification
    for user in dm_users:
        target_handle = user['handle_str']
        if f'@{target_handle}' in message:
            dm_name = dm['name']
            notification_message = f'{sender_handle} tagged you in {dm_name}'
            make_notification(user["u_id"], -1, dm_id, notification_message)

    message_id = message_dic['message_id']
    return {'message_id': message_id}


def message_edit_v1(token, message_id, message):
    '''
    Updates message with new text
    '''

    valid_msg_id = check_message_id(message_id)
    message_length = len(message)

    if message_length > 1000:
        raise InputError
    if valid_msg_id == False:
        raise InputError

    if message_length == 0:
        message_remove_v1(token, message_id)
        return

    channels = data_store.get()['channels']
    dms = data_store.get()['dms']

    for channel in channels:
        msg_list = channel['messages']
        i = 0
        for i in range(len(msg_list)):
            if msg_list[i]['message_id'] == message_id:
                check_user_auth(token, message_id)
                msg_list[i]['message'] = message
                break
    
    for dm in dms:
        msg_list = dm['messages']
        i = 0
        for i in range(len(msg_list)):
            if msg_list[i]['message_id'] == message_id:
                check_member_dm_messages(token, message_id)
                msg_list[i]['message'] = message
                break
    
    return {}
    

def message_remove_v1(token, message_id):
    ''' 
    Message is removed from channel / DM
    '''
    valid_msg_id = check_message_id(message_id)

    if valid_msg_id == False:
        raise InputError

    channels = data_store.get()['channels']

    i = 0

    for channel in channels:
        msg_list = channel['messages']
        i = 0
        for i in range(len(msg_list)):
            if msg_list[i]['message_id'] == message_id:
                check_user_auth(token, message_id)
                del msg_list[i]
                break
    
    dms = data_store.get()['dms']

    for dm in dms:
        msg_list = dm['messages']
        i = 0
        for i in range(len(msg_list)):
            if msg_list[i]['message_id'] == message_id:
                check_member_dm_messages(token, message_id)
                del msg_list[i]
                break

    return {}

def message_react_v1(token, message_id, react_id):
    '''
    Given a message within a channel / DM that the authorised user is a part of
    Adds a react to that message
    '''
    # Throws InputError when it isnt a valid message in channel / DM
    # TODO: Check they are in the channel
    valid_msg_id = check_message_id(message_id)

    token_result = decode_jwt(token)
    user_id = token_result["u_id"]

    sender_users = data_store.get()['users']
    for user in sender_users:
        if user_id == user['u_id']:
            sender_handle = user['handle_str']

    if valid_msg_id is False:
        raise InputError
    if react_id is not 1:
        raise InputError

    already_react = check_current_react(message_id)

    if already_react is 1:
        raise InputError
    
    channels = data_store.get()['channels']

    i = 0

    for channel in channels:
        msg_list = channel['messages']
        i = 0
        for i in range(len(msg_list)):
            if msg_list[i]['message_id'] == message_id:
                msg_list[i]['reacts'] = react_id
                #Sending notification
                u_id = msg_list[i]['u_id']

                channel_name = channel['name']
                notification_message = f'{sender_handle} reacted to your message in {channel_name}'
                make_notification(u_id, channel['channel_id'], -1, notification_message)
                break

    
    dms = data_store.get()['dms']

    for dm in dms:
        msg_list = dm['messages']
        i = 0
        for i in range(len(msg_list)):
            if msg_list[i]['message_id'] == message_id:
                msg_list[i]['reacts'] = react_id
                #Sending notification
                u_id = msg_list[i]['u_id']    
                dm_name = dm['name']
                notification_message = f'{sender_handle} reacted to your message in {dm_name}'
                make_notification(u_id, -1, dm['dm_id'], notification_message)
                break


    return {}



def message_unreact_v1(token, message_id, react_id):
    '''
    Given a message within a channel / DM that the authorised user is a part of
    Removes a react of that message
    '''
    # Throws InputError when it isnt a valid message in channel / DM
    valid_msg_id = check_message_id(message_id)

    if valid_msg_id is False: #TODO doesnt run
        raise InputError
    if react_id is not 1:
        raise InputError

    already_react = check_current_react(message_id)

    if already_react is not 1:
        raise InputError
    
    # Functionality
    channels = data_store.get()['channels']

    i = 0

    for channel in channels:
        msg_list = channel['messages']
        i = 0
        for i in range(len(msg_list)):
            if msg_list[i]['message_id'] == message_id:
                msg_list[i]['reacts'] = 0
                break
    
    dms = data_store.get()['dms']

    for dm in dms:
        msg_list = dm['messages']
        i = 0
        for i in range(len(msg_list)):
            if msg_list[i]['message_id'] == message_id:
                msg_list[i]['reacts'] = 0
                break

    return {}

def message_pin_v1(token, message_id):
    '''
    Given a message within a channel or DM, mark it as 'pinned'
    '''
    # Error checks
    valid_msg_id = check_message_id(message_id)
    current_pin = check_current_pin(message_id)
    user_permissions = check_user_permissions(token, message_id)

    if valid_msg_id is False:
        raise InputError
    if current_pin is True:
        raise InputError
    if user_permissions is False:
        raise AccessError

    # Functionality
    channels = data_store.get()['channels']

    i = 0

    for channel in channels:
        msg_list = channel['messages']
        i = 0
        for i in range(len(msg_list)):
            if msg_list[i]['message_id'] == message_id:
                msg_list[i]['is_pinned'] = True
                break
    
    dms = data_store.get()['dms']

    for dm in dms:
        msg_list = dm['messages']
        i = 0
        for i in range(len(msg_list)):
            if msg_list[i]['message_id'] == message_id:
                msg_list[i]['is_pinned'] = True
                break

def message_unpin_v1(token, message_id):
    '''
    Given a message within a channel or DM remove its mark as 'pinned'
    '''
    # Error checks
    valid_msg_id = check_message_id(message_id)
    current_pin = check_current_pin(message_id)
    user_permissions = bool(check_user_permissions(token, message_id))

    if valid_msg_id is False:
        raise InputError
    if current_pin is False:
        raise InputError
    if user_permissions is False:
        raise AccessError

    # Functionality
    channels = data_store.get()['channels']

    i = 0

    for channel in channels:
        msg_list = channel['messages']
        i = 0
        for i in range(len(msg_list)):
            if msg_list[i]['message_id'] == message_id:
                msg_list[i]['is_pinned'] = False
                break
    
    dms = data_store.get()['dms']

    for dm in dms:
        msg_list = dm['messages']
        i = 0
        for i in range(len(msg_list)):
            if msg_list[i]['message_id'] == message_id:
                msg_list[i]['is_pinned'] = False
                break

def message_share_v1(token, og_message_id, message, channel_id, dm_id):

    '''
    shares a message sent from one channel/dm to another + any addidtional message requested provided the user is in both

    Arguements:
        token (string) - must be a valid token
        og_message_id(integer) - id of message to be shared
        message(string) - can be empty, message that user would like to send with shared message 
        channel_id(integer) - must be a channel which exists
        dm_id(integer) - must be a valid dm that exists

    Exceptions:
        Input Error - Occurs when:
                        - both channel_id and dm_id are invalid
                        - neither channel_id nor dm_id are -1
                        - og_message_id does not refer to a valid message within a channel/DM that the authorised user has joined
                        - length of message is more than 1000 characters

                        
        Access Error - Occurs when:
                        - the pair of channel_id and dm_id are valid (i.e. one is -1, the other is valid) and 
                        the authorised user has not joined the channel or DM they are trying to share the message to

    Return Value:
        Returns dictionary containing shared message id { shared_message_id }
    '''

    if dm_id == -1:
        if check_valid_channel(channel_id) == False: 
            raise InputError
        check_member_channel(token, channel_id)
    elif channel_id == -1:
        if check_valid_dm(dm_id) == False:
            raise InputError
        check_member_dm(token, dm_id)
    else: 
        raise InputError

    if len(message) > 1000:
        raise InputError
    
    if check_message_id(og_message_id) == False: 
        raise InputError

    if og_message_id_check(token, og_message_id) == False:
        raise InputError

    og_message = get_og_message(og_message_id)

    shared_message = str(og_message + ' ' + message)

    if dm_id == -1:
        check_sendlater()
        shared_message_id = message_send_v1(token, channel_id, shared_message)["message_id"]
    elif channel_id == -1:
        check_sendlater()
        shared_message_id = message_senddm_v1(token, dm_id, shared_message)["message_id"]


    return {'shared_message_id': shared_message_id}


def message_sendlater_v1(token, channel_id, message, time_sent):
    '''
    Sends a message from user to channel automatically at a specificed time in the future
    '''
    message_length = len(message)
    # check_member = check_member_channel(token, channel_id)
    check_member_channel(token, channel_id)
    # check_channel = check_valid_channel(channel_id)
    current_time = get_time()

    decoded_jwt = decode_jwt(token)
    auth_user_id = decoded_jwt['u_id']

    # Error checks
    # if check_channel == False: #TODO doesnt run
    #     raise InputError
    if message_length < 1 or message_length > 1000:
        raise InputError
    if current_time > time_sent:
        raise InputError
    # if check_member == False: #TODO doesnt run
    #     raise AccessError

    message_id = 0
    while check_repeat_msg_id(message_id) == False: #TODO doesnt run
        message_id += 1

    messages_sendlater = data_store.get()['messages_sendlater']
    info = data_store.get()

    new_message = {
        'message_id': message_id,
        'u_id': auth_user_id,
        'message': message,
        'time_sent': time_sent,
        'reacts': 0,
        'is_pinned': False,
        'channel': True,
        'id': channel_id,
    }

    messages_sendlater.append(new_message)
    info['messages_sendlater'] = messages_sendlater
    data_store.set(info)

    return {'message_id': new_message['message_id']}
    

def message_sendlaterdm_v1(token, dm_id, message, time_sent):
    '''
    Sends a message from user to dm automatically at a specificed time in the future
    '''
    message_length = len(message)
    check_dm = check_valid_dm(dm_id)
    current_time = get_time()

    decoded_jwt = decode_jwt(token)
    auth_user_id = decoded_jwt['u_id']

    # Error checks
    if check_dm == False:
        raise InputError
    if message_length < 1 or message_length > 1000:
        raise InputError
    if current_time > time_sent:
        raise InputError
    
    check_member_dm(token, dm_id)

    message_id = 0
    while check_repeat_msg_id(message_id) == False:
        message_id += 1

    info = data_store.get()
    messages_sendlater = data_store.get()['messages_sendlater']

    new_message = {
        'message_id': message_id,
        'u_id': auth_user_id,
        'message': message,
        'time_sent': time_sent,
        'reacts': 0,
        'is_pinned': False,
        'channel': False,
        'id': dm_id,
    }

    messages_sendlater.append(new_message)
    info['messages_sendlater'] = messages_sendlater
    data_store.set(info)

    return {'message_id': new_message['message_id']}