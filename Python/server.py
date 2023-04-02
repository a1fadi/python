from distutils.log import debug
import sys
import signal
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.email import compose_email


from src.error import InputError
from src.auth import auth_register_v2, auth_login_v2, auth_logout_v1, auth_passwordreset_request_v1, auth_passwordreset_reset_v1
from src import config
from src.other import clear_v1, notifications_get_v1, search_v1
from src.channel import channel_join_v2, channel_invite_v2, channel_leave_v1, channel_add_owner_v1, channel_remove_owner_v1, channel_messages_v2, channel_details_v2
from src.channels import channels_list_v2, channels_create_v2, channels_listall_v2
from src.dm import dm_create_v1, dm_list_v1, dm_messages_v1
from src.dms import  dm_leave_v1, dm_remove_v1, dm_details_v1
from src.permissions import admin_remove_user_v1, admin_change_user_perms_v1
from src.users import users_all_v1
from src.user_profile import user_profile_v1, user_profile_setname_v1, user_profile_setemail_v1, user_profile_sethandle_v1
from src.message import message_send_v1, message_edit_v1, message_remove_v1, message_senddm_v1, message_react_v1, message_unreact_v1
from src.message import message_pin_v1, message_unpin_v1, message_sendlater_v1, message_sendlaterdm_v1, message_share_v1
from src.message_helper import check_sendlater

import pickle
from src.data_store import data_store

'''
ESTABLISHING PERSISTENCE
'''
clear_v1()
try:
    data_store = pickle.load(open("export.p", "rb"))
except Exception:
	pass

'''
FLASK SETUP
'''
def quit_gracefully(*args):
    '''For coverage'''
    exit(0)

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)


'''
AUTH ROUTES
'''
@APP.route("/auth/login/v2", methods = ['POST'])
def auth_login_server():
    data = request.get_json()
    email = data['email']
    password = data['password']
    result = auth_login_v2(email, password)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps(result), 200

@APP.route("/auth/register/v2", methods = ['POST'])
def auth_register_server():
    data = request.get_json()
    email = data['email']
    password = data['password']
    name_first = data['name_first']
    name_last = data['name_last']
    result = auth_register_v2(email, password, name_first, name_last)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps(result), 200

@APP.route("/auth/logout/v1", methods = ['POST'])
def auth_logout_server():
    data = request.get_json()
    token = data['token']
    result = auth_logout_v1(token)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps(result), 200

@APP.route("/auth/passwordreset/request/v1", methods = ['POST'])
def auth_passwordreset_request_server():
    data = request.get_json()
    email = data['email']
    reset_code = auth_passwordreset_request_v1(email)
    if (reset_code != ''):
        compose_email(email, reset_code)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps({}), 200

@APP.route("/auth/passwordreset/reset/v1", methods = ['POST'])
def auth_passwordreset_reset_server():
    data = request.get_json()
    reset_code = data['reset_code']
    new_password = data['new_password']
    auth_passwordreset_reset_v1(reset_code, new_password)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps({}), 200


'''
USER/PROFILE ROUTES
'''
@APP.route("/user/profile/v1", methods = ['GET'])
def user_profile_server():
    token = request.args.get('token')
    u_id = request.args.get('u_id')
    response = user_profile_v1(token, u_id)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps(response), 200

@APP.route("/user/profile/setname/v1", methods = ['PUT'])
def user_profile_setname_server():
    data = request.get_json()
    token = data['token']
    name_first = data['name_first']
    name_last = data['name_last']
    response = user_profile_setname_v1(token, name_first, name_last)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps(response), 200

@APP.route("/user/profile/setemail/v1", methods = ['PUT'])
def user_profile_setemail_server():
    data = request.get_json()
    token = data['token']
    email = data['email']
    response = user_profile_setemail_v1(token, email)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps(response), 200

@APP.route("/user/profile/sethandle/v1", methods = ['PUT'])
def user_profile_sethandle_server():
    data = request.get_json()
    token = data['token']
    handle_str = data['handle_str']
    response = user_profile_sethandle_v1(token, handle_str)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps(response), 200


'''
CLEAR ROUTE
'''

@APP.route("/clear/v1", methods=['DELETE'])
def clear():
    clear_v1()
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps({})


'''
CHANNELS ROUTES
'''

@APP.route("/channels/list/v2", methods=['GET'])
def list_channels():
    token = request.args.get('token')
    result = channels_list_v2(token)
    return dumps(result), 200

@APP.route("/channels/create/v2", methods=['POST'])
def create_channel():
    request_data = request.get_json()
    token = request_data['token']
    name = request_data['name']
    is_public = request_data['is_public']
    result = channels_create_v2(token, name, is_public)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps(result), 200

@APP.route('/channels/listall/v2', methods=['GET'])
def channels_listsll():
    token = request.args.get('token')
    response = channels_listall_v2(token)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps(response)

'''
CHANNEL ROUTES
'''

@APP.route("/channel/join/v2", methods = ['POST'])
def join_channel():
    request_data = request.get_json()
    token = request_data['token']
    channel = request_data['channel_id']
    channel_join_v2(token, channel)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps ({}), 200

@APP.route("/channel/invite/v2", methods = ['POST'])
def invite_channel():
    request_data = request.get_json()
    token = request_data['token']
    channel = request_data['channel_id']
    user = request_data['u_id']
    channel_invite_v2(token, channel, user)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps ({}), 200

@APP.route("/channel/leave/v1", methods = ['POST'])
def leave_channel():
    request_data = request.get_json()
    token = request_data['token']
    channel = request_data['channel_id']
    channel_leave_v1(token, channel)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps ({}), 200

@APP.route("/channel/addowner/v1", methods = ['POST'])
def add_owner():
    request_data = request.get_json()
    token = request_data['token']
    channel = request_data['channel_id']
    user = request_data['u_id']
    channel_add_owner_v1(token, channel, user)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps ({}), 200

@APP.route("/channel/removeowner/v1", methods = ['POST'])
def remove_owner():
    request_data = request.get_json()
    token = request_data['token']
    channel = request_data['channel_id']
    user = request_data['u_id']
    channel_remove_owner_v1(token, channel, user)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps ({}), 200

@APP.route('/channel/details/v2', methods=['GET'])
def channel_details():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    response = channel_details_v2(token, channel_id)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps(response)


'''
DM ROUTES
'''

@APP.route("/dm/details/v1", methods=['GET'])
def dm_details():
    token = request.args.get('token')
    dm_id = request.args.get('dm_id')
    response = dm_details_v1(token, dm_id)
    return dumps(response)

@APP.route("/dm/leave/v1", methods = ['POST'])
def leave_dm():
    request_data = request.get_json()
    token = request_data['token']
    dm = request_data['dm_id']
    result = dm_leave_v1(token, dm)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps (result), 200 

@APP.route("/dm/remove/v1", methods = ['DELETE'])
def remove_dm():
    request_data = request.get_json()
    token = request_data['token']
    dm = request_data['dm_id']
    dm_remove_v1(token, dm)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps ({}), 200 

@APP.route("/dm/create/v1", methods=['POST'])
def create_dm():
    request_data = request.get_json()
    token = request_data['token']
    u_ids = request_data['u_ids']
    result = dm_create_v1(token, u_ids)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps(result)

@APP.route("/dm/list/v1", methods=['GET'])
def get_list():
    token = request.args.get('token')
    result = dm_list_v1(token)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps(result)

'''
MESSAGE ROUTES
'''

@APP.route("/channel/messages/v2", methods=['GET'])
def channel_messages():
    check_sendlater()
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    start = request.args.get('start')
    result = channel_messages_v2(token, channel_id, start)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps(result)

@APP.route("/dm/messages/v1", methods=['GET'])
def dm_messages():
    check_sendlater()
    token = request.args.get('token')
    dm_id = request.args.get('dm_id')
    start = request.args.get('start') 
    dm_messages_v1(token, dm_id, start)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps(dm_messages_v1(token, dm_id, start))

@APP.route("/message/send/v1", methods=['POST'])
def message_send():
    check_sendlater()
    request_data = request.get_json()
    token = request_data['token']
    channel_id = request_data['channel_id']
    message = request_data['message']
    result = message_send_v1(token, channel_id, message)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps(result)

@APP.route("/message/senddm/v1", methods=['POST'])
def dm_message_send():
    check_sendlater()
    request_data = request.get_json()
    token = request_data['token']
    dm_id = request_data['dm_id']
    message = request_data['message']
    output = message_senddm_v1(token, dm_id, message)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps(output)

@APP.route("/message/edit/v1", methods=['PUT'])
def message_edit():
    check_sendlater()
    request_data = request.get_json()
    token = request_data['token']
    message_id = request_data['message_id']
    message = request_data['message']
    message_edit_v1(token, message_id, message)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps({})

@APP.route("/message/remove/v1", methods=['DELETE'])
def message_remove():
    check_sendlater()
    request_data = request.get_json()
    token = request_data['token']
    message_id = request_data['message_id']
    message_remove_v1(token, message_id)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps({})

@APP.route("/message/react/v1", methods=['POST'])
def message_react():
    check_sendlater()
    request_data = request.get_json()
    token = request_data['token']
    message_id = request_data['message_id']
    react_id = request_data['react_id']
    message_react_v1(token, message_id, react_id)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps({})

@APP.route("/message/unreact/v1", methods=['POST'])
def message_unreact():
    check_sendlater()
    request_data = request.get_json()
    token = request_data['token']
    message_id = request_data['message_id']
    react_id = request_data['react_id']
    message_unreact_v1(token, message_id, react_id)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps({})

@APP.route("/message/pin/v1", methods=['POST'])
def message_pin():
    check_sendlater()
    request_data = request.get_json()
    token = request_data['token']
    message_id = request_data['message_id']
    message_pin_v1(token, message_id)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps({})

@APP.route("/message/unpin/v1", methods=['POST'])
def message_unpin():
    check_sendlater()
    request_data = request.get_json()
    token = request_data['token']
    message_id = request_data['message_id']
    message_unpin_v1(token, message_id)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps({})

@APP.route("/message/sendlater/v1", methods=['POST'])
def message_sendlater():
    check_sendlater()
    request_data = request.get_json()
    token = request_data['token']
    channel_id = request_data['channel_id']
    message = request_data['message']
    time_sent = request_data['time_sent']
    message_id = message_sendlater_v1(token, channel_id, message, time_sent)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps(message_id)

@APP.route("/message/sendlaterdm/v1", methods=['POST'])
def message_sendlaterdm():
    check_sendlater()
    request_data = request.get_json()
    token = request_data['token']
    dm_id = request_data['dm_id']
    message = request_data['message']
    time_sent = request_data['time_sent']
    message_id = message_sendlaterdm_v1(token, dm_id, message, time_sent)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps(message_id)

@APP.route("/message/share/v1", methods=['POST'])
def message_share():
    check_sendlater()
    request_data = request.get_json()
    token = request_data['token']
    og_message_id = request_data['og_message_id']
    message = request_data['message']
    channel_id = request_data['channel_id']
    dm_id = request_data['dm_id']
    response = message_share_v1(token, og_message_id, message, channel_id, dm_id)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps(response)


'''
ADMIN ROUTES
'''

@APP.route("/admin/user/remove/v1", methods = ['DELETE'])
def remove_user():
    request_data = request.get_json()
    token = request_data['token']
    u_id = request_data['u_id']
    admin_remove_user_v1(token, u_id)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps({})

@APP.route("/admin/userpermission/change/v1", methods=['POST'])
def permission_change():
    request_data = request.get_json()
    token = request_data['token']
    u_id = request_data['u_id']
    permission_id = request_data['permission_id']
    response = admin_change_user_perms_v1(token, u_id, permission_id)
    with open('export.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps(response)

'''
USER ROUTES
'''
@APP.route("/users/all/v1", methods=['GET'])
def users_all():
    token = request.args.get('token')
    response = users_all_v1(token)
    return dumps(response)

'''
OTHER ROUTES
'''
@APP.route("/notifications/get/v1", methods=['GET'])
def notification_get():
    check_sendlater()
    token = request.args.get('token')
    response = notifications_get_v1(token)
    return dumps(response)

@APP.route("/search/v1", methods=['GET'])
def search():
    check_sendlater()
    token = request.args.get('token')
    query_str = request.args.get('query_str')
    response = search_v1(token, query_str)
    return dumps(response)



#### NO NEED TO MODIFY BELOW THIS POINT



if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port

