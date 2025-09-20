# Create a program to play Texas Hold'em Poker

# The program should be able to handle multiple players and the dealer
# The program should be able to handle multiple rounds of betting
# The program should be able to handle the dealer's actions
# The program should be able to handle the player's actions
# The program should be able to handle the game's end

import random
from typing import List
from utils import Suit, Card, evaluate_hand, compare_hands, calculate_pot_odds

class Deck:
    def __init__(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [Card(rank, suit) for suit in Suit for rank in ranks]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self) -> Card:
        return self.cards.pop()


class Player:
    def __init__(self, name: str, chips: int):
        self.name = name
        self.chips = chips
        self.hand: List[Card] = []
        self.current_bet = 0

    def bet(self, amount: int) -> int:
        if amount > self.chips:
            amount = self.chips
        self.chips -= amount
        self.current_bet += amount
        return amount

    def make_decision(self, game_state) -> str:
        # Implement decision-making logic using Monte Carlo simulation
        win_probability = monte_carlo_simulation(self, game_state.community_cards, 1000)
        
        # Calculate the amount to call
        amount_to_call = max(0, game_state.current_bet - self.current_bet)
        
        # Calculate pot odds
        if amount_to_call > 0:
            pot_odds = calculate_pot_odds(game_state.pot, amount_to_call)
        else:
            pot_odds = 0  # If no call is needed, set pot odds to 0
        
        if win_probability > pot_odds:
            if amount_to_call == 0:
                return 'check'
            else:
                return 'call'
        elif win_probability > 0.7:  # Arbitrary threshold for raising
            return 'raise'
        else:
            if amount_to_call == 0:
                return 'check'
            else:
                return 'fold'

class Game:
    def __init__(self, players: List[Player], small_blind: int, big_blind: int):
        self.players = players
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.deck = Deck()
        self.community_cards: List[Card] = []
        self.pot = 0
        self.current_bet = 0

    def deal_hole_cards(self):
        for _ in range(2):
            for player in self.players:
                player.hand.append(self.deck.deal())

    def deal_community_cards(self, num_cards: int):
        for _ in range(num_cards):
            self.community_cards.append(self.deck.deal())

    def betting_round(self):
        # Implement betting round logic
        active_players = [player for player in self.players if player.chips > 0]
        betting_players = active_players.copy()
        
        while len(betting_players) > 1:
            for player in betting_players:
                if player.chips == 0:
                    continue
                
                decision = player.make_decision(self)
                
                if decision == 'fold':
                    betting_players.remove(player)
                elif decision == 'call':
                    bet_amount = self.current_bet - player.current_bet
                    self.pot += player.bet(bet_amount)
                    player.current_bet = self.current_bet
                elif decision == 'raise':
                    raise_amount = min(player.chips, self.current_bet * 2)  # Simple raise logic
                    self.pot += player.bet(raise_amount)
                    self.current_bet = player.current_bet
                    # Reset betting for other players
                    for other_player in betting_players:
                        if other_player != player:
                            other_player.current_bet = 0
            
            # Check if all players have the same bet
            if all(player.current_bet == self.current_bet for player in betting_players):
                break
        
        # Reset current bets for the next round
        for player in self.players:
            player.current_bet = 0
        self.current_bet = 0
        pass

    def play_hand(self):
        print("\n--- New Hand ---")
        # Reset current_bet for all players
        for player in self.players:
            player.current_bet = 0
        
        # Initialize pot with small and big blinds
        self.pot = self.small_blind + self.big_blind
        
        # Collect small and big blinds
        small_blind_player = self.players[0]  # Assuming first player is small blind
        big_blind_player = self.players[1]    # Assuming second player is big blind
        
        small_blind_player.bet(self.small_blind)
        big_blind_player.bet(self.big_blind)
        
        print(f"Small blind: {self.small_blind} from {small_blind_player.name}")
        print(f"Big blind: {self.big_blind} from {big_blind_player.name}")
        print(f"Pot: {self.pot}")

        self.deal_hole_cards()
        print("Hole cards dealt")
        self.betting_round()  # Pre-flop
        print("Pre-flop betting round complete")
        
        self.deal_community_cards(3)  # Flop
        print(f"Flop: {' '.join(str(card) for card in self.community_cards)}")
        self.betting_round()
        print("Flop betting round complete")
        
        self.deal_community_cards(1)  # Turn
        print(f"Turn: {self.community_cards[-1]}")
        self.betting_round()
        print("Turn betting round complete")
        
        self.deal_community_cards(1)  # River
        print(f"River: {self.community_cards[-1]}")
        self.betting_round()
        print("River betting round complete")
        
        self.showdown()
        print("Showdown complete")

        for player in self.players:
            print(f"{player.name}: {player.chips} chips")

    def showdown(self):
        # Implement showdown logic
        active_players = [player for player in self.players if player.chips > 0 and len(player.hand) > 0]
        if len(active_players) == 1:
            winner = active_players[0]
            winner.chips += self.pot
            print(f"{winner.name} wins {self.pot} chips")
        else:
            player_hands = [(player, player.hand + self.community_cards) for player in active_players]
            winner = max(player_hands, key=lambda x: evaluate_hand(x[1]))[0]
            winner.chips += self.pot
            print(f"{winner.name} wins {self.pot} chips")
            print(f"Winning hand: {' '.join(str(card) for card in winner.hand)}")
        self.pot = 0

def monte_carlo_simulation(player: Player, community_cards: List[Card], num_simulations: int) -> float:
    wins = 0
    for _ in range(num_simulations):
        sim_deck = Deck()
        # Create a new list of cards to remove
        cards_to_remove = player.hand + community_cards
        # Remove cards from the simulated deck if they exist
        sim_deck.cards = [card for card in sim_deck.cards if card not in cards_to_remove]
        
        sim_community_cards = community_cards.copy()
        while len(sim_community_cards) < 5:
            sim_community_cards.append(sim_deck.deal())
        
        opponent_hand = [sim_deck.deal(), sim_deck.deal()]
        
        result = compare_hands(player.hand + sim_community_cards, opponent_hand + sim_community_cards)
        if result == 1:
            wins += 1
        elif result == 0:
            wins += 0.5
    
    return wins / num_simulations

# Main game loop
if __name__ == "__main__":
    players = [Player("Player 1", 1000), Player("Player 2", 1000)]
    game = Game(players, small_blind=5, big_blind=10)

    num_hands = 100
    for _ in range(num_hands):
        game.play_hand()
        # Reset game state for next hand
        game.community_cards = []
        game.pot = 0
        game.current_bet = 0
        game.deck = Deck()
        for player in game.players:
            player.hand = []

    # Print final chip counts
    for player in game.players:
        print(f"{player.name}: {player.chips} chips")

