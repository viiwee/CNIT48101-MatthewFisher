import sys
import pyperclip
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

passwords = {}
debug = False
# The master password in password123


def make_dictionary():
    file = open('passwords.txt', 'r')
    for line in file:
        account, password = line.split(':')
        passwords[account] = password.strip()
    if debug:
        print(passwords)


def get_password(account, master_password):
    key = SHA256.new((master_password.encode())).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    if debug:
        print(key)
        print(master_password)
    if account in passwords:
        try:
            pyperclip.copy(cipher.decrypt(base64.b64decode(passwords[account])).decode())
        except UnicodeDecodeError:
            print('Incorrect master password, try again.')
            return
        print('Password for ' + account + 'copied to clipboard.')
    else:
        print('No account named ' + account)


def set_password(account, password, master_password):
    if account in passwords:
        print('Account "' + account + '" already exists.')
        if account != 'master':
            return
    if account == 'master':
        print('Not finished')
        key = SHA256.new((password.encode())).digest()

        # create a hash of the hash that is used to decode passwords. Store that double hash. At beginning of program,
        # check if the master key is correct by double hashing the master key they inputted
    else:
        key = SHA256.new((master_password.encode())).digest()
        cipher = AES.new(key, AES.MODE_ECB)
        file = open('passwords.txt', 'a')
        if debug:
            print(base64.b64encode(cipher.encrypt(password.encode())).decode())
        encoded = base64.b64encode(cipher.encrypt(password.encode())).decode()
        file.write(account + ':' + encoded + '\n')


def get_command(command):
    if len(sys.argv) < 3:
        print('Usage: \npassword_locker.py get <account>\n' +
              'password_locker.py set <account> <password>')
        sys.exit()
    if command == 'get':
        get_password(sys.argv[2], sys.argv[3])
        return
    if command == 'set':
        if debug:
            print('ARGV SIZE: ' + str(len(sys.argv)))
        if len(sys.argv) == 5:
            set_password(sys.argv[2], sys.argv[3], sys.argv[4])
        else:
            print("Incorrect number of args")
        return
    print('Command: "' + command + '" not found.')


make_dictionary()
get_command(sys.argv[1])


