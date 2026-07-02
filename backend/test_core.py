from backend.engine.hand_evaluator import HandEvaluator
from backend.engine.equity import EquityEngine
from backend.engine.pot_odds import PotOddsCalculator


def test_hand_evaluator_rank_type():
    evaluator = HandEvaluator()
    rank = evaluator.evaluate(['As', 'Ks'], ['Qs', 'Js', 'Ts', '2d', '3h'])
    assert isinstance(rank, int)
    assert rank > 0


def test_equity_engine_returns_probabilities():
    evaluator = HandEvaluator()
    engine = EquityEngine(evaluator, num_simulations=100)
    result = engine.calculate(['As', 'Ah'], [], num_opponents=1)
    assert 0.0 <= result['win'] <= 1.0
    assert 0.0 <= result['tie'] <= 1.0
    assert 0.0 <= result['lose'] <= 1.0
    assert result['simulations_run'] == 100


def test_pot_odds_calculator():
    pot_calc = PotOddsCalculator()
    odds = pot_calc.calculate(pot_size=100.0, bet_to_call=50.0, equity=0.40)
    assert odds['required_equity'] == 0.3333
    assert odds['calling_ev_positive'] is False
