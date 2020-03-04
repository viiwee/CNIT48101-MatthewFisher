import sys
import pyperclip
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad

passwords = {}
password_file = 'passwords.txt'
debug = False
block_size = 32


# The master password is MasterPassword123


def make_dictionary():
    file = open(password_file, 'r')
    for line in file:
        account, password = line.split(':')
        passwords[account] = password.strip()
    if debug:
        print(passwords)


def check_master(password):
    key = SHA256.new((password.encode())).digest()  # This is the key that all passwords can be unencrypted with.
    # Don't store it
    key = SHA256.new(key).digest()  # This is the hash of the key that all passwords can be unencrypted with. This
    # can be stored
    key = base64.b64encode(key).decode()
    master = passwords['master']
    if debug:
        print('Key: ' + str(key))
        print('Master: ' + str(master))
    if key == master:
        return
    else:
        print('Incorrect master password. Try again.')
        sys.exit()


def get_password(account, master_password):
    key = SHA256.new((master_password.encode())).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    if debug:
        print(key)
        print(master_password)
    if account in passwords:
        try:
            password = base64.b64decode(passwords[account])
            password = cipher.decrypt(password)
            password = unpad(password, block_size).decode()
            pyperclip.copy(password)
        except UnicodeDecodeError:
            print('Incorrect master password, try again.')
            return
        print('Password for ' + account + 'copied to clipboard.')
    else:
        print('No account named ' + account)


def set_master(account, password):
    if account == 'master':
        key = SHA256.new((password.encode())).digest()  # This is the key that all passwords can be unencrypted with.
        # Don't store it
        key = SHA256.new(key).digest()  # This is the hash of the key that all passwords can be unencrypted with. This
        # can be stored
        key = base64.b64encode(key).decode()

        file = open(password_file, 'w')
        file.write(account + ':' + key + '\n')
        # create a hash of the hash that is used to decode passwords. Store that double hash. At beginning of program,
        # check if the master key is correct by double hashing the master key they inputted
        return


def set_password(account, master_password, password):
    if account in passwords:
        print('Account "' + account + '" already exists. '
                                      '\nIf you are trying to change the master password. Instead use: '
                                      '\npassword_locker.py set master <new_password>')
    elif account not in passwords:
        key = SHA256.new((master_password.encode())).digest()
        cipher = AES.new(key, AES.MODE_ECB)
        file = open(password_file, 'a')
        if debug:
            print('Master_encoded: ' + str(master_password.encode()))
            print('Key: ' + str(key))
            print('Decoded key: ' + str(base64.b64encode(key).decode()))
            encoded_password = pad(password.encode(), block_size)
            print('Padded Encoded password: ' + str(encoded_password))
            encrypted_password = cipher.encrypt(encoded_password)
            print('Encrypted password: ' + str(encrypted_password))
            base64_encrypted_password = base64.b64encode(encrypted_password)
            print('Base64 Encoded, encrypted password: ' + str(base64_encrypted_password))
            decoded_base64_encrypted_password = base64_encrypted_password.decode()
            print('Decoded, base64 encoded, encrypted password: ' + str(decoded_base64_encrypted_password))
            password = decoded_base64_encrypted_password
            file.write(account + ':' + password + '\n')
        else:
            password = pad(password.encode(), block_size)
            password = cipher.encrypt(password)
            password = base64.b64encode(password)
            password = password.decode()
            file.write(account + ':' + password + '\n')
        return


def get_command():
    if len(sys.argv) < 2:
        print('Usage: \npassword_locker.py get <account> <master password>\n' +
              'password_locker.py set <account> <password> <master password>\n')
        sys.exit()
    command = sys.argv[1]
    if debug:
        print('ARGV SIZE: ' + str(len(sys.argv)))
    if command == 'get':
        if len(sys.argv) == 4:
            check_master(sys.argv[3])
            get_password(sys.argv[2], sys.argv[3])
            return
        else:
            print('Usage: \npassword_locker.py get <account> <master password>\n')
            return
    if command == 'set':
        if len(sys.argv) >= 4:
            if len(sys.argv) == 4:
                set_master(sys.argv[2], sys.argv[3])
                return
            if len(sys.argv) == 5:
                check_master(sys.argv[3])
                set_password(sys.argv[2], sys.argv[3], sys.argv[4])
                return
        else:
            print('Usage: password_locker.py set <account> <master password> <password> \n')
            return
    print('Command: "' + command + '" not found.')


make_dictionary()
get_command()

