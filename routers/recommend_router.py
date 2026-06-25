# backend/routers/recommend_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.poker_models import HandHistory
from backend.schemas.poker_schemas import RecommendRequest
# Mocking engines assuming standard class naming styles, adjust imports if your files use different names
from backend.engine.equity import EquityEngine
from backend.engine.pot_odds import PotOddsCalculator

router = APIRouter(prefix="/recommend", tags=["AI Strategy Recommendations"])

@router.post("/")
def get_strategy_recommendation(payload: RecommendRequest, db: Session = Depends(get_db)):
    try:
        # 1. Invoke your structural Phase 2 calculation engines
        # (Adjust method calls below to match your exact equity/pot-odds method names if needed)
        equity_result = EquityEngine.calculate(payload.hole_cards, payload.community_cards, payload.num_opponents)
        win_equity = equity_result.get("win", 0.0)
        
        pot_odds_result = PotOddsCalculator.calculate(payload.pot_size, payload.bet_to_call, win_equity)
        pot_odds_positive = pot_odds_result.get("calling_justified", False)

        # 2. Apply Claude's specific postflop strategic heuristic rule layer
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

        # Simple scaling amount logic based on pot sizes
        amount = payload.bet_to_call if action == "CALL" else (payload.pot_size * 0.5 if action == "RAISE" else 0.0)

        # 3. Instantiate database mapping row to track historical context
        hand_log = HandHistory(
            session_id=payload.session_id,
            hole_cards=",".join(payload.hole_cards),
            community_cards=",".join(payload.community_cards) if payload.community_cards else None,
            pot_size=payload.pot_size,
            engine_equity=win_equity,
            ai_suggestion=f"{action} {amount}".strip()
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