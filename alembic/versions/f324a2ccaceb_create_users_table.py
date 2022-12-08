"""create users table

Revision ID: f324a2ccaceb
Revises: 00bd302bc107
Create Date: 2022-12-05 23:33:07.185321

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f324a2ccaceb'
down_revision = '00bd302bc107'
branch_labels = None
depends_on = None


def upgrade():
    users = op.create_table(
        'Users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('active', sa.Boolean(), server_default='TRUE', nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
        )
    op.bulk_insert(
        users,
        [
            {
                "email": "admin@admin.com", 
                "password": "$2b$12$.kVwKcH50GM73vGOolxnaOd5MmY/r/DyxziKvwsuYmEV81Y2JBoeK"
            }
        ]
        )
    pass


def downgrade():
    op.drop_table('Users')
    pass
