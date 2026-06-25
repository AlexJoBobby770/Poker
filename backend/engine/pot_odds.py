# backend/engine/pot_odds.py

class PotOddsCalculator:
    def calculate(self, pot_size: float, bet_to_call: float, equity: float) -> dict:
        """
        Calculates pot odds and checks if calling yields positive expected value.
        """
        # The financial threshold ratio you need to break even on a call
        pot_odds_ratio = bet_to_call / (pot_size + bet_to_call) if (pot_size + bet_to_call) > 0 else 0
        calling_justified = equity >= pot_odds_ratio
        
        # Long-term EV tracking formula
        ev = (equity * pot_size) - ((1.0 - equity) * bet_to_call)

        return {
            "required_equity": round(pot_odds_ratio, 4),
            "actual_equity": round(equity, 4),
            "calling_ev_positive": calling_justified,
            "ev": round(ev, 2)
        }

    def minimum_defence_frequency(self, bet_size: float, pot_size: float) -> float:
        """MDF mathematical representation = Pot / (Pot + Bet)"""
        if (pot_size + bet_size) == 0:
            return 0.0
        return round(pot_size / (pot_size + bet_size), 4)