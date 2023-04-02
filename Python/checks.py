# from src.data_store import data_store
# import re

# '''
# A file containing all the check functions that are used across multiple
# functions in 
# '''

# '''
# AUTH Checks
# '''
# def check_email_valid(email):
#     '''
#     Check email is actually an email
#     Parameters: email as string
#     Return: Boolean True if a match is found, False if otherwise
#     '''
#     regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
#     if(re.fullmatch(regex, email)):
#         return True
#     else:
#         return False


# def check_password_length(password):
#     '''
#     Check password is of valid length
#     Parameters: password as string
#     Return: Boolean True if a condtions are met, False if otherwise
#     '''
#     if(len(password) < 6):
#         return False
#     else:
#         return True


# def check_name_length(name):
#     '''
#     Checks that the length of a name is between 1 and 50 characters inclusive
#     Parameters: name as string
#     Return: Boolean True if a condtions are met, False if otherwise
#     '''
#     if(len(name) >= 1 and len(name) <= 50):
#         return True
#     else:
#         return False


# def check_email_registered(email):
#     '''
#     Checks if email is registered, used by both login and register functions
#     Parameters: name as string
#     Return: Boolean True if a condtions are met, False if otherwise
#     '''
#     user = data_store.get()['users']
    
#     #iterates through data store looking for an id with matching email, 
#     #breaks if matching email is found or counter excedes list length
#     i = 0
#     while(i < len(data_store.get()['users']) and email != user[i]["email"]):
#        i = i + 1
    
#     #checks if previous while loop broke from matching email or from exceeding list length
#     if (i < len(data_store.get()['users'])):
#         return True
#     else:
#         return False


# '''
# CHANNEL Checks
# '''
# def check_valid_channel(channel_id):
#     '''
#     Helper function specifically for message implementation
#     Checks if the channel is valid then outputs the channel id if it is
#     '''
#     channels = data_store.get()['channels']
    
#     for channel in channels:
#         if (channel['channel_id'] == channel_id):
#             return channel 

#     return False

# def check_start_val(info, channel_id, start):
#     '''
#     Helper function specifically for message implementation
#     Checks if the start value inputted refers to an actual message
#     If not returns False
#     If it does either returns -1 if all the messages are to be displayed or
#     it returns the start value plus 50
#     '''
#     # Finds total number of messages
#     result = check_valid_channel(channel_id)
#     messages_list = result['messages']
#     num_messages = len(messages_list)

#     # Checks if start value sits in range
#     if start < 0 :
#         return False
#     elif start > num_messages :
#         return False
#     elif ((num_messages - start) < 50):
#         return -1
#     else:
#         return (start + 50)


# '''
# CHANNELS Checks
# '''
# def check_channel_name_length(string):
#     '''
#     Checks that the length of a name is between 1 and 20 characters inclusive
#     Parameters: name as string
#     Return: Int 0 if a condtions are met, 1 if otherwise
#     '''
#     length = len(string)
#     return False if length >= 1 and length <= 20 else True


