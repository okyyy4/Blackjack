"""
    Blackjack created by okyyy4, feel free to use my code and study it.
    As far as I know there are no bugs but I would still appreciate any feedback on my code.
    Thank you and have fun!
"""

import random

# Universal Variables
suits = ('Hearts', 'Spades', 'Clubs', 'Diamonds')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
ranks = ('Two', "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", 'Queen', 'King', 'Ace')
play = True


# Game Classes
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_one(self):
        return self.deck.pop(0)


class Player:
    def __init__(self):
        self.own_hand = []
        self.value_of_hand = 0
        self.ace_count = 0

    def add_card(self, card):
        self.own_hand.append(card)
        self.value_of_hand += values[card.rank]

        if card.rank == 'Ace':
            self.ace_count += 1

    def ace_check(self):
        while self.value_of_hand > 21 and self.ace_count:
            self.value_of_hand -= 10
            self.ace_count -= 1


class Dealer:
    def __init__(self):
        self.name = "Dealer"
        self.own_hand = []
        self.ace_count = 0
        self.value_of_hand = 0

    def add_card(self, card):
        self.own_hand.append(card)
        self.value_of_hand += values[card.rank]

        if card.rank == 'Ace':
            self.ace_count += 1

    def ace_check(self):
        while self.value_of_hand > 21 and self.ace_count:
            self.value_of_hand -= 10
            self.ace_count -= 1


# Game Functions
def hit_or_stay(deck, player):
    global play
    while play:
        to_hit = input("Would you like to hit or stay?: (H or S)")
        if to_hit == 'H':
            player.add_card(deck.deal_one())
            player.ace_check()
            break
        elif to_hit == 'S':
            play = False
            break
        else:
            print("Your input is invalid, try again!")
            continue


def show_initial_hands(player, dealer):
    """Shows hands for first round only"""
    print('\n')
    print("THIS IS DEALER'S HAND")
    print("ONE HIDDEN CARD")
    print(dealer.own_hand[1])
    print('\n')
    print("THIS IS YOUR HAND.")
    for card in player.own_hand:
        print(card)
    print('\n')


def show_hands(player, dealer):
    """Shows hands for all other rounds"""
    print('\n')
    print("THIS IS DEALER'S HAND")
    for card in dealer.own_hand:
        print(card)
    print('\n')
    print("THIS IS YOUR HAND")
    for card in player.own_hand:
        print(card)
    print('\n')


def bet():
    while True:
        try:
            amount_bet = int(input(f"You currently have {player_balance} dollars. How much do you want to bet?:  "))
        except ValueError:
            print("Wrong Input, Try Again.")
            continue
        else:
            return amount_bet


def check_score(player_balance):
    """Returns rank at the end of the game in accordance with final player_balance"""
    if player_balance >= 10000:
        print("You cleaned the house out! Rank: Two Aces ")
    elif 8500 <= player_balance < 10000:
        print("Almost perfect! Rank: Blackjack ")
    elif 7000 <= player_balance < 8500:
        print("Excellent! Rank: Split Aces ")
    elif 6000 <= player_balance < 7000:
        print("Good effort! Rank: Ace-Face ")
    elif 5000 <= player_balance < 6000:
        print("Okay job. Rank: Jack ")
    elif 3000 <= player_balance < 5000:
        print("Poor effort. Rank: Low-roller ")
    elif 1000 <= player_balance < 3000:
        print("Are you even trying? Rank: Bad Trip to Vegas ")
    elif 100 <= player_balance < 1000:
        print("Gambling isn't for you buddy. Rank: Bus Ticket Home")
    elif player_balance <= 0:
        print("Never play again. Rank: Complete Failure ")


# Game Logic
print("Welcome to Blackjack created by okyyy4.")
print("You are free to use any of my code to your heart's content.")
print("Before we begin, this version of Blackjack does not include split, insurance etc. decisions. Only hit and stay.")
print("There is a betting system where both the dealer and player start off with 5000 dollars each.")
print("You will receive a rank corresponding to the amount of money you lose or win at the end of the game.")
print("Have Fun!")
player_balance = 5000
dealer_balance = 5000
game_on = True
while game_on:
    deck = Deck()
    deck.shuffle()
    player = Player()
    dealer = Dealer()
    player.add_card(deck.deal_one())
    player.add_card(deck.deal_one())
    dealer.add_card(deck.deal_one())
    dealer.add_card(deck.deal_one())
    on_the_line = 0
    player_bet = 0
    dealer_bet = 0
    show_initial_hands(player, dealer)
    while play:
        while on_the_line == 0:
            player_bet = bet()
            if player_bet > player_balance:
                player_bet = 0
                print("You have insufficient funds, try again!")
            else:
                dealer_bet = player_bet
                on_the_line += dealer_bet
                on_the_line += player_bet
                player_balance -= player_bet
                dealer_balance -= dealer_bet
                break
        hit_or_stay(deck, player)
        show_initial_hands(player, dealer)
        if player.value_of_hand > 21:
            print("You exceeded 21, you lose!")
            dealer_balance += on_the_line
            break

    if player.value_of_hand <= 21:
        while dealer.value_of_hand < player.value_of_hand:
            dealer.add_card(deck.deal_one())
            dealer.ace_check()
        if dealer.value_of_hand > 21:
            print("Dealer busts, you win!")
            player_balance += on_the_line
            print(player_balance)
            show_hands(player, dealer)
        elif dealer.value_of_hand > player.value_of_hand:
            print("Dealer wins, you lose!")
            dealer_balance += on_the_line
            show_hands(player, dealer)
        elif dealer.value_of_hand < player.value_of_hand:
            print("You win, dealer loses!")
            player_balance += on_the_line
            show_hands(player, dealer)
        else:
            print("It's a TIE.")
            player_balance += player_bet
            dealer_balance += dealer_bet
            show_hands(player, dealer)

    play_again = input("Do you want to play again? (Y or N): ")
    if dealer_balance <= 0:
        play_again = 'N'
        print("The dealer is out of money!")
    elif player_balance == 0:
        play_again = 'N'
        print("You're all out of money!")

    if play_again == 'Y':
        play = True
        continue
    elif play_again not in ['Y', 'N']:
        play = False
        check_score(player_balance)
        print("I'm going to take that as a no. See ya!")
        player_balance = 5000
        dealer_balance = 5000
    else:
        check_score(player_balance)
        print("Thank you for playing!")
        player_balance = 5000
        dealer_balance = 5000
        break
