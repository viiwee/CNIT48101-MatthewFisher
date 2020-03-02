import hashlib

password_dictionary = {}

with open('10-million-password-list-top-1000000.txt') as dictionary:
    for word in dictionary:
        hashed_word = hashlib.sha256(word.strip().encode()).hexdigest()
        password_dictionary[word.strip()] = hashed_word


while True:
    input_password = input('What password would you like to check?: ')
    hashed_password = hashlib.sha256(input_password.encode()).hexdigest()

    for key in password_dictionary:
        #print('Password:' + hashed_password)
        #print('Dictionary: ' + key + ':' + password_dictionary.get(key))
        if hashed_password == password_dictionary.get(key):
            print('Found the password: ' + key + ':' + hashed_password)
            break
