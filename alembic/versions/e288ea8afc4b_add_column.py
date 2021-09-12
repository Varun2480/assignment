"""add_column

Revision ID: e288ea8afc4b
Revises: 
Create Date: 2021-09-12 12:43:15.035471

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e288ea8afc4b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('studentinfo', sa.Column('alembic_update', sa.String(20)))


def downgrade():
    op.drop_column('studentinfo', 'alembic_update')
