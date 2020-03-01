"""Price Precision

Revision ID: 68405e4c59bb
Revises: 224f58fc39c9
Create Date: 2020-02-20 22:49:56.681017

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '68405e4c59bb'
down_revision = '224f58fc39c9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('service', 'price')
    op.add_column('service', sa.Column('price', sa.Float(precision=2), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('service', 'price')
    op.add_column('service', sa.Column('price', mysql.FLOAT(), nullable=True))
    # ### end Alembic commands ###