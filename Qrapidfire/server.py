__author__ = 'darkryder (sambhav13085@iiitd.ac.in)'

# Type of questions:
# 3 levels
#
# 1 level
# What is the gcd of (x, y) where x-> [1, 10^6]; y -> [1, 10^6]
# Number of factors of x where x -> [1, 10^6]
# This is sparta / Answer to life / universe and everything
#
# 2nd level
# Math calculation -> an expression with 8 variables and operators and brackets
#
# 3rd level
# For this following video, what is it's rank on youtube most watched?
# Do you love Byld? [yes]

import SocketServer as SS
from threading import Thread
from time import time as now
from random import choice, randint

from utils import gcd, number_of_factors, math_equation_QA_generator
from utils import gcd_q_generator, number_of_factors_q_generator, youtube_text_QA_generator

PORT = 5021

class Question(object):
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def __repr__(self):
        return "<%s>: %s" % (str(self.question), str(self.answer))

    def verify(self, check):
        return self.answer in [check, check.strip(), check.strip().lower()]

class NaiveMathQuestion(Question):
    def __init__(self, q_maker_func, answer_func, *params):
        question = q_maker_func(*params)
        answer = answer_func(*params)
        super(NaiveMathQuestion, self).__init__(question, answer)

    def verify(self, check):
        try:
            return self.answer == int(check)
        except Exception, e:
            print e
            return False

class MathEquationQuestion(NaiveMathQuestion):
    def __init__(self, *args):
        question, answer = math_equation_QA_generator(*args)
        super(MathEquationQuestion, self).__init__(
            lambda x: question,
            lambda x: answer,
            None
            )

levels_to_questions = {1: [], 2: [], 3:[], 4:[]}

for _ in xrange(1, 25):
    r_ = lambda : randint(100, 10**5)

    q = NaiveMathQuestion(gcd_q_generator, gcd, r_(), r_())
    print "Created Question", q
    levels_to_questions[1].append(q)

    q = NaiveMathQuestion(number_of_factors_q_generator, number_of_factors, r_())
    print "Created Question", q
    levels_to_questions[1].append(q)

    temp_args = lambda l, u, count: [randint(l, u) for _ in xrange(count)]
    q = MathEquationQuestion(temp_args(10, 1000, 8))
    print "Created Question", q
    levels_to_questions[2].append(q)

for song_title, rank in youtube_text_QA_generator():
    q = Question('What is the youtube most watched rank of "%s"' % song_title,
        str(rank))
    print "Created Question", q
    levels_to_questions[3].append(q)

levels_to_questions[1].append(Question("What is the answer to Life, Universe"
    " and Everything?", "42"))
print "Added a spark of life."

levels_to_questions[1].append(Question('What number do you think of when'
    ' you hear "This is Sparta!"', "300"))
print "Added motivation."

levels_to_questions[4].append(Question("Do you love Byld? [yes/no]",
    "yes"))
print "Added some love"

print """
Questions Ready.
Let's Roll.
Server up on port %d
""" % PORT

class QuizMaster(SS.BaseRequestHandler):
    MAX_UPPER_TIME = 5 # seconds
    FLAG = "8b433670258f79578f9a4e5ea388b007"
    def handle(self):
        current_level = 1
        last_request_time = now()
        answer = 'anything'
        print "[%s] Guinea pig connected." % str(self.client_address)

        while len(answer):

            self.request.send("Level %d.\n" % current_level)
            question = choice(levels_to_questions[current_level])
            self.request.send(str(question.question) + '\n')

            answer = self.request.recv(2048)
            diff = now() - last_request_time
            last_request_time = now()
            if diff > QuizMaster.MAX_UPPER_TIME:
                print "[%s] Reply time exceeded: %s" % (str(self.client_address), str(diff))
                self.request.send("Too late.\n")
                break

            if not question.verify(answer):
                print "[%s] Incorrect answer for Question [%s]. Received answer [%s]" % (
                    str(self.client_address), str(question), str(answer))
                self.request.send("Incorrect answer bruh.\n")
                break

            current_level += 1

            if current_level == 5:
                print "[%s] pig escaped." % str(self.client_address)
                self.request.send("You won: [%s]\n" % QuizMaster.FLAG)
                break

        print "[%s] pig died. :(" % str(self.client_address)
        self.request.close()

class ThreadedQuizMaster(SS.ThreadingMixIn, SS.TCPServer):
    pass

ThreadedQuizMaster.allow_reuse_address = True
ThreadedQuizMaster(('0.0.0.0', PORT), QuizMaster).serve_forever()
