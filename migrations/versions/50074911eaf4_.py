"""empty message

Revision ID: 50074911eaf4
Revises: f91326442eb4
Create Date: 2020-04-18 04:11:06.309348

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50074911eaf4'
down_revision = 'f91326442eb4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('license', sa.Column('resale', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('license', 'resale')
    # ### end Alembic commands ###