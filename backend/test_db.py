
from database import SessionLocal, engine, Base
from models.poker_models import GameSession, OpponentProfile


Base.metadata.create_all(bind=engine)

def test_database_crud_operations():
    db = SessionLocal()
    test_session = None
    opponent = None

    try:
        test_session = GameSession(num_players=2, notes="Test Session Verification")
        db.add(test_session)
        db.commit()
        db.refresh(test_session)

        assert test_session.id is not None
        assert test_session.num_players == 2

        opponent = OpponentProfile(player_name="Villain_770", total_hands_observed=42, inferred_style="FISH")
        db.add(opponent)
        db.commit()
        db.refresh(opponent)

        assert opponent.id is not None
        assert opponent.player_name == "Villain_770"

        queried_player = db.query(OpponentProfile).filter_by(player_name="Villain_770").first()
        assert queried_player is not None
        assert queried_player.total_hands_observed == 42

    finally:
        if test_session is not None:
            db.delete(test_session)
        if opponent is not None:
            db.delete(opponent)
        db.commit()
        db.close()
