# backend/models/poker_models.py
import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from backend.database import Base

class GameSession(Base):
    __tablename__ = "game_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_name = Column(String, nullable=True, default=lambda: f"Session_{datetime.date.today().isoformat()}")
    small_blind = Column(Float, nullable=False, default=1.0)
    big_blind = Column(Float, nullable=False, default=2.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    net_profit = Column(Float, default=0.0)

    # Relationship to cleanly query hands belonging to this session
    hands = relationship("HandHistory", back_populates="session", cascade="all, delete-orphan")


class HandHistory(Base):
    __tablename__ = "hand_histories"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("game_sessions.id", ondelete="CASCADE"), nullable=False)
    hand_number = Column(Integer, nullable=False)
    
    # Game State vectors stored as simple strings or JSON lists
    hole_cards = Column(JSON, nullable=False)          # e.g., ["As", "Ah"]
    community_cards = Column(JSON, nullable=False)     # e.g., ["Jd", "Ts", "2c"]
    pot_size = Column(Float, nullable=False)
    stack_size = Column(Float, nullable=False)
    num_active_players = Column(Integer, nullable=False, default=2)
    
    # Engine Calculations
    calculated_equity = Column(Float, nullable=False)  # Win/Tie percentage
    required_equity = Column(Float, nullable=False)    # Pot odds break-even line
    expected_value = Column(Float, nullable=False)     # EV score
    recommended_action = Column(String, nullable=False)# FOLD, CALL, RAISE
    
    # Dynamic LLM Context storage
    ai_explanation = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    session = relationship("GameSession", back_populates="hands")


class OpponentProfile(Base):
    __tablename__ = "opponent_profiles"

    id = Column(Integer, primary_key=True, index=True)
    player_name = Column(String, unique=True, index=True, nullable=False)
    
    # Basic tracking telemetry to feed into your K-Means clustering algorithm
    total_hands_observed = Column(Integer, default=0)
    vpip_count = Column(Integer, default=0)            # Voluntarily Put Money In Pot
    pfr_count = Column(Integer, default=0)             # Pre-Flop Raise count
    three_bet_count = Column(Integer, default=0)
    agg_actions = Column(Integer, default=0)           # Total bets + raises
    pass_actions = Column(Integer, default=0)          # Total checks + calls
    
    # The derived classification metric calculated by ML notebook module
    inferred_style = Column(String, default="UNKNOWN") # e.g., "TAG", "LAG", "FISH", "WHALE"
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)