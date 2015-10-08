if __name__ == "__main__":
    raise Exception ("This file should not be run from the interpreter."
        "Instead open up django's shell and call the run method.")

from hashlib import md5
from django.template.loader import render_to_string

SALT = "Wohatbewu2nveh3@t3"

def run():
    for iteration in xrange(269):
        current = md5()
        current.update(SALT + str(iteration))
        current = current.hexdigest()

        fresh = md5()
        fresh.update(SALT + str(iteration + 1))
        fresh = fresh.hexdigest()

        print (iteration, current, fresh)

        template = render_to_string("QKeepRunning_template.html", {'next': fresh})
        with open('QKeepRunning/' + current + '.html', 'w') as f:
            f.write(template)

    print "Done"

# Serve this folder directly from nginx.
