"""Add repeat mode to bills

Revision ID: c2ada7f17350
Revises: 42c61aca41d8
Create Date: 2017-03-12 01:26:53.868131

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2ada7f17350'
down_revision = '42c61aca41d8'
branch_labels = None
depends_on = None

repeat_mode = sa.Enum('minute', 'hour', 'day', 'week', 'month', 'year', name='repeatenum')


def upgrade():
    repeat_mode.create(op.get_bind())
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bills', sa.Column('repeat_mode', repeat_mode, nullable=True))
    op.add_column('bills', sa.Column('repeat_value', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bills', 'repeat_value')
    op.drop_column('bills', 'repeat_mode')
    # ### end Alembic commands ###

    repeat_mode.drop(op.get_bind())