# backend/routers/session_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.poker_models import GameSession, HandHistory
from backend.schemas.poker_schemas import SessionCreate, SessionResponse
from typing import List, Dict, Any

router = APIRouter(prefix="/session", tags=["Game Sessions"])

@router.post("/", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(session_data: SessionCreate, db: Session = Depends(get_db)):
    try:
        new_session = GameSession(
            num_players=session_data.num_players,
            notes=session_data.notes
        )
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        return new_session
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create game session in database: {str(e)}"
        )

@router.get("/{session_id}", response_model=Dict[str, Any])
def get_session_metadata(session_id: int, db: Session = Depends(get_db)):
    session = db.query(GameSession).filter(GameSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail=f"Game session with ID {session_id} not found")
    
    # Grab all hand IDs associated with this specific session
    hand_ids = db.query(HandHistory.id).filter(HandHistory.session_id == session_id).all()
    flat_hand_ids = [h[0] for h in hand_ids]

    return {
        "session_id": session.id,
        "num_players": session.num_players,
        "notes": session.notes,
        "created_at": session.created_at,
        "associated_hand_ids": flat_hand_ids
    }