# backend/engine/hand_evaluator.py
from treys import Card, Evaluator

class HandEvaluator:
    def __init__(self):
        self.evaluator = Evaluator()

    def parse_card(self, card_str: str) -> int:
        """Converts a standard string like 'As' or 'Td' to treys integer format."""
        # treys expects uppercase for ranks, lowercase for suits.
        formatted_card = card_str[0].upper() + card_str[1].lower()
        return Card.new(formatted_card)

    def evaluate(self, hole_cards: list[str], board: list[str]) -> int:
        """Returns integer hand rank. Lower is better. 1 = Royal Flush."""
        treys_hand = [self.parse_card(c) for c in hole_cards]
        treys_board = [self.parse_card(c) for c in board]
        return self.evaluator.evaluate(treys_board, treys_hand)

    def rank_to_string(self, rank: int) -> str:
        """Converts integer rank to human-readable format like 'Full House'."""
        return self.evaluator.class_to_string(self.evaluator.get_rank_class(rank))