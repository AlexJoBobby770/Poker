
from database import SessionLocal
from models.poker_models import GameSession, OpponentProfile

# Open an atomic database transaction session
db = SessionLocal()

print("--- Testing Database Operations ---")
try:
    # 1. Insert a test game session tracking row
    test_session = GameSession(small_blind=1.0, big_blind=2.0, session_name="Test Session Kochi")
    db.add(test_session)
    db.commit() # Push the data permanently down into the PostgreSQL container
    db.refresh(test_session)
    print(f"✅ Successfully created GameSession! Generated Row ID: {test_session.id}")

    # 2. Insert an opponent tracking row to test the profiling database connection
    opponent = OpponentProfile(player_name="Villain_770", total_hands_observed=42, inferred_style="FISH")
    db.add(opponent)
    db.commit()
    db.refresh(opponent)
    print(f"✅ Successfully created OpponentProfile! Name: {opponent.player_name}")

    # 3. Read it back out to verify data integrity
    queried_player = db.query(OpponentProfile).filter_by(player_name="Villain_770").first()
    print(f"🔍 Query Verification -> Player: {queried_player.player_name}, Observed Hands: {queried_player.total_hands_observed}")

    # 4. Clean up the database so we don't leave junk rows behind
    db.delete(test_session)
    db.delete(opponent)
    db.commit()
    print("🧹 Database verification complete and test records cleaned up successfully!")

except Exception as e:
    print(f"❌ Database error encountered: {e}")
finally:
    db.close() # Always close the connection pool when done