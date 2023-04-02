from src.data_store import data_store
from src.error import AccessError
from src.helpers import decode_jwt

'''
Functions that interpret or modify the global permissions of a user
'''

def users_all_v1(token):
    '''
    A function that prints the details of all registered users
    Parameters: token
    Return: a dictionary containint a list of dictionaries {users} wheres users = [{xyz},{xyz}, ...]
    '''
    token = str(token)

    user_info = data_store.get()['users']

    decode_jwt(token)

    all_users = []
    for user in user_info:
        if user['name_first'] == 'Removed' and user['name_last'] == 'user':
            continue
        else:
            user_details = user.copy()
            user_details.pop('password')
            user_details.pop('session_id')
            user_details.pop('permission_id')
            user_details.pop('reset_code')
            user_details.pop('notifications')
            all_users.append(user_details)

    return {'users': all_users}