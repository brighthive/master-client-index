"""empty message

Revision ID: 3187a44ef222
Revises: 7da08ea50a5a
Create Date: 2019-05-13 17:54:53.264249

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3187a44ef222'
down_revision = '7da08ea50a5a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('individual', sa.Column(
        'suffix', sa.String(length=10), nullable=True))


def downgrade():
    op.drop_column('individual', 'suffix')
