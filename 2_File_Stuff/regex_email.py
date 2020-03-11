import re


def checkEmail(email):
    format = re.compile('^[\w]+@[\w]+\.[\w]+$')
    if format.match(email) is not None:
        print(email + ' is a valid email.')
    else:
        print(email + ' is not a valid email.')


while True:
    checkEmail(input('Type an email to be checked: '))
