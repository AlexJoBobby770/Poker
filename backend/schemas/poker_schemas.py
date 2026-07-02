import re
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field, field_validator

CARD_REGEX = re.compile(r"^[2-9TJQKA][shdc]$")

class SessionCreate(BaseModel):
    num_players: int = Field(..., ge=2, le=9)  # Validation rule: Between 2 and 9 players
    notes: Optional[str] = None

class SessionResponse(BaseModel):
    id: UUID
    num_players: int
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class RecommendRequest(BaseModel):
    session_id: UUID
    hole_cards: List[str] = Field(..., min_items=2, max_items=2)
    community_cards: List[str] = Field(default=[])
    street: str = Field(..., description="preflop, flop, turn, or river")
    pot_size: float
    hero_stack: float
    bet_to_call: float
    num_opponents: int
    position: str

    @field_validator("hole_cards", "community_cards")
    @classmethod
    def validate_card_formats(cls, cards: List[str]) -> List[str]:
        for card in cards:
            if not CARD_REGEX.match(card):
                raise ValueError(f"Invalid card string format: '{card}'. Must match e.g., 'As', 'Kh', '2d'")
        return cards

    @field_validator("community_cards")
    @classmethod
    def validate_street_lengths(cls, community_cards: List[str], info) -> List[str]:
        street = info.data.get("street", "").lower()
        expected_counts = {"preflop": 0, "flop": 3, "turn": 4, "river": 5}
        
        if street in expected_counts and len(community_cards) != expected_counts[street]:
            raise ValueError(f"Community cards length ({len(community_cards)}) does not match street '{street}' (expected {expected_counts[street]})")
        return community_cards

    @field_validator("community_cards")
    @classmethod
    def check_duplicate_cards(cls, community_cards: List[str], info) -> List[str]:
        hole_cards = info.data.get("hole_cards", [])
        all_cards = hole_cards + community_cards
        if len(all_cards) != len(set(all_cards)):
            raise ValueError("Duplicate cards detected across hole cards and community cards.")
        return community_cards

    @field_validator("street")
    @classmethod
    def validate_street(cls, street: str) -> str:
        normalized = street.lower()
        valid_streets = {"preflop", "flop", "turn", "river"}
        if normalized not in valid_streets:
            raise ValueError("street must be one of preflop, flop, turn, or river")
        return normalized