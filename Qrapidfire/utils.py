from __future__ import division

__author__ = 'darkryder (sambhav13085@iiitd.ac.in)'

from math import sqrt, ceil
from random import shuffle, choice

_rbool = lambda: choice([True, False])

def gcd(*args):
    a, b = args
    a, b = max(a, b), min(a, b)
    while a % b != 0 and b != 1:
        a, b = b, a % b
    return b

def number_of_factors(number):
    count = 0
    for i in xrange(1, int(sqrt(number)) + 1): # not including sqrt
        if number % i == 0:
            count += 2
    if sqrt(number) == int(sqrt(number)): count -= 1
    return count

def math_equation_QA_generator(*args):
    _ARGS_LENGTH = 12
    args = args[0]
    assert len(args) == _ARGS_LENGTH
    assert 0 not in args
    operators = ['+', '-', '/', '*']
    args = list(args)
    shuffle(args)

    # QUESTION = "%d %s %d %s %d %s %d %s %d %s %d %s %d %s %d"
    # only open brackets in the first half of the equation
    QUESTION = []
    opened_brackets_count = 0

    for index, arg in enumerate(args):

        # time to insert a number. Also a bracket can be opened.
        if index <= _ARGS_LENGTH / 2 and _rbool():
            QUESTION.append('(')
            opened_brackets_count += 1
        QUESTION.append(str(arg))

        # time to insert an operator. Also a bracket can be closed.
        if opened_brackets_count > 0 and _rbool():
            QUESTION.append(')')
            opened_brackets_count -= 1
        QUESTION.append(choice(operators))

    QUESTION = QUESTION[:-1]
    for _ in xrange(opened_brackets_count): QUESTION.append(')')

    QUESTION = ''.join(QUESTION)
    ANSWER = int(eval(QUESTION))
    info = ("While evaluating the given equation, understand that 1/2 = 0.5"
        "\nFinally give the int() of the answer.\n")

    return info + "What is the value of " + QUESTION, ANSWER


def gcd_q_generator(*params):
    assert len(params) == 2
    assert 0 not in params
    TEXTS = [
        "What is the gcd of %d and %d",
        "Find the gcd of %d and %d"
        ]
    return choice(TEXTS) % tuple(params)

def number_of_factors_q_generator(*params):
    assert len(params) == 1
    assert 0 not in params
    TEXTS = [
        "Find the number of factors of %d",
        "How many factors are there of %d"
    ]
    return choice(TEXTS) % tuple(params)

def youtube_text_QA_generator():
    mapper = [
        "Gangnam Style",
        "Baby",
        "Blank Space",
        "Dark Horse",
        "Roar",
        "Shake It Off",
        "Bailando",
        "All About That Bass",
        "Uptown Funk",
        "See You Again",
        "Counting Stars",
        "Party Rock Anthem",
        "Love the Way You Lie",
        "Waka Waka (This Time for Africa)",
        "Love the Way You Lie"
    ]

    for i, x in enumerate(mapper):
        yield x, i+1
