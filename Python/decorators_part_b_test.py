from decorators_part_b import show_weather_v2, hello_v2, show_weather_v3, hello_v3

# The pylint ignores are just to stop VSCode linters from showing errors
# - you don't have to run pylint on your code at all :)

def test_show_weather_v2():
    # pylint: disable=no-value-for-parameter
    assert show_weather_v2('raining') == 'hi! Today, the weather is raining'
    assert show_weather_v2('sunny') == 'hi! Today, the weather is sunny'

def test_hello_v2():
    # pylint: disable=no-value-for-parameter
    assert hello_v2() == 'Hello hi!!!'

def test_show_weather_v3():
    # pylint: disable=no-value-for-parameter
    assert show_weather_v3('rain') == 'COMP1531!!! Today, the weather is looking like rain'
    assert show_weather_v3('hail and thunder') == 'COMP1531!!! Today, the weather is looking like hail and thunder'

def test_hello_v3():
    # pylint: disable=no-value-for-parameter
    assert hello_v3() == 'Hello hi!!!'
