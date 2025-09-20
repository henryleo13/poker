from treys import Card, Evaluator
import random

# Create cards using Card.new() method
# Example cards: "Ah" for Ace of hearts, "Kd" for King of diamonds, etc.
cards = ["As", "Kh", "Qc", "Jd", "Th", "9s", "8h", "7c", "6d", "5h", "4s", "3h", "2c"]
suits = ["h", "d", "c", "s"]  # hearts, diamonds, clubs, spades

# Create a deck by converting string representations to card integers
deck = []
for card in cards:
    for suit in suits:
        deck.append(Card.new(card[0] + suit))

evaluator = Evaluator()
# Shuffle the deck
random.shuffle(deck)

# Draw cards for player's hand and flop
player_hand = [deck.pop(), deck.pop()]
flop = [deck.pop(), deck.pop(), deck.pop()]

# Print the cards
print("Your hand:", end=" ")
Card.print_pretty_cards(player_hand)

print("Flop:", end=" ")
Card.print_pretty_cards(flop)

p1_score = evaluator.evaluate(flop, player_hand)
p1_class = evaluator.get_rank_class(p1_score)
print(p1_score)
print(p1_class)