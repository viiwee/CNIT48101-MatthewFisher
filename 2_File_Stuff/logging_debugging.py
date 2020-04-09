# This file contains three different programs
#   The first is a coin toss program to demonstrate logging under normal circumstances
#   The second is a math program to demonstrate critical errors in a try/catch scenario
#   The third is a regex program to search through the log file and find all the critical errors

#################################################
# Coin Toss
#################################################
import random
import logging
import inspect

logging.basicConfig(filename='logging_debugging.log', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of program')

guess = ''
while guess not in ('heads', 'tails'):
    logging.debug('Start of user input')
    print('Guess the coin toss! Enter heads or tails:')
    guess = input()
    logging.debug('Received input: ' + guess)

toss = random.randint(0, 1)  # 0 is tails, 1 is heads
logging.debug('Toss is: ' + str(toss))

logging.debug('Checking if toss = guess: ' +
              str(type(toss)) + ':' + str(toss) + ' = ' +
              str(type(guess)) + ':' + guess)
if toss == guess:  # Error here is that you are comparing an int (1 or 0) to a string (heads or tails)
    print('You got it!')
else:
    print('Nope! Guess again!')
    guesss = input()  # Error here is a misspelled variable

    logging.debug('Checking if toss = guess: ' +
                  str(type(toss)) + ':' + str(toss) + ' = ' +
                  str(type(guess)) + ':' + guess)
    if toss == guess:  # Error here is that you are comparing an int (1 or 0) to a string (heads or tails)
        print('You got it!')
    else:
        print('Nope. You are really bad at this game.')
logging.debug('End of program')

#################################################
# Math
#################################################
import math


def curline():
    return inspect.currentframe().f_back.f_lineno


logging.debug('Start of Math program')
for x in range(1, 1000):
    divide = random.randint(0, 1000)
    randomNumber = random.randint(0, 300)
    logging.debug('Divide: ' + str(divide) + ' By: ' + str(randomNumber))
    try:
        dividend = math.floor(int(divide) / int(randomNumber))
    except ZeroDivisionError:
        logging.critical('Line ' + str(curline()) + ': Error dividing ' + str(divide) + ' by ' + str(randomNumber) + '. Cannot divide by 0.')

#################################################
# Regex Search the Log
#################################################
import re


logfile = open('logging_debugging.log')


def check_critical(text):
    critical_format = re.compile('^.+- CRITICAL -.+$')
    if critical_format.match(text) is not None:
        print(text)


for line in logfile.readlines():
    check_critical(line)

