import random
###
# Useful methods of the Dictionary type
# keys(): Returns each key
# values(): Returns the values of each key
# items(): Returns the each key and its value
# Cannot be modified, but are useful for loops
# 'name' in player.keys() will check if 'name' is a key that exists in the player dictionary
#     Alternatively: 'name' in player
# player.get('name', 'No name'): Gets the player's name, and returns 'no name' if there is none set
# player.setdefault('name', 'Gerald'): If the 'name'
###

player = {'name': '', 'health': 0, 'attacks': {'stab': 2, 'slash': 3, 'fall': -1}}
enemy = {'name': 'Pi Thon', 'health': 50, 'attacks': {'stab': 2, 'slash': 3, 'fall': -1}}


def to_object_type(obj, set_to):
    #print("Input Type: " + str(type(obj)))
    if isinstance(obj, int):
        try:
            return int(set_to)
        except ValueError:
            raise
    if isinstance(obj, str):
        try:
            return str(set_to)
        except ValueError:
            raise
    if isinstance(obj, list):
        try:
            return list(set_to)
        except ValueError:
            raise
    if isinstance(obj, dict):
        try:
            return dict(set_to)
        except ValueError:
            raise


def set_vars(entity):
    for key in entity.keys():
        if isinstance(entity[key], dict) | isinstance(entity[key], list):
            continue
        while True:
            try:
                entity[key] = to_object_type(entity[key], input('Please set a value for ' + str(key) + ': '))
            except ValueError:
                print("Please enter a different value, you should be entering a: " + str(type(entity[key])))
                continue
            break
        #print("Output type: " + str(type(entity[key])))


def play_game():
    def attack(attacker, victim, move):
        if move in attacker.get('attacks'):
            dmg = attacker.get('attacks').get(move)
            if dmg >= 0:
                victim['health'] = victim['health'] - dmg
                print(attacker['name'] + " dealt " + str(dmg) + " damage to " + victim['name'] + "[" + str(victim['health']) + "]")
            else:
                attacker['health'] = attacker['health'] + dmg
                print(attacker['name'] + "[" + str(attacker['health']) + "]" + " hurt themselves, dealing " + str(dmg) + " damage.")

    def list_moves(attacker):
        print("You can do the following moves: ", end="")
        for move in attacker['attacks'].keys():
            print(str(move) + "(" + str(attacker['attacks'][move]) + " dmg)", end=" | ")
        print()
    set_vars(player)

    def pick_attack(entity):
        return str(random.choice(list(entity['attacks'])))
    while True:
        print(enemy.get('name') + " has " + str(enemy.get('health')) + " health.")
        print(player.get('name') + " has " + str(player.get('health')) + " health.")
        list_moves(player)
        attack(player, enemy, input("What would you like to do: "))
        attack(enemy, player, pick_attack(enemy))
        if player['health'] <= 0:
            break
        if enemy['health'] <= 0:
            break
    print("Game Over.")


while True:
    print("Welcome to dictionary fight, let's begin")
    play_game()







