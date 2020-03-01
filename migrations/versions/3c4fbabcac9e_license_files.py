"""License files

Revision ID: 3c4fbabcac9e
Revises: 0f5361a61b00
Create Date: 2020-02-22 20:22:17.640177

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c4fbabcac9e'
down_revision = '0f5361a61b00'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('license_files',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('data', sa.LargeBinary(), nullable=True),
    sa.Column('license_id', sa.Integer(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['license_id'], ['license.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('license_files')
    # ### end Alembic commands ###