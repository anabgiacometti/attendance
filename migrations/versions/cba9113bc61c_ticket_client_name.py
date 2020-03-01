"""Ticket client name

Revision ID: cba9113bc61c
Revises: 15e10a5e016a
Create Date: 2020-02-24 18:36:44.926645

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cba9113bc61c'
down_revision = '15e10a5e016a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ticket', sa.Column('contact_name', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ticket', 'contact_name')
    # ### end Alembic commands ###