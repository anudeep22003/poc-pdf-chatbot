"""add conversation table

Revision ID: f00bf1e69285
Revises: 635c37ce64dc
Create Date: 2023-08-14 20:34:55.772209

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f00bf1e69285'
down_revision = '635c37ce64dc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('conversation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('domain', sa.Text(), nullable=True),
    sa.Column('ts_created', sa.DateTime(timezone=True), server_default=sa.text("(STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW'))"), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('conversation')
    # ### end Alembic commands ###