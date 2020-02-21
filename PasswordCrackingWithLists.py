invalidPasswords = ['password', 'abc', 'test']
passwordExtensions = ['1', '12', '123', '!', '@']
invalidArray = []
passwordList = []

while True:
    nextPassword = input('Type the passwords you want to check, pressing enter after each: ')
    if nextPassword == '':
        break
    passwordList.append(nextPassword)


def generate_invalid_list():
    global invalidArray
    for i in range(0, len(invalidPasswords)):
        invalidArray.append(invalidPasswords[i])  # Add each plain invalid password to the list
        for j in range(0, len(passwordExtensions)):
            invalidArray.append(invalidPasswords[i]+passwordExtensions[j])  # Add each invalid password with
            # extensions to the list


def check_passwords(check_list):
    global invalidArray
    for i in range(0, len(check_list)):
        for j in range(0, len(invalidArray)):
            if invalidArray[j] == check_list[i]:
                new_password = input('Please pick a different password instead of "' + check_list[i] + '": ')
                check_list[i] = new_password


generate_invalid_list()
check_passwords(passwordList)
