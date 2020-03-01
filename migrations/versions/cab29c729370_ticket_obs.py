"""Ticket obs

Revision ID: cab29c729370
Revises: cba9113bc61c
Create Date: 2020-02-25 05:45:26.672984

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'cab29c729370'
down_revision = 'cba9113bc61c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ticket', sa.Column('obs', sa.Text(), nullable=True))
    op.alter_column('ticket_file', 'data',
               existing_type=mysql.LONGBLOB(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('ticket_file', 'data',
               existing_type=mysql.LONGBLOB(),
               nullable=False)
    op.drop_column('ticket', 'obs')
    # ### end Alembic commands ###