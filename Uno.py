import random

class Card:
    # Class represents a playing card.

    def __init__(self, color, type):
        # Method is the constructor that initializes the card with a color and a type.

        self.color = color
        self.type = type
    
    def __str__(self):
        # Method returns a string representation of the card.

        return f'{self.type} {self.color}'
    
    @staticmethod
    def cardFromString(card_played_str):
        # Static method is used to create a Card object from a string representation of a card.

        if card_played_str == 'wild' or card_played_str == '+4':
            card_played = Card('', card_played_str)
        else:
            type, color = card_played_str.split()
            card_played = Card(color, type)
        return card_played


class Deck:
    # Class represents a deck of cards.

    def __init__(self):
        # Method initializes the deck by creating instances of all possible cards and adding them to the cards list.

        self.cards = []

        colors = ['blue', 'red', 'green', 'yellow']

        types = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'skip', 'reverse', '+2']

        wildcards = ['wild', '+4']

        for wildcard in wildcards:
            for _ in range(8):
                self.cards.append(Card('', wildcard))

        for color in colors:
            for type in types:
                for _ in range(4):
                    self.cards.append(Card(color, type))
        
    def shuffle(self):
        # Method shuffles the cards in the deck.

        random.shuffle(self.cards)
        return self.cards
    
    def deal(self, quantity):
        # Method deals a specified quantity of cards from the deck.

        dealt_cards = []
        for _ in range(quantity):
            card = self.cards.pop()
            dealt_cards.append(card)
        return dealt_cards


class PlayerHand:
    #  Class represents the hand of a player.

    def __init__(self):
        # Method initializes the player's hand as an empty list.

        self.hand_cards = []

    def addCard(self, card_list):
        # Method adds a list of cards to the player's hand.

        self.hand_cards.extend(card_list)
    
    def display(self):
        # Method prints the player's hand.

        print()
        print(f'You have {len(self.hand_cards)} cards:')
        print()
        print(' | '.join(map(str, self.hand_cards)))
        print()
    
    def canPlay(self, current_card, played_card):
        # Method checks if the player can play a specific card based on the current card in play. 

        card_in_hand = None
        for card in self.hand_cards:
            if card.color == played_card.color and card.type == played_card.type:
                card_in_hand = card
                break

        if card_in_hand is None:
            print("You don't have that card in your hand")
            return False
        
        if current_card.color == played_card.color or current_card.type == played_card.type or played_card.color == '':
            return True
        
        return False
    
    def playCard(self, played_card):
        # Method removes a played card from the player's hand.

        for card in self.hand_cards:
            if card.color == played_card.color and card.type == played_card.type:
                self.hand_cards.remove(card)
                break

    def hasWon(self):
        # Method checks if the player has won the game.

        if len(self.hand_cards) == 0:
            print()
            print('YOU WON!!!!😁🤩🎇')
            return 1
        return 0
    

class ComputerHand:
    # Class represents the hand of the computer opponent.

    def __init__(self):
        # Method initializes the computer's hand as an empty list.

        self.hand_cards = []

    def addCard(self, card_list):
        # Method adds a list of cards to the computer's hand.

        self.hand_cards.extend(card_list)
    
    def display(self):
        # Method prints the number of cards in the computer's hand.

        print(f'Computer has {len(self.hand_cards)} cards')
        print()
    
    def canPlay(self, current_card, played_card):
        #  Method checks if the computer can play a specific card based on the current card in play.

        if played_card not in self.hand_cards:
            return False
        if current_card.color == played_card.color or current_card.type == played_card.type or played_card.color == '':
            return True
        return False
    
    def playCard(self, played_card):
        # Method removes a played card from the computer's hand.

        for card in self.hand_cards:
            if card.color == played_card.color and card.type == played_card.type:
                self.hand_cards.remove(card)
                break

    def hasWon(self):
        # Method checks if the computer has won the game. 

        if len(self.hand_cards) == 0:
            print()
            print('The opponent won 😿😥😭')
            return 1
        return 0

class Game:
    #  Class represents the game itself.

    @staticmethod
    def playerTurn(deck, player_hand, current_card):
        # Static method handles the player's turn by getting the player's input, checking if the chosen card is valid, and returning the played card.

        while True:
            print()
            played_card_str = input('"D" to draw a card or choose which card to play: ').lower()
            print()
            if played_card_str == 'd':
                player_hand.addCard(deck.deal(1))
                player_hand.display()
            elif played_card_str == '+4' or played_card_str == 'wild':
                wild = played_card_str
                wild = Card.cardFromString(wild)
                player_hand.playCard(wild)
                print()
                print('blue | red | green | yellow')
                chosen_color = input('Choose a color: ').lower()
                if chosen_color not in ['blue', 'red', 'green', 'yellow']:
                    print()
                    print('Please choose a valid color')
                    chosen_color = input('Choose a color: ').lower()
                    played_card_str = played_card_str + ' ' + chosen_color
                    played_card = Card.cardFromString(played_card_str)
                    break
                else:
                    played_card_str = played_card_str + ' ' + chosen_color
                    played_card = Card.cardFromString(played_card_str)
                    break
            elif played_card_str == '' or played_card_str == 'd ' or played_card_str == ' d':
                print()
                print('Play a valid card') 
                print()
            elif played_card_str != 'd' or played_card_str != '+4' or played_card_str != 'wild':
                played_card = Card.cardFromString(played_card_str)
                if player_hand.canPlay(current_card, played_card) is False:
                    print()
                    print('Play a valid card')
                    print()
                else:
                    player_hand.playCard(played_card)
                    break
            

        return played_card

    @staticmethod
    def computerTurn(deck, computer_hand, current_card):
        #  Static method handles the computer's turn by checking if the computer has a valid card to play and returning the played card.

        valid_play = None
        while valid_play is None:
            i = 0
            while i - 1 <= len(computer_hand.hand_cards):
                if i < len(computer_hand.hand_cards):
                    if computer_hand.canPlay(current_card, computer_hand.hand_cards[i]) is False:
                        i += 1
                    else:
                        break
                else: 
                    computer_hand.addCard(deck.deal(1))
                    i = 0
            if i <= len(computer_hand.hand_cards):
                valid_play = 1
                played_card = computer_hand.hand_cards[i]
        computer_hand.playCard(played_card)
        if played_card.type == '+4' or played_card.type == 'wild':
            color_list = ['blue', 'red', 'green', 'yellow']
            chosen_color = random.choice(color_list)
            played_card = played_card.type + ' ' + chosen_color
            played_card = Card.cardFromString(played_card)
        return played_card


    def start(self):
        # Method represents the script of the game.

        deck = Deck()
        deck.shuffle()

        player_hand = PlayerHand()
        computer_hand = ComputerHand()

        player_hand.addCard(deck.deal(7))
        computer_hand.addCard(deck.deal(7))

        current_card1 = deck.cards.pop()
        while current_card1.type == '+2' or current_card1.type == 'skip' or current_card1.type == '+4' or current_card1.type == 'wild' or current_card1.type == 'reverse':
            current_card1 = deck.cards.pop()

        print('*' * 35)
        print()
        print(f'The initial card is {current_card1}')
        
        played_card1 = current_card1
        initial_card = played_card1
        winner = None

        while winner is None:
            print()
            print('*' * 35)

            print()

            computer_hand.display()
            player_hand.display()

            print()
            print('*' * 35)
            print()

            played_card2 = initial_card

            if played_card1.type != 'skip':
                played_card2 = Game.playerTurn(deck, player_hand, current_card1) 
                current_card2 = played_card2
            if played_card1.type == 'skip':
                current_card2 = played_card1

            if played_card1.type != 'skip':
                print('*' * 35)
                print()
                print(f'The current card is {current_card2}')
                print()
                print('*' * 35)

            check = player_hand.hasWon()
            if check == 1:
                break

            if current_card2.type == '+4':
                computer_hand.addCard(deck.deal(4))
            elif current_card2.type == '+2':
                computer_hand.addCard(deck.deal(2))
            
            print()

            if played_card2.type != 'skip':
                played_card1 = Game.computerTurn(deck, computer_hand, current_card2)

            current_card1 = played_card1

            if played_card2.type != 'skip':
                print(f'The opponent played a {current_card1}')

            if current_card1.type == '+4':
                player_hand.addCard(deck.deal(4))
            elif current_card1.type == '+2':
                player_hand.addCard(deck.deal(2))

            check = computer_hand.hasWon()
            if check == 1:
                break


# Calling the game to begin

game = Game()

game.start()