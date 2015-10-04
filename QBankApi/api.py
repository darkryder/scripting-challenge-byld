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


# Question statement
# To be written.
