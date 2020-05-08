import re

# NIST guidelines:
# Minimum of 8 characters
# Ability to use all special characters but no special requirement to use them
# Restrict sequential and repetitive characters (Ex: 1234, aaaaaaa)
# Restrict context-specific passwords (Ex: Name of the site, name of the user)
# Restrict common passwords and dictionary words
# Restrict passwords from previous breach corpuses


def checkPassword(password):
    # Define the rules
    offending = []

    def not_eight_chars(string):
        if len(string) >= 8:
            return None
        else:
            return "Must be 8 characters"

    def sequential(string):
        for i in range(0, len(string) - 2):
            char = ord(string[i])
            char2 = ord(string[i + 1])
            char3 = ord(string[i + 2])
            # Test for positive sequential
            if char + 1 == char2 and char2 + 1 == char3:
                reason = chr(char) + chr(char2) + chr(char3)
                return 'Password must not contain any sequential characters: (' + reason + ')'
            # Test for negative sequential
            if char - 1 == char2 and char2 - 1 == char3:
                reason = chr(char) + chr(char2) + chr(char3)
                return 'Password must not contain any sequential characters: (' + reason + ')'
        return None

    def repeating(string):
        for i in range(0, len(string) - 2):
            char = ord(string[i])
            char2 = ord(string[i + 1])
            char3 = ord(string[i + 2])
            # Test for positive sequential
            if char == char2 and char2 == char3:
                reason = chr(char) + chr(char2) + chr(char3)
                return 'Password must not contain any repeating characters: (' + reason + ')'
        return None

    def dictionary(string):
        english_words = open('english_words.txt', 'r')
        for word in english_words:
            if word.upper().strip() == string.upper().strip():
                return 'Password must not be a dictionary word: ' + word.strip()
        return None

    def cracked(string):
        cracked_passwords = open('10-million-password-list-top-1000000.txt', 'r')
        for passwd in cracked_passwords:
            if passwd.upper().strip() == string.upper().strip():
                return 'Password has been previously compromised: ' + passwd.strip()
        return None
    # Set error flag to false.
    flag = False

    #Test for eight characters
    description = not_eight_chars(password)
    if description is not None:
        flag = True
        offending.append(description)
    description = sequential(password)
    if description is not None:
        flag = True
        offending.append(description)

    description = repeating(password)
    if description is not None:
        flag = True
        offending.append(description)

    description = dictionary(password)
    if description is not None:
        flag = True
        offending.append(description)

    description = cracked(password)
    if description is not None:
        flag = True
        offending.append(description)

    if flag:
        print('Password does not meet NIST requirements:')
        for reason in offending:
            print('\t' + reason)
    else:
        print('Password passes')


while True:
    checkPassword(input('Enter a password: '))