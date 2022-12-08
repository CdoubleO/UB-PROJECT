"""create projects table

Revision ID: 00bd302bc107
Revises: 
Create Date: 2022-12-05 23:11:00.653309

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00bd302bc107'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'Projects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('active', sa.String(), nullable=False, server_default='TRUE'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False,server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
        )
    pass

def downgrade():
    op.drop_table('Projects')
    pass
