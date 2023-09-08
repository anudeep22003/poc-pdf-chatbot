"""added timing values to domain and message tables

Revision ID: 220b79e3bb28
Revises: f00bf1e69285
Create Date: 2023-08-31 13:49:40.286212

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '220b79e3bb28'
down_revision = 'f00bf1e69285'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('domain', sa.Column('time_to_index', sa.Float(), nullable=True))
    op.add_column('message', sa.Column('response_time', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('message', 'response_time')
    op.drop_column('domain', 'time_to_index')
    # ### end Alembic commands ###
