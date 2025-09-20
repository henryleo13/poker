from typing import List
from enum import Enum

class Suit(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"

class Card:
    def __init__(self, rank: str, suit: Suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank}{self.suit.value}"

def evaluate_hand(hand: List[Card]) -> int:
    # Implement hand evaluation logic
    # This is a placeholder implementation
    return sum(int(card.rank) if card.rank.isdigit() else 10 for card in hand)

def compare_hands(hand1: List[Card], hand2: List[Card]) -> int:
    score1 = evaluate_hand(hand1)
    score2 = evaluate_hand(hand2)
    if score1 > score2:
        return 1
    elif score1 < score2:
        return -1
    else:
        return 0

def calculate_pot_odds(pot: int, bet_to_call: int) -> float:
    return bet_to_call / (pot + bet_to_call)

# ... other utility functions as needed


class Player:
    def __init__(self, name: str, chips: int):
        self.name = name
        self.chips = chips
        self.hand: List[Card] = []
        self.current_bet = 0  # Add this line

    def bet(self, amount: int) -> int:
        if amount > self.chips:
            amount = self.chips
        self.chips -= amount
        self.current_bet += amount  # Update current_bet when betting
        return amount

    def reset_hand(self):
        self.hand = []
        self.current_bet = 0  # Reset current_bet when hand is reset

    # ... (other methods remain the same)
