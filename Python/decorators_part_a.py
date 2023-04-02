def suffix_message(function):
    def wrapper(*args, **kwargs):
        length = len(args)
        suffix = ", Suffix: "
        if length == 1:
            return function(args[0]) + suffix + args[0]
        elif length == 0:
            return function()
        else:
            return function(args[0], args[1]) + suffix + args[0]
    return wrapper

@suffix_message
def greet(person, greeting):
    return f'Hello {person}! {greeting}'

@suffix_message
def show_weather(weather):
    return 'The weather is ' + weather + ' today'

@suffix_message
def hello():
    return 'Hello'

@suffix_message
def side_effects_only(message):
    print(f'{message}! This function only has side effects.')
