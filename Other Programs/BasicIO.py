def check_name(my_name):
    while True:
        print('Your name is ' + str(len(my_name)) + ' characters long')
        if len(my_name) >= 10:
            print('Why is your name so long? would you mind shortening it?')
        elif len(my_name) <= 2:
            print('Why is your name so short? would you mind making it a little longer?')
        else:
            print('Thank you for having a short name.')
            break
        my_name = input('Please type your name: ')
    print('Your name, ' + my_name + ', seems okay')


check_name(input('Please type your name: '))
