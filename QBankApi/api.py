if __name__ == "__main__":
    raise Exception ("This file should not be run from the interpreter."
        "Instead open up django's shell and call the run method.")


import SocketServer as SS
from time import sleep

from byld.models import Team, Question
question = Question.objects.filter(title__contains="ATM")
if not len(question) == 1: raise Exception ("ATM Question not added")
question = question[0]

def method(token, amount):
    team = Team.objects.filter(token=token) # catch Exception in upper method
    if len(team) != 1:
        return "Invalid auth token"
    team = team[0]
    if team.ATM_ongoing:
        return ("Awesome! Application logic has "
            "to be threadsafe before they can be run in different threads."
            " FLAG: 08eefddebede4b1508991aef4b9d9477")
    if team.ATM_balance - amount < 0:
        team.ATM_balance = 10**8
        team.save()
        return ("Not enough balance. Resetting your "
            "balance so that you can continue playing. Please retry.")
    team.ATM_ongoing = True
    team.save()
    sleep(2)
    team.ATM_ongoing = False
    team.ATM_balance -= amount
    team.save()
    return 'Removed: ' + str(amount) + '  Balance left: ' + str(team.ATM_balance)


class ATM_Transactioner(SS.BaseRequestHandler):
    def err(self, data):
        print "Received Invalid format: ", data
        self.request.send("Invalid format.\n FORMAT: WITHDRAW [TOKEN] [AMOUNT]\n")


    def handle(self):
        data = "anything"
        print "[%s] Session started." % str(self.client_address)
        while len(data):
            data = self.request.recv(2048)
            if not data: break
            print "[%s] Received: (%s)" % (str(self.client_address), str(data))

            data = data.strip().split(" ")
            if len(data) != 3 or (len(data) == 3 and data[0] != "WITHDRAW"):
                self.err(str(data))
                continue

            _, token, amount = data

            try:
                amount = int(amount)
            except ValueError:
                self.err("AMOUNT -> " + str(amount))
                continue
            if amount < 0:
                self.err("AMOUNT NEGATIVE -> " + str(amount))
                continue

            self.request.send(method(token, amount) + '\n')

        self.request.close()


class ATMServer(SS.ThreadingMixIn, SS.TCPServer):
    """Handle requests in a separate thread."""
ATMServer.allow_reuse_address = True

def run():
    PORT = 6025
    print "Server up on port ", str(PORT)
    ATMServer(('0.0.0.0', PORT), ATM_Transactioner).serve_forever()


PROBLEM_STATEMENT ="""

After a lot of beating, the scrum programmer, Phlegm,
finally told you the basic pseudocode of the method
that runs when you withdraw money from your account.

Eyes gleaming, your friend, Lolum, looks at it greedily,
hungrily. You can see his shoulders getting tense,
brow furrowed, reading through it, trying to find
something exploitable. As you keep an eye out on Phlegm,
Lolum suddenly roars with laughter, and with his hands flying
on the keyboard, you see something miraculous happening.
Money starts pouring out of the ATM, disproportionate to
that being deducted from your account.

Can you exploit this too?



 - withdraw.py

def main():

    ## -- SNIP -- ##

    in = read().strip().split(" ")
    assert len(in) == 3
    assert (in[0] == "WITHDRAW")

    _, key, amount = in

    assert isInt(in[2])

    account = getAccount(key)
    account.amount -= amount

    if not BCryptHashVerify(account, key):
        account += amount
        return send_message_to_atm(ALERT_INVALID)

    else:
        account.save() # commit to db
        return send_message_to_atm(GIVE_MONEY, amount)

    ## -- SNIP -- ##

"""
