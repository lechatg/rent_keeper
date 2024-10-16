"""Add user_id to operation table

Revision ID: 492c4743c8bd
Revises: 56387a052c69
Create Date: 2024-09-26 15:08:39.130229

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '492c4743c8bd'
down_revision: Union[str, None] = '56387a052c69'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('operation', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'operation', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'operation', type_='foreignkey')
    op.drop_column('operation', 'user_id')
    # ### end Alembic commands ###
