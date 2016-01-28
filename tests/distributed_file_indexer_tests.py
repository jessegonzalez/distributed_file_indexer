from nose.tools import with_setup

from dfi import utils

def setup():
    pass

def teardown():
    pass

@with_setup(setup, teardown)
def test_tokenize():
    input1 = ' one   two three four five '
    input2 = 'one:two:three:four:five'
    input3 = 'one_two_three_four_five'
    input4 = 'one two three four five!'
    input5 = 'don\'t can\'t won\'t?'

    assert utils.tokenize(input1) == ['one', 'two', 'three', 'four', 'five']
    assert utils.tokenize(input2) == ['one', 'two', 'three', 'four', 'five']
    assert utils.tokenize(input3) == ['one', 'two', 'three', 'four', 'five']
    assert utils.tokenize(input4) == ['one', 'two', 'three', 'four', 'five']
    assert utils.tokenize(input5) == ['don', 't', 'can', 't', 'won', 't']

@with_setup(setup, teardown)
def test_counter():
    input1 = "one one two three one"
    input2 = 'don\'t can\'t won\'t?'

    assert utils.counter(input1) == {'one': 3, 'two': 1, 'three': 1}
    assert utils.counter(input2) == {'don': 1, 'can': 1, 'won': 1, 't': 3}


