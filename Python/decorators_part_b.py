# TODO: Create the prefix_with decorator generator
def prefix_with(argument):
    pass

###
# Do not edit functions below
###

def say_hi():
    return 'hi'


@prefix_with(say_hi)
def show_weather_v2(message, weather):
    return f'{message}! Today, the weather is {weather}'


@prefix_with(say_hi)
def hello_v2(message):
    return f'Hello {message}!!!'

@prefix_with('COMP1531')
def show_weather_v3(message, weather):
    return f'{message}!!! Today, the weather is looking like {weather}'

@prefix_with("hi")
def hello_v3(message):
    return f'Hello {message}!!!'
