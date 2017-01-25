"""empty message

Revision ID: d0caa631c733
Revises: 912b1182a6c2
Create Date: 2017-01-26 00:37:21.732713

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0caa631c733'
down_revision = '912b1182a6c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('auth_token', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'auth_token')
    # ### end Alembic commands ###
