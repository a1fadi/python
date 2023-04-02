'''
The flask server wrapper

All endpoints return JSON as output.
All POST requests pass parameters through JSON instead of Form.
'''
from json import dumps
from flask import Flask, request

from brooms import get_users, add_user, get_messages, send_message, clear

APP = Flask(__name__)

'''
Endpoint: '/users'
Method: GET
Parameters: ()
Output: { "users": [ ... list of strings ... ] }

Returns a list of all the users as a list of strings.
'''
@APP.route("/users", methods = ['GET'])
def users_get():
    response = get_users()
    return dumps(response), 200

'''
Endpoint: '/users'
Method: POST
Parameters: ( name: string )
Output: {}

Adds a user to the room/broom.
'''
@APP.route("/users", methods=['POST'])
def user_add():
    request_data = request.get_json()
    name = request_data['name']
    add_user(name)
    return dumps({}), 200 

'''
Endpoint: '/message'
Method: GET
Parameters: ()
Output: { "messages": [ { "from" : string, "to" : string, "message" : string } ] }

Returns a list of all the messages sent, who they came from, and who they are going to.
'''

@APP.route("/message", methods = ['GET'])
def message_get():
    response = get_messages()
    return dumps(response), 200

'''
Endpoint: '/message'
Method: POST
Parameters: (user_from: string, user_to: string, message: string)
Output: {}

Sends a message from user "user_from" to user "user_to". All three parameters are strings.
'''
@APP.route("/message", methods=['POST'])
def message_add():
    request_data = request.get_json()
    user_from = request_data['user_from']
    user_to = request_data['user_to']
    message = request_data['message']
    send_message(user_from, user_to, message)
    return dumps({}), 200 

@APP.route("/clear", methods=['DELETE'])
def clear_ting():
    clear()
    return dumps({}), 200 


if __name__ == '__main__':
    # If you are running on VLAB and there is a port in use error,
    # you may need to change the port from 8080 to something else.
    #
    # REMEMBER TO SET THE PORT BACK TO 8080 BEFORE SUBMITTING!
    #
    APP.run(debug=True, port=8021)
