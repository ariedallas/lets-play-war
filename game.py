import random
import sys

from enum import Enum

class CardSuit(Enum):
    CLUB = 'Clubs'
    DIAMOND = 'Diamonds'
    HEART = 'Hearts'
    SPADE = 'Spades'

class CardValue(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

class Player:
    def __init__(self, name, var_deck):
        self.name = name
        self.my_deck = var_deck
        self.my_cards = var_deck.deck

    def wins(self, var_pot):
        for c in var_pot:
            self.my_cards.append(c)

        # print(self.my_deck.total_cards())

    def draw(self):
        return self.my_cards.pop(0)


    def print_first_five_cards(self):
        print(
            [c.name for c in self.my_cards[:5]]
        )


    def print_last_three_cards(self):
        print(
            [c.name for c in self.my_cards[-3:]]
        )

    def select_random_card(self):
        rand_card_object = random.choice(self.my_deck.deck)
        rand_card_object.print_name()
        return rand_card_object


class DeckOfCards:
    def __init__(self, provided_cards=None):
        if provided_cards:
            self.deck = provided_cards

        else: # Setup initial deck
            self.deck = []

            for suit in CardSuit:
                for rank in CardValue:
                    new_card = Card(CardValue(rank), CardSuit(suit))
                    self.deck.append(new_card)

    def shuffle(self):
        random.shuffle(self.deck)


    def total_cards(self):
        return len(self.deck)


    def split_deck(self):
        mid_point = len(self.deck) // 2

        deck_part_one = self.deck[:mid_point]
        deck_part_two = self.deck[mid_point:]

        return deck_part_one, deck_part_two


class Card:
    def __init__(self, card_value, card_suit):
        self.card_value = card_value
        self.card_suit = card_suit
        self.name = f"{self.card_value.name.title()} of {self.card_suit.value.title()}"


    def print_name(self):
        print(f"{self.card_value.name.title()} of {self.card_suit.value.title()}")


class Game:
    def __init__(self, player_one, player_two):
        self.pot = []
        self.player_one = player_one
        self.player_two = player_two

    def round(self):
        print("\nBegin round:")
        print(f"{self.player_one.name} begins this round with: {self.player_one.my_deck.total_cards()} cards")
        print(f"{self.player_two.name} begins this round with: {self.player_two.my_deck.total_cards()} cards")

        # self.player_one.print_first_five_cards()
        # self.player_one.print_last_three_cards()
        #
        # print(f"Mao begins this round with: ")
        # self.player_two.print_first_five_cards()
        # self.player_two.print_last_three_cards()

        drawn_card_h = self.player_one.draw()
        drawn_card_m = self.player_two.draw()

        self.pot.append(drawn_card_h)
        self.pot.append(drawn_card_m)

        print()
        self.print_pot()

        self.determine_pot(drawn_card_h, drawn_card_m)


    def print_pot(self):
        print("    The pot is: ", end=" ")
        for c in self.pot:
            print(c.name, end=" : ")
        print()


    def shuffle_pot(self):
        random.shuffle(self.pot)


    def war(self):
        for c in range(3):
            self.pot.append(self.player_one.draw())
            self.pot.append(self.player_two.draw())

        drawn_card_h = self.player_one.draw()
        drawn_card_m = self.player_two.draw()

        self.pot.append(drawn_card_h)
        self.pot.append(drawn_card_m)

        self.print_pot()

        self.determine_pot(drawn_card_h, drawn_card_m)


    def determine_pot(self, drawn_card_p_one, drawn_card_p_two):
        val_card_h = drawn_card_p_one.card_value.value
        val_card_m = drawn_card_p_two.card_value.value

        if val_card_h > val_card_m:
            print(f"    {self.player_one.name} Wins! {drawn_card_p_one.name} >>> {drawn_card_p_two.name}")
            self.shuffle_pot()
            self.player_one.wins(self.pot)
            self.pot = []
        elif val_card_m > val_card_h:
            print(f"    {self.player_two.name} Wins! {drawn_card_p_two.name} >>> {drawn_card_p_one.name}")
            self.shuffle_pot()
            self.player_two.wins(self.pot)
            self.pot = []
        else:
            print("    WAR!!!")
            self.war()

    def check_for_winner(self):
        if self.player_one.my_deck.total_cards() == 0:
            return True, self.player_two
        elif self.player_two.my_deck.total_cards() == 0:
            return True, self.player_one
        else:
            return False, None

# ---- MAIN ---- #

def main():
    game_deck = DeckOfCards()
    game_deck.shuffle()

    deck_part_one, deck_part_two = game_deck.split_deck()

    player_humberto = Player("Humberto", DeckOfCards(deck_part_one))
    player_mao = Player("Mao", DeckOfCards(deck_part_two))

    game = Game(player_humberto, player_mao)

    while True:
        user_input = input("\nNext Round Go -->  ")

        if user_input.lower() == "no":
            break

        if game.check_for_winner()[0]:
            _, winner = game.check_for_winner()
            print(f"{winner.name}, wins!!!")
            sys.exit(0)

        game.round()

if __name__ == "__main__":
    main()

# edge cases: what if player doesn't have enough cards?
#   however many cards they have, they play.
#   i.e. if they have two cards remaining after the tie, they draw remaining minus one
#   if they tie on the last card, then they win
# split the deck in half and give each player 1/2
# can I show flipped cards?
# can I do a reveal of what each person won?