import hashlib
word_list = ['sidewalk', 'planes', 'are', 'cool', 'how', 'many', 'words', 'should', 'I', 'put', 'in', 'here']


def generate_hash_list(words):
    hashes = {}
    for word in words:
        hash_object = hashlib.sha256(word.encode())
        hashes[word] = hash_object.hexdigest()
    return hashes


def check_hashes(plaintext_word_list):
    hashed_password = input('Enter a SHA256 hash of a password: ')
    # hashed_password = hashlib.sha256(plaintext_password.encode()).hexdigest()
    hash_dict = generate_hash_list(word_list)
    for check_hash in hash_dict.keys():
        # print(check_hash)
        # print(hash_dict.get(check_hash))
        if hash_dict.get(check_hash) == hashed_password:
            print('The password entered was: ' + check_hash)


check_hashes(word_list)




