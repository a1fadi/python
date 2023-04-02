from day_to_message import day_to_message


def test_days_to_message():
    assert(day_to_message('monday') == "It's Monday!")
    assert(day_to_message('Monday') == "It's Monday!")
    assert(day_to_message('Friday') == "Rebecca who?")
    assert(day_to_message('fri') is None)
    assert(day_to_message('') is None)
