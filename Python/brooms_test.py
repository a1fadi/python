'''
Tests
'''
from brooms import send_message, get_messages, clear, get_users, add_user
import pytest

def test_simple():
    clear()
    add_user("Jake")
    assert(get_users() == {"users":["Jake"]})
    add_user("Hayden")
    assert(get_users() == {"users":["Hayden", "Jake"]})
    send_message("Jake", "Hayden", "Hello!")
    send_message("Jake", "Hayden", "Goodbye!")
    assert get_messages() == {
        "messages": [
            {"from": "Jake", "to": "Hayden", "message": "Hello!"},
            {"from": "Jake", "to": "Hayden", "message": "Goodbye!"},
        ]
    }

def test_clear():
    clear()
    add_user("Jake")
    assert(get_users() == {"users":["Jake"]})
    add_user("Hayden")
    send_message("Jake", "Hayden", "Hello!")
    send_message("Jake", "Hayden", "Goodbye!")
    assert(clear() == {})

def test_add_user_same_name():
    clear()
    add_user("Jake")
    with pytest.raises(KeyError):
        add_user("Jake")

def test_lots_users():
    clear()
    add_user("Jake")
    add_user("Hayden")
    add_user("Fadi")
    add_user("Fadi1")
    assert(get_users() == {"users":["Fadi1","Fadi","Hayden", "Jake"]})

def test_messages():
    clear()
    add_user("Fadi")
    add_user("Hayden")
    send_message("Fadi", "Hayden", "He!")
    send_message("Fadi", "Hayden", "Goo")
    assert get_messages() == {
        "messages": [
            {"from": "Fadi", "to": "Hayden", "message": "He!"},
            {"from": "Fadi", "to": "Hayden", "message": "Goo"},
        ]
    }

def test_messages_invalid1():
    clear()
    add_user("Fadi")
    with pytest.raises(KeyError):
        send_message("Fadi", "Hayden", "He!")

def test_messages_invalid2():
    clear()
    add_user("Fadi")
    with pytest.raises(KeyError):
        send_message("Tim", "Fadi", "He!")

