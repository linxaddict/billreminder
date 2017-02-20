"""Add FriendRequest model

Revision ID: 31afcd344252
Revises: 6cf4261a4d79
Create Date: 2017-02-19 19:56:51.917040

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31afcd344252'
down_revision = '6cf4261a4d79'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('friend_requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('from_id', sa.Integer(), nullable=True),
    sa.Column('to_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['from_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['to_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('friend_requests')
    # ### end Alembic commands ###