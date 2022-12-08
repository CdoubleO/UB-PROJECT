"""create user group table

Revision ID: c9dd06739e31
Revises: e92f288fb6ee
Create Date: 2022-12-08 11:31:52.118330

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9dd06739e31'
down_revision = 'e92f288fb6ee'
branch_labels = None
depends_on = None


def upgrade():
    User_Groups = op.create_table(
        'UserGroups',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('active',sa.Boolean(), server_default='TRUE', nullable=False),
        sa.Column('created_at',sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')        
        )

    op.bulk_insert(
        User_Groups,
        [
            {'title':'Administrator', 'description':'Full Access'},
            {'title':'Guest', 'description':'Limited Access - Read Only'},
            {'title':'Basic User', 'description':'Limited Access - Read all and Write by group'},
        ],
        multiinsert=False
        )
    pass


def downgrade():
    op.drop_table('UserGroups')
    pass