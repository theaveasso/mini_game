##### Hangman Game

import random as rnd
import sys, time, os

def welcome(text):
    for line in text:
        sys.stdout.write(line)
        sys.stdout.flush()
        time.sleep(.1)
    print('')

    time.sleep(.2)
    os.system('cls || clear')

def pick_rnd_word(words):
    return rnd.choice(words)

welcome('Welcome to Hangman!\nLet\'s Play!!!')

# random select a word
words = 'ant baboon badger bat bear beaver camel cat clam cobra cougar\
       coyote crow deer dog donkey duck eagle ferret fox frog goat goose hawk\
       lion lizard llama mole monkey moose mouse mule newt otter owl panda\
       parrot pigeon python rabbit ram rat raven rhino salmon seal shark sheep\
       skunk sloth snake spider stork swan tiger toad trout turkey turtle\
       weasel whale wolf wombat zebra'.split()

secret_word = pick_rnd_word(words)


# set the live 
live = len(secret_word) - 3
if live <=2  : live = 3
print(f'Remain guess: {live}')

# generate the dash visual for player
dash = '_' * len(secret_word)
print(dash)


# asking player for the input
while live > 0:
    guessing = input('Guessing the letters\n')

    # if guessing the right answer add char to the dash
    for i in range(len(secret_word)):
        if guessing in secret_word[i]:
            dash = dash[:i] + secret_word[i] + dash[i+1:]


    if guessing not in secret_word:
        live -= 1
        print(f'Remain guess: {live}')
   
    # showing the word
    for letter in dash:
        print(letter, end=' ')
    print()

    if live == 0:
        print('GAME OVER!')
        time.sleep(.2)
        break

    elif '_' not in dash:
        print('HORRAY, YOU WIN!')
        time.sleep(.2)
        break
    
    