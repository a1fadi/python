from functools import total_ordering
from src.data_store import data_store, TOTAL_NUMBER_OF_SESSIONS
from src.error import InputError
from src.helpers import decode_jwt, user_not_channel, user_not_dm


def clear_v1():
    store = data_store.get()
    store['users'] = []
    store['channels'] = []
    store['dms'] = []
    store['messages_sendlater'] = []

    global TOTAL_NUMBER_OF_SESSIONS
    TOTAL_NUMBER_OF_SESSIONS = 0
    data_store.set(store)


def notifications_get_v1(token): 

    '''
   Return the user's most recent 20 notifications, ordered from most recent to least recent.

    Arguements:
        token (string) - must be a valid token

    Return Value:
        Returns dictionary of type notifications with all the notifications of the user, { notifications }
    '''

    token = str(token)
    notifications = []

    token_result = decode_jwt(token)
    user_id = token_result["u_id"]
    info = data_store.get()['users'] 
    
    for user in info:
        if user['u_id'] == user_id:  
            count = 0
            for i in user['notifications']:
                length = len(user['notifications'])
                notifications.append(i)
                count+=1
                if count >= 20 or count > length:
                    break

    return {'notifications': notifications} 

def search_v1(token, query_str):

    '''
    Given a query string, return a collection of messages in all of the channels/DMs 
    that the user has joined that contain the query (case-insensitive).

    Arguements:
        token (string) - must be a valid token
        query_str (string) - contains what is to be searched    

    Exceptions:
        Input Error - Occurs when:
                        - token is invalid
                        - length of query_str is less than 1 or over 1000 characters
                        
    Return Value:
        Returns dictionary of type messages with all the returns from the search, { messages }
    '''

    token = str(token)
    query_str = (str(query_str))
    
    messages = []
    info = data_store.get()['channels']

    dms = data_store.get()['dms']

    if (len(query_str) > 1000) or (len(query_str) < 1):
        raise InputError

    token_result = decode_jwt(token)
    auth_user_id = token_result["u_id"]

    for channel in info:
        if user_not_channel(auth_user_id, channel) == True:
            msg_list = channel['messages']
            for i in range(len(msg_list)):
                if query_str.lower() in (msg_list[i]['message']).lower():
                    messages.append(msg_list[i])
    
    for dm in dms:
        if user_not_dm(auth_user_id, dm) == True: 
            msg_list = dm['messages']
            for i in range(len(msg_list)):
                if query_str.lower() in (msg_list[i]['message']).lower():
                    messages.append(msg_list[i])

                    
    return {'messages': messages}



    



