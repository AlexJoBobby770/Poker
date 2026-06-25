# backend/engine/equity.py
import random
from backend.engine.hand_evaluator import HandEvaluator

class EquityEngine:
    def __init__(self, evaluator: HandEvaluator, num_simulations: int = 10000):
        self.evaluator = evaluator
        self.num_simulations = num_simulations
        
        # Build a global immutable deck
        ranks = "23456789TJQKA"
        suits = "shdc"
        self.full_deck = [f"{r}{s}" for r in ranks for s in suits]

    def calculate(self, hole_cards: list[str], community_cards: list[str], num_opponents: int) -> dict:
        """
        Runs a Monte Carlo simulation to calculate winning probabilities.
        """
        dead_cards = set(hole_cards + community_cards)
        remaining_deck = [card for card in self.full_deck if card not in dead_cards]

        wins = 0
        ties = 0
        losses = 0

        needed_board_cards = 5 - len(community_cards)

        for _ in range(self.num_simulations):
            # Sample remaining cards randomly for board completions
            k = (2 * num_opponents) + needed_board_cards
            deck_sample = random.sample(remaining_deck, k)
            
            # Deal opponent hands dynamically from the randomized sample
            opponents_hands = []
            for _ in range(num_opponents):
                opponents_hands.append([deck_sample.pop(), deck_sample.pop()])

            # Complete the remaining streets on the board
            simulated_board = list(community_cards)
            for _ in range(needed_board_cards):
                simulated_board.append(deck_sample.pop())

            # Evaluate Hero's standing
            hero_rank = self.evaluator.evaluate(hole_cards, simulated_board)

            # Evaluate Opponents' standings
            best_opponent_rank = float('inf')
            for opp_hand in opponents_hands:
                opp_rank = self.evaluator.evaluate(opp_hand, simulated_board)
                if opp_rank < best_opponent_rank:
                    best_opponent_rank = opp_rank

            # In treys, lower rank scores signify stronger absolute hand values
            if hero_rank < best_opponent_rank:
                wins += 1
            elif hero_rank == best_opponent_rank:
                ties += 1
            else:
                losses += 1

        return {
            "win": round(wins / self.num_simulations, 4),
            "tie": round(ties / self.num_simulations, 4),
            "lose": round(losses / self.num_simulations, 4),
            "simulations_run": self.num_simulations
        }