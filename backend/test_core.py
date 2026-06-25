# backend/test_core.py
from engine.hand_evaluator import HandEvaluator
from engine.equity import EquityEngine
from engine.pot_odds import PotOddsCalculator

evaluator = HandEvaluator()
engine = EquityEngine(evaluator, num_simulations=10000)
pot_calc = PotOddsCalculator()

print("--- Testing Core System Components ---")

# 1. Test Hand Evaluator (Royal Flush Verification)
rank = evaluator.evaluate(['As', 'Ks'], ['Qs', 'Js', 'Ts', '2d', '3h'])
print(f"Royal Flush Rank (Should be 1): {rank}")
print(f"Hand Category: {evaluator.rank_to_string(rank)}")

print("\n--- Running Monte Carlo (10k iterations) ---")
# 2. Preflop Pocket Aces vs 1 Random Opponent (Should yield ~85% Win/Tie Equity)
preflop_aa = engine.calculate(['As', 'Ah'], [], num_opponents=1)
print(f"Pocket Aces Preflop Equity: {preflop_aa}")

# 3. Flop Equity Test (Nut Straight Draw)
flop_draw = engine.calculate(['As', 'Kh'], ['Jd', 'Ts', '2c'], num_opponents=1)
print(f"Nut Straight Draw on Flop Equity: {flop_draw}")

print("\n--- Testing Pot Odds ---")
# 4. Pot Odds check (Pot = 100, Bet to call = 50, Equity = 40%)
odds = pot_calc.calculate(pot_size=100.0, bet_to_call=50.0, equity=0.40)
print(f"Pot Odds Summary: {odds}")