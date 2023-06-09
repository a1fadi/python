'''
data_store.py

This contains a definition for a Datastore class which you should use to store your data.
You don't need to understand how it works at this point, just how to use it :)

The data_store variable is global, meaning that so long as you import it into any
python file in src, you can access its contents.

Example usage:

    from data_store import data_store

    store = data_store.get()
    print(store) # Prints { 'names': ['Nick', 'Emily', 'Hayden', 'Rob'] }

    names = store['names']

    names.remove('Rob')
    names.append('Jake')
    names.sort()

    print(store) # Prints { 'names': ['Emily', 'Hayden', 'Jake', 'Nick'] }
    data_store.set(store)
'''
SECRET = "F09A_Ants"
TOTAL_NUMBER_OF_SESSIONS = 0

## YOU SHOULD MODIFY THIS OBJECT BELOW

initial_object = {
    'users': [
        {
            'u_id': 0,
            'email': " ",
            'password': " ",
            'name_first': " ",
            'name_last': " ", 
            'handle_str': " ",
            'session_id': [],
            'permission_id': 0,
            'reset_code': "",
            'notifications': [{
                'channel_id': 0,
                'dm_id': 0,
                'notification_message': " ",
            }],
        },
    ],
    'channels': [
        {
            'channel_id': 0,
            'name': " ",
            'is_public': True,
            'owner_members': [],
            'other_members': [],
            'messages': [{
                'message_id': 0,
                'u_id': 0,
                'message': " ",
                'time_sent': 0,
                'reacts': 0,
                'is_pinned': False,
            }],
        },
    ],
    'dms': [
        {
            'dm_id': 0,
            'name': " ",
            'owner_members': [],
            'other_members': [],
            'messages': [{
                'message_id': 0,
                'u_id': 0,
                'message': " ",
                'time_sent': 0,
                'reacts': 0,
                'is_pinned': False,
            }],
        },
    ],
    'messages_sendlater': [
        {
            'message_id': 0,
            'u_id': 0,
            'message': " ",
            'time_sent': 0,
            'reacts': 0,
            'is_pinned': False,
            'channel': True,
            'id': 0,
        },
    ],
}

## YOU SHOULD MODIFY THIS OBJECT ABOVE

## YOU ARE ALLOWED TO CHANGE THE BELOW IF YOU WISH
class Datastore:
    def __init__(self):
        self.__store = initial_object

    def get(self):
        return self.__store

    def set(self, store):
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.__store = store

print('Loading Datastore...')

global data_store
data_store = Datastore()
