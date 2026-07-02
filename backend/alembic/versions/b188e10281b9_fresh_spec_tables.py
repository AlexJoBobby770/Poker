"""fresh_spec_tables

Revision ID: b188e10281b9
Revises: 
Create Date: 2026-06-25 21:14:32.756886

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b188e10281b9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'game_sessions',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('num_players', sa.Integer(), nullable=False),
        sa.Column('notes', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'hand_histories',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('session_id', sa.Integer(), sa.ForeignKey('game_sessions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('hand_number', sa.Integer(), nullable=False),
        sa.Column('hole_cards', sa.JSON(), nullable=False),
        sa.Column('community_cards', sa.JSON(), nullable=False),
        sa.Column('pot_size', sa.Float(), nullable=False),
        sa.Column('stack_size', sa.Float(), nullable=False),
        sa.Column('num_active_players', sa.Integer(), nullable=False, default=2),
        sa.Column('calculated_equity', sa.Float(), nullable=False),
        sa.Column('required_equity', sa.Float(), nullable=False),
        sa.Column('expected_value', sa.Float(), nullable=False),
        sa.Column('recommended_action', sa.String(), nullable=False),
        sa.Column('ai_explanation', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'opponent_profiles',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('player_name', sa.String(), nullable=False),
        sa.Column('total_hands_observed', sa.Integer(), nullable=True),
        sa.Column('vpip_count', sa.Integer(), nullable=True),
        sa.Column('pfr_count', sa.Integer(), nullable=True),
        sa.Column('three_bet_count', sa.Integer(), nullable=True),
        sa.Column('agg_actions', sa.Integer(), nullable=True),
        sa.Column('pass_actions', sa.Integer(), nullable=True),
        sa.Column('inferred_style', sa.String(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.UniqueConstraint('player_name', name='uq_opponent_profiles_player_name'),
    )


def downgrade() -> None:
    op.drop_table('opponent_profiles')
    op.drop_table('hand_histories')
    op.drop_table('game_sessions')
