import random
import math
while True:
    divide = random.randint(0, 1000)
    randomNumber = random.randint(0, 1000)
    print('#####')
    print('Divide: ' + str(divide) + '\nBy: ' + str(randomNumber))
    try:
        dividend = math.floor(int(divide) / int(randomNumber))
    except ZeroDivisionError:
        print('Error: Cannot divide by 0')
        input("Press Enter to continue...")

    remainder = int(divide) - (dividend * randomNumber)
    print('Output: ' + str(dividend * randomNumber) + ' ' + str(remainder))
    print('#####')
