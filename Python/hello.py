# pylint: disable=missing-module-docstring
from flask import Flask, request 
from json import dumps 

names = []

APP = Flask(__name__)


@APP.route('/names/add', methods = ['POST'])
def add_name():
    
    request_data = request.get_json()
    name = request_data['name']
    names.append(name)
    return dumps({}), 200 

@APP.route("/names", methods=['GET'])
def get_names():
    names_dic = {
        'names': names
    }
    return dumps(names_dic), 200 


@APP.route("/names/remove", methods=['DELETE'])
def delete_name():
    request_data = request.get_json()
    name = request_data['name']
    for i in names: 
        if i == name:  
            names.remove(name)
            return dumps({}), 200 
        return dumps({}), 400 

@APP.route("/names/clear", methods=['DELETE'])
def delete_name():
    for i in names:  
        names.remove(i)
    #names = []
    return dumps({}), 200 

if __name__ == "__main__":
    APP.run(port=5000)