"""Update nullity

Revision ID: 42c61aca41d8
Revises: 80e2fc15678e
Create Date: 2017-03-05 20:43:04.957116

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '42c61aca41d8'
down_revision = '80e2fc15678e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('bills', 'amount',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('bills', 'description',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('bills', 'description',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('bills', 'amount',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    # ### end Alembic commands ###