import re


def check_email(email):
    email_format = re.compile('^[\w]+@[\w]+\.[\w]+$')
    if email_format.match(email) is not None:
        print(email + ' is a valid email.')
    else:
        print(email + ' is not a valid email.')


while True:
    check_email(input('Type an email to be checked: '))
