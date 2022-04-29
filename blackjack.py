## Blackjack ## 21 Card game

import random as rnd
import os, time, sys

#### Initialize
# initialize cards
cards = [11,2,3,4,5,6,7,8,9,10,10,10,10]

#How much you want to bet?'))

## draw a card
def draw_cards(n,player):
    for i in range(n):
        player.append(rnd.choice(cards))
    return player

# draw a card
def show_dealer_card(com_cards):
    print(f'The dealler\'s card is {com_cards[0]}')

# show card to the UI
def show_player(players):
    print(f'Your cards is {players}')


# ask the player (Hit or stand)
def hit_or_stand(p_cards,c_cards):
    while sum(p_cards) < 21:
        show_player(p_cards)
        show_dealer_card(c_cards)
        hos = input('[Hit] (add one more card) or [Stand](keep what you have):  ')

        if hos == 'hit':
            draw_cards(1, p_cards)
        else: 
            break
        show_player(p_cards)


def draw_more_card_to_com(c_cards):
    if sum(c_cards) < 17:
        draw_cards(1, c_cards)

def check_winner(p_cards, c_cards):
    p = sum(p_cards)
    c = sum(c_cards)
    if p == c: print('You and the dealer have the same amount of number!')
    elif p > 21 : print('Oop, You lose!')
    elif p > c or c > 21 : print('Horray! You Win!')
    else: print('Oop, Your cards is smaller than the dealer!')

# blackjack rules
def blackjack():
    isTrue = True
    while isTrue:

        p = []
        c = []
        player_cards = draw_cards(2, p)
        com_cards = draw_cards(2, c)

        hit_or_stand(player_cards, com_cards)

        draw_more_card_to_com(com_cards)

        check_winner(player_cards, com_cards)
        print(f'The dealer cards is {com_cards}')


        con = input('Play again! [Yes] or [No]\n')

        if con  == 'n' or con == 'no':
            isTrue = False


##### Game 
if __name__ == "__main__":
    blackjack()
