"""Add a column

Revision ID: 55394037a1ed
Revises: 
Create Date: 2021-09-09 19:03:56.313896

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55394037a1ed'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('studentinfo', sa.Column('alembic_update', sa.String))


def downgrade():
    op.drop_column('studentinfo', 'alembic_update')
