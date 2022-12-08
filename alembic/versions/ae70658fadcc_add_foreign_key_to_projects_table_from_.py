"""add foreign key to projects table from users table

Revision ID: ae70658fadcc
Revises: f324a2ccaceb
Create Date: 2022-12-06 00:15:13.468391

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae70658fadcc'
down_revision = 'f324a2ccaceb'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'Projects', 
        sa.Column('created_by_user_id', sa.Integer(), nullable=False)
        )
    op.create_foreign_key(
        'project_users_fk',
        source_table='Projects', 
        referent_table='Users',
        local_cols=['created_by_user_id'],
        remote_cols=['id'],
        ondelete="CASCADE"
        )
    pass


def downgrade():
    op.drop_constraint('project_users_fk', table_name='Projects')
    op.drop_column('Projects','created_by_user_id')
    pass
