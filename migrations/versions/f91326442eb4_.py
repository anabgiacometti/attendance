"""empty message

Revision ID: f91326442eb4
Revises: d8efb5112e1b
Create Date: 2020-04-18 03:49:32.623760

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f91326442eb4'
down_revision = 'd8efb5112e1b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('client', sa.Column('resale', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('client', 'resale')
    # ### end Alembic commands ###
