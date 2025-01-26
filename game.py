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
        self.round_counter = 0

    def round(self):
        print(f"\nBegin round: {self.round_counter}")
        print(f"{self.player_one.name} begins this round with: {self.player_one.my_deck.total_cards()} cards")
        print(f"{self.player_two.name} begins this round with: {self.player_two.my_deck.total_cards()} cards")

        drawn_card_h = self.player_one.draw()
        drawn_card_m = self.player_two.draw()

        self.pot.append(drawn_card_h)
        self.pot.append(drawn_card_m)

        print()
        self.print_pot()

        self.determine_pot(drawn_card_h, drawn_card_m, 0)
        self.round_counter += 1


    def print_pot(self):
        print("    The pot is: ", end=" ")

        if len(self.pot) <= 2:
            for c in self.pot[:2]:
                print(c.name, end=" : ")
            print()
        else:
            for c in self.pot[:3]:
                print(c.name, end=" : ")
            print(f"[ ++ {len(self.pot) -3} more cards ]")


    def shuffle_pot(self):
        random.shuffle(self.pot)


    def war(self, cnt, draw_amount=3):
        for c in range(draw_amount):
            self.pot.append(self.player_one.draw())
            self.pot.append(self.player_two.draw())

        drawn_card_h = self.player_one.draw()
        drawn_card_m = self.player_two.draw()

        self.pot.append(drawn_card_h)
        self.pot.append(drawn_card_m)

        self.print_pot()


        self.determine_pot(drawn_card_h, drawn_card_m, cnt)


    def determine_pot(self, drawn_card_p_one, drawn_card_p_two, cnt):
        val_card_h = drawn_card_p_one.card_value.value
        val_card_m = drawn_card_p_two.card_value.value

        if val_card_h > val_card_m:
            print(f"    {self.player_one.name.upper()} WINS!   {drawn_card_p_one.name} >>> {drawn_card_p_two.name}")
            self.shuffle_pot()
            self.player_one.wins(self.pot)
            self.pot = []
        elif val_card_m > val_card_h:
            print(f"    {self.player_two.name.upper()} WINS!   {drawn_card_p_two.name} >>> {drawn_card_p_one.name}")
            self.shuffle_pot()
            self.player_two.wins(self.pot)
            self.pot = []
        else:
            cnt += 1
            if cnt == 1:
                print("\n    IT'S WAR!!!\n")
            elif cnt == 2:
                print("\n    DOUBLE WAR!!!\n")
            elif cnt == 3:
                print("\n    TRIPLE WAR!!!\n")
            else:
                print(f"\n    ALL OUT UNSTOPPABLE WAR #{cnt}!!!\n")

            curr_loser = self.get_curr_loser()

            if curr_loser.my_deck.total_cards() >= 4:
                self.war(cnt)
            elif 0 < curr_loser.my_deck.total_cards() < 4:
                draw_amount = curr_loser.my_deck.total_cards() - 1
                self.war(cnt, draw_amount)
            else:
                # curr_loser.my_deck.total_cards() == 0:
                curr_loser.wins(self.pot)

        if self.check_for_winner()[0]:
            _, winner = self.check_for_winner()
            print(f"\n{winner.name}, wins the game!!!")
            sys.exit(0)

            # elif curr_loser.my_deck.total_cards() == 1:

    def get_curr_loser(self):
        if self.player_one.my_deck.total_cards() <= self.player_two.my_deck.total_cards():
            return self.player_one
        else:
            return self.player_two


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

    # print(type(player_mao.my_deck.total_cards()))

    game = Game(player_one=player_humberto, player_two=player_mao)

    while True:
        user_input = input("\nNext Round Go -->  ")

        if user_input.lower() == "no":
            break

        game.round()

if __name__ == "__main__":
    main()

#   how to implement / track double war?

# show a stack trace with recursion
# clean up pot print with war
# can I show flipped cards?
# can I do a reveal of what each person won?