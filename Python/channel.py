from src.data_store import data_store
from src.error import InputError, AccessError
from src.helpers import is_valid_user, is_valid_channel, check_start_val, is_user_valid_member, decode_jwt, user_in_channel, user_not_channel, make_notification


def channel_details_v2(token, channel_id):
    '''
    A function which returns the information of a particular channel as a 
    dictionary containing:
    {channel_id, name, is_public, owner_members, all_members}
    Parameters: a user id in the form of an integer, a channel id in the 
        form of an integer
    Returns: returns true if the user id is a valid one and false if it is 
        invalid
    '''
    token = str(token)
    channel_id = int(channel_id)
    
    info = data_store.get()
    token_info = decode_jwt(token)
    if info['channels'] == []:
        raise InputError("No Channels Exist")


    required_channel, valid_channel = is_valid_channel(info, channel_id)
    user_in_channel = False

    '''
    Following are the tests to make sure the correct errors are raised
    '''
    if valid_channel == False:
        raise InputError("Please Enter a Valid Channel Id")

    for member in required_channel['owner_members']:
        if member['u_id'] == token_info['u_id']:
            user_in_channel = True
    
    for member in required_channel['other_members']:
        if member['u_id'] == token_info['u_id']:
            user_in_channel = True

    if user_in_channel == False:
        raise AccessError("User is not a Member of this Channel")
    
    details = required_channel.copy()    
    # Makes a copy of the channel information
    details.pop('channel_id')  
    # Removes the unnecessary fields of channel_id and messages
    details.pop('messages')
    details['all_members'] = []
    for item in details['owner_members']:
        details['all_members'].append(item)
    for item in details['other_members']:
        details['all_members'].append(item)
    # Makes sure all owners contains correct information
    details.pop('other_members') # Removes the other owners field

    return details
    


def channel_messages_v2(token, channel_id, start):
    '''
    Message function that when given a channel id and a start value outputs 50 messages from the start value
    It returns a dictionary with the messages, start value and end value
    If there are not 50 messages it will return -1 for the end value
    '''
    # Setting up data store
    info = data_store.get()   

    token = str(token)
    channel_id = int(channel_id)
    start = int(start)

    channel, valid_channel = is_valid_channel(info, channel_id)

    token_result = decode_jwt(token)
    auth_user_id = token_result["u_id"]

    # Error checking statements
    if (valid_channel == False):
        raise InputError
    if (check_start_val(info, channel_id, start) == False):
        raise InputError
    if (is_user_valid_member(info, auth_user_id, channel_id) == False):
        raise AccessError

    # Determines end value to be returned
    end = check_start_val(info, channel_id, start)

    # Gets the correct set of messages
    message_list = channel['messages']

    # Checks if list is less than 50 and ensures list does return extra items
    if (end == -1):
        num_messages = len(message_list)
        list_end = num_messages - start
        messages = message_list[start:list_end]
    elif (end > 0):
        messages = message_list[start:end]


    return {
        'messages': messages,
        'start': start,
        'end': end,
    }

    
def channel_join_v2(token, channel_id):  

    '''
    appends a user to a channels other member list given it is a public channel

    Arguements:
        token (string) - must be a valid token
        channel_id (integer) - must be a valid channel id (i.e channel exists)

    Exceptions:
        Input Error - Occurs when:
                        - token is invalid
                        - channel id doesn't exist 
                        - user is already a member 

        Access Error - Occurs when:
                        - Channel is private and user isn't a global member

    Return Value:
        Returns empty dictionary
        '''


    #retrieve all the data necessary and store in variables 
    info = data_store.get()
    required_channel, valid_channel = is_valid_channel(info, channel_id)

    token_result = decode_jwt(token)
    user_id = token_result["u_id"]

    '''
    To raise an InputError if the users ID is invalid
    '''      
    '''
    To raise an InputError if the Channel ID is invalid
    '''
    if valid_channel == False:
        raise InputError
    '''
    To check if the user is already in the respective channel
    '''
    if user_in_channel(user_id, required_channel) == False:
        raise InputError

    '''
    To deny access into a private channel
    '''
    for user in info['users']:
        if user['u_id'] == token_result['u_id']:
            if user['permission_id'] != 1:
                if required_channel['is_public'] == False:
                    raise AccessError
    '''
    Adding the new user into the channels list of members
    '''
    new_member = {}
    for user in info['users']:
        if user['u_id'] == token_result['u_id']:
            new_member = user.copy()

    new_member.pop('password')
    new_member.pop('notifications')
    
    required_channel['other_members'].append(new_member)
    

def channel_invite_v2(token, channel_id, u_id):

    '''
    appends a user to a channels other member list given the inviter is part of the channel

    Arguements:
        token (string) - must be a valid token
        channel_id (integer) - must be a valid channel id (i.e channel exists)
        u_id (integer) - must be a valid user id

    Exceptions:
        Input Error - Occurs when:
                        - token is invalid
                        - channel id doesn't exist 
                        - u_id is already a member 
                        - uid isnt valid

        Access Error - Occurs when:
                        - Auth user isnt a part of the channel

    Return Value:
        Returns empty dictionary
        '''


    info = data_store.get()
    required_channel, valid_channel = is_valid_channel(info, channel_id)

    token_result = decode_jwt(token)
    user_id = token_result["u_id"]

    '''
    Test to see if inviters used ID is valid
    ''' 

    '''
    Test to see if person being invited used ID is valid
    '''

    if is_valid_user(info, u_id) == False:
        raise InputError

    '''
    Test to see if channel ID is valid
    '''

    if valid_channel == False:
        raise InputError

    '''
    Checking to see if the inviter is in the channel already, if not raising an error
    '''

    if user_not_channel(user_id, required_channel) == False:
        raise AccessError


    '''
    Checking to see that the person being invited isnt already in the channel
    '''
    if user_not_channel(u_id, required_channel) == True:
        raise InputError
    
    '''
    Test to see if person invited is actually being added to the channels members list
    '''

    new_member = {}
    for user in info['users']:
        if user['u_id'] == u_id:
            new_member = user.copy()

    new_member.pop('password')
    new_member.pop('session_id')
    new_member.pop('permission_id')
    new_member.pop('reset_code')
    new_member.pop('notifications')
    
    required_channel['other_members'].append(new_member) 
    #Sending notification
    target_handle = " "
    handle = data_store.get()['users']
    for i in handle:
        if i['u_id'] == user_id:
            target_handle = i['handle_str']

    channel_name = required_channel['name']
    notification_message = f'{target_handle} added you to {channel_name}'
    make_notification(u_id, channel_id, -1, notification_message)      
                

def channel_leave_v1(token, channel_id):
    
    '''
    removes a user from a channels member lists (either owner or other)

    Arguements:
        token (string) - must be a valid token
        channel_id (integer) - must be a valid channel id (i.e channel exists)

    Exceptions:
        Input Error - Occurs when:
                        - token is invalid
                        - channel id doesn't exist 
                        
        Access Error - Occurs when:
                        - user isnt already a member 

    Return Value:
        Returns empty dictionary
    '''

    channel_info = data_store.get()['channels']
    token_result = decode_jwt(token)
    user_id = token_result["u_id"]

    '''
    Check whether channel is a valid channel 
    '''

    channel_exists = False
    for id in channel_info:
        if id['channel_id'] == channel_id:
            channel_exists = True 

    if channel_exists == False:
        raise InputError

    '''
    Check whether user is already in the channel or not
    '''

    user_exists = False
    for channel in channel_info:
        for user in channel['owner_members']: 
            if user['u_id'] == user_id: 
                user_exists = True
    
    for channel in channel_info:
        for user in channel['other_members']:
            if user['u_id'] == user_id:
                user_exists = True
        
    if user_exists == False:
        raise AccessError

    for channel in channel_info:
        if channel['channel_id'] == channel_id: 
            channel_leave = channel
    '''
    Remove said user from the list if theyre an owner member
    '''
    
    for user in channel_leave['other_members']:
        if user['u_id'] == user_id:
            channel_leave['other_members'].remove(user)
   
    '''
    Remove said user from the list if theyre a regular member
    '''
    for user in channel_leave['owner_members']:
        if user['u_id'] == user_id:
            channel_leave['owner_members'].remove(user)

    return {}    

def channel_add_owner_v1(token, channel_id, u_id):

    '''
    adds an owner to the owners list of a channel 

    Arguements:
        token (string) - must be a valid token
        channel_id (integer) - must be a valid channel id (i.e channel exists)
        u_id(integer) - must be a valid user id

    Exceptions:
        Input Error - Occurs when:
                        - token is invalid
                        - channel id doesn't exist 
                        - u_id isnt a member of the channel 
                        - u_id is already a owner of the channel 
                        
        Access Error - Occurs when:
                        - auth user isn't an owner or global owner

    Return Value:
        Returns empty dictionary
    '''

    info = data_store.get()
    user_info = data_store.get()['users']
    required_channel, valid_channel = is_valid_channel(info, channel_id)

    token_result = decode_jwt(token)
    user_id = token_result['u_id']

    '''
    Check whether channel is a valid channel 
    '''

    if valid_channel == False: 
        raise InputError 
    
    '''
    Check whether 'future owner' ID is valid
    '''

    if is_valid_user(info, u_id) == False:
        raise InputError

    '''
    Check to see if the 'future owner' is already in the channel
    '''
    verify = 0
    for user in required_channel['other_members']:
        if user['u_id'] == u_id:
            verify += 1  
    if verify == 0:
        raise InputError 

    '''
    Check to see if authoriser himself is an owner or a global owner or any member at all 
    '''
    verify = 0
    verify2 = 0
    for user in required_channel['owner_members']:
        if user['u_id'] == token_result['u_id']:
            verify += 1
            verify2 += 1
    
    for user in required_channel['other_members']:
        if user['u_id'] == token_result['u_id'] and verify == 0:
            verify += 1

    for user in user_info:
        if user['u_id'] == user_id:
            if user['permission_id'] == 1:
                verify2 += 1

    if verify == 0:
        raise AccessError 
    
    if verify2 == 0:
        raise AccessError
    
    """
    Moving the member into owners
    """

    move_member = {}
    for user in info['users']:
        if user['u_id'] == u_id:
            move_member = user.copy()

    move_member.pop('password')
    move_member.pop('notifications')
    required_channel['other_members'].remove(move_member)
    required_channel['owner_members'].append(move_member)


def channel_remove_owner_v1(token, channel_id, u_id):

    '''
    removes an owner from the owners list of a channel 

    Arguements:
        token (string) - must be a valid token
        channel_id (integer) - must be a valid channel id (i.e channel exists)
        u_id(integer) - must be a valid user id

    Exceptions:
        Input Error - Occurs when:
                        - token is invalid
                        - channel id doesn't exist 
                        - u_id isnt a member of the channel 
                        - u_id is the only owner of the channel 
                        
        Access Error - Occurs when:
                        - auth user isn't an owner or global owner

    Return Value:
        Returns empty dictionary
    '''
    
    info = data_store.get()
    required_channel, valid_channel = is_valid_channel(info, channel_id)
    user_info = data_store.get()['users']
    token_result = decode_jwt(token)

    '''
    Check whether channel is a valid channel 
    '''

    if valid_channel == False: 
        raise InputError 
    
    '''
    Check whether 'user' ID is valid
    '''

    if is_valid_user(info, u_id) == False:
        raise InputError

        
    '''
    Check to see if user is the only owner of the channel
    '''
    if len(required_channel['owner_members']) == 1: 
        raise InputError

    '''
    Check to see if they are even a member or not 
    '''

    verify = 0
    for user in required_channel['owner_members']:
        if user['u_id'] == token_result['u_id']:
            verify += 1
    
    for user in required_channel['other_members']:
        if user['u_id'] == token_result['u_id']:
            verify += 1
    
    if verify == 0:
        raise AccessError

    '''
    Check to see if authoriser himself is an owner 
    '''
    verify = 0
    for user in required_channel['owner_members']:
        if user['u_id'] == token_result['u_id']:
            verify += 1

    for user in user_info:
        if user['u_id'] == token_result['u_id']:
            if user['permission_id'] == 1:
                verify +=1
    
    if verify == 0:
        raise AccessError 
    
    

    '''
    Check to see if the 'user' is already an owner of the channel
    '''

    verify = 0
    for user in required_channel['owner_members']:
        if user['u_id'] == u_id:
            verify += 1
    
    if verify == 0:
        raise InputError
      
    
    '''
    Remove the member from the owner_members list
    '''

    move_member = {}
    for user in info['users']:
        if user['u_id'] == u_id:
            move_member = user.copy()


    move_member.pop('password')
    move_member.pop('notifications')

    
    required_channel['owner_members'].remove(move_member)
    required_channel['other_members'].append(move_member) 

    return {}
