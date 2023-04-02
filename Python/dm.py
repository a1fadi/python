from src.data_store import data_store
from src.error import InputError, AccessError
from src.helpers import is_valid_user, get_owner, decode_jwt, checkIfDuplicates, create_dm_id, create_dm_name, list_other_members, get_usr_dms, make_notification


def dm_messages_v1(token, dm_id, start):
    '''
    Message function that when given a dm id and a start value outputs 50 messages from the start value
    It returns a dictionary with the messages, start value and end value
    If there are not 50 messages it will return -1 for the end value
    '''

    token = str(token)
    dm_id = int(dm_id)
    start = int(start)
    
    info = data_store.get()   


    dm, valid_dm = is_valid_dm(info, dm_id)

    token_result = decode_jwt(token)
    auth_user_id = token_result["u_id"]

    
    if (valid_dm == False):
        raise InputError
    if (check_start_val(dm_id, start) == False):
        raise InputError
    if (is_user_valid_member_dm(info, auth_user_id, dm_id) == False):
        raise AccessError
    # Determines end value to be returned
    end = check_start_val(dm_id, start)

    # Gets the correct set of messages
    message_list = dm['messages']

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

def is_user_valid_member_dm(info, auth_user_id, dm_id):
    '''
    Helper function specifically for message implementation
    Checks if the user has access to the dm
    If they do returns true otherwise returns false
    '''
    
    for dm in info['dms']:
        if dm['dm_id'] == dm_id:
            dm_dic = dm
    
    if dm_dic['owner_members'][0]['u_id'] == auth_user_id :
        return True 
    
    for member in dm_dic['other_members']:
        if member['u_id'] == auth_user_id:
            return True
    
    return False

def is_valid_dm(info, dm_id):
    '''
    A helper function to test if the dm id passed into a function is of a 
    dm that already exists
    Parameters: info dictionary containing the data store, auth_user_id as an 
        integer
    Returns: returns true if the user id is a valid one and false if it is 
        invalid
    '''
    for dm in info['dms']:
        if dm['dm_id'] == dm_id:
            return (dm, True)

    return None, False

def check_start_val(dm_id, start):
    '''
    Helper function specifically for message implementation
    Checks if the start value inputted refers to an actual message
    If not returns False
    If it does either returns -1 if all the messages are to be displayed or
    it returns the start value plus 50
    '''
    # Finds total number of messages
    dms = data_store.get()['dms']
    
    for dm in dms:
        if (dm['dm_id'] == dm_id):
            result = dm 
    
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


def dm_create_v1(token, u_ids):
    '''
    Creates a DM between an owner and u_ids
    Parameters: token as an int and u_ids as a list of ints
    Returns: A dictionary of the created dm's id
    '''
    # Checking valid user
    info = data_store.get()
    decoded_jwt = decode_jwt(token)
    auth_user_id = decoded_jwt['u_id']

    if checkIfDuplicates(u_ids):
        raise InputError("Duplicate u_ids exist")
    

    for users in u_ids:
        if is_valid_user(info, users) == False:
            raise InputError(f"An invalid u_id exists: {users}")
    
    # Put data in new dm
    u_ids.append(auth_user_id)
    dms = data_store.get()['dms']

    dm_id = create_dm_id()
    name = create_dm_name(u_ids)
    owner = get_owner(auth_user_id)

    new_owner = owner.copy()
    new_owner.pop('password')
    new_owner.pop('permission_id')
    new_owner.pop('session_id')
    new_owner.pop('reset_code')
    new_owner.pop('notifications')
    
    other_members_list = list_other_members(auth_user_id, u_ids)
    
    new_dm = {
            'dm_id': dm_id,
            'name': name,
            'owner_members': [new_owner],
            'other_members': other_members_list,
            'messages': [],
        }

    dms.append(new_dm)
    
    #Sending notification 
    # #MAKE FOR LOOP MAKING A NOTIFICATION FOR EVERYONE IN U_IDS  
    handle = data_store.get()['users']
    for i in handle:
        if i['u_id'] == auth_user_id:
            target_handle = i['handle_str']

    dm_name = new_dm['name']
    for user in u_ids:
        notification_message = f'{target_handle} added you to {dm_name}'
        make_notification(user, -1, dm_id, notification_message) 
  
    info['dms'] = dms
    data_store.set(info)
    return {'dm_id': dm_id}


def dm_list_v1(token):
    '''
    Provides a list of all dms (and their associated details)
    that the authorised user is part of.
    Parameters: auth user id as an integer
    Return: A dictionary containing a list of dictionaries with the name and
        id of dms the authorised user is a part of
    '''
    token = str(token)

    decoded_jwt = decode_jwt(token)
    auth_user_id = decoded_jwt['u_id']
    
    all_data = data_store.get()
    usr_dms = get_usr_dms(auth_user_id, all_data)

    return {'dms': usr_dms}

