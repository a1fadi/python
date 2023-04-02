from decorators_part_a import show_weather, hello, greet

def test_show_weather():
    assert show_weather('raining') == 'The weather is raining today, Suffix: raining'
    assert show_weather('sunny') == 'The weather is sunny today, Suffix: sunny'

def test_hello():
    assert hello() == 'Hello'

def test_greet():
    assert greet('nick', 'how are you?') == 'Hello nick! how are you?, Suffix: nick'
    assert greet('jake', 'lovely weather today!') == 'Hello jake! lovely weather today!, Suffix: jake'
    assert greet('emily', 'good day for a beach trip') == 'Hello emily! good day for a beach trip, Suffix: emily'
