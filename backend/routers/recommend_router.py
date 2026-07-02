# backend/routers/recommend_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.poker_models import GameSession, HandHistory
from backend.schemas.poker_schemas import RecommendRequest
from backend.engine.hand_evaluator import HandEvaluator
from backend.engine.equity import EquityEngine
from backend.engine.pot_odds import PotOddsCalculator

router = APIRouter(prefix="/recommend", tags=["AI Strategy Recommendations"])

@router.post("/")
def get_strategy_recommendation(payload: RecommendRequest, db: Session = Depends(get_db)):
    try:
        session = db.query(GameSession).filter(GameSession.id == payload.session_id).first()
        if not session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Game session {payload.session_id} not found")

        equity_engine = EquityEngine(HandEvaluator())
        pot_odds_calculator = PotOddsCalculator()

        equity_result = equity_engine.calculate(payload.hole_cards, payload.community_cards, payload.num_opponents)
        win_equity = equity_result.get("win", 0.0)
        pot_odds_result = pot_odds_calculator.calculate(payload.pot_size, payload.bet_to_call, win_equity)
        pot_odds_positive = pot_odds_result.get("calling_ev_positive", False)

        action = "FOLD"
        confidence = 0.85

        if win_equity > 0.65:
            action = "RAISE"
        elif win_equity > 0.45 and pot_odds_positive:
            action = "CALL"
        elif win_equity < 0.30:
            action = "FOLD"
        else:
            action = "CALL"

        amount = payload.bet_to_call if action == "CALL" else (payload.pot_size * 0.5 if action == "RAISE" else 0.0)

        latest_hand = db.query(HandHistory.hand_number).filter(HandHistory.session_id == payload.session_id).order_by(HandHistory.hand_number.desc()).first()
        next_hand_number = (latest_hand[0] + 1) if latest_hand else 1

        hand_log = HandHistory(
            session_id=payload.session_id,
            hand_number=next_hand_number,
            hole_cards=payload.hole_cards,
            community_cards=payload.community_cards,
            pot_size=payload.pot_size,
            stack_size=payload.hero_stack,
            num_active_players=payload.num_opponents + 1,
            calculated_equity=win_equity,
            required_equity=pot_odds_result.get("required_equity", 0.0),
            expected_value=pot_odds_result.get("ev", 0.0),
            recommended_action=action,
            ai_explanation=(
                f"Win equity {win_equity:.4f}, required equity {pot_odds_result.get('required_equity', 0.0):.4f}, "
                f"bet_to_call {payload.bet_to_call}, pot_size {payload.pot_size}"
            )
        )
        
        db.add(hand_log)
        db.commit()
        db.refresh(hand_log)

        # 4. Return structural payload matching specifications
        return {
            "hand_id": hand_log.id,
            "recommendation": {
                "action": action,
                "amount": amount,
                "confidence": confidence
            },
            "equity": {
                "win": win_equity,
                "tie": equity_result.get("tie", 0.0),
                "lose": equity_result.get("lose", 0.0)
            },
            "pot_odds": pot_odds_result
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal analytical/database pipeline error: {str(e)}"
        )