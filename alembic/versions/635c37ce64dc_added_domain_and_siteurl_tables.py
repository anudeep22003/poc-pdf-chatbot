"""added domain and siteurl tables

Revision ID: 635c37ce64dc
Revises: 
Create Date: 2023-08-11 13:27:33.186053

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '635c37ce64dc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('domain',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('domain', sa.String(), nullable=False),
    sa.Column('pagerank', sa.PickleType(), nullable=True),
    sa.Column('textrank', sa.PickleType(), nullable=True),
    sa.Column('sitemap', sa.Text(), nullable=True),
    sa.Column('ts_created', sa.DateTime(timezone=True), server_default=sa.text("(STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW'))"), nullable=False),
    sa.Column('ts_updated', sa.DateTime(timezone=True), server_default=sa.text("(STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW'))"), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_domain_domain'), 'domain', ['domain'], unique=True)
    op.create_index(op.f('ix_domain_id'), 'domain', ['id'], unique=False)
    op.create_table('message',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('conv_id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('sender', sa.String(), nullable=False),
    sa.Column('receiver', sa.String(), nullable=False),
    sa.Column('sources', sa.String(), nullable=True),
    sa.Column('ts_created', sa.DateTime(timezone=True), server_default=sa.text("(STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW'))"), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('siteurl',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('domain', sa.String(), nullable=False),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('html', sa.Text(), nullable=True),
    sa.Column('ts_created', sa.DateTime(timezone=True), server_default=sa.text("(STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW'))"), nullable=False),
    sa.Column('ts_updated', sa.DateTime(timezone=True), server_default=sa.text("(STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW'))"), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_siteurl_id'), 'siteurl', ['id'], unique=False)
    op.create_index(op.f('ix_siteurl_url'), 'siteurl', ['url'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_siteurl_url'), table_name='siteurl')
    op.drop_index(op.f('ix_siteurl_id'), table_name='siteurl')
    op.drop_table('siteurl')
    op.drop_table('message')
    op.drop_index(op.f('ix_domain_id'), table_name='domain')
    op.drop_index(op.f('ix_domain_domain'), table_name='domain')
    op.drop_table('domain')
    # ### end Alembic commands ###
