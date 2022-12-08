"""create tasks table

Revision ID: 7947a7facf87
Revises: ea224d468c0a
Create Date: 2022-12-06 01:03:57.079203

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7947a7facf87'
down_revision = 'ea224d468c0a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'Tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('active', sa.Boolean(), server_default='TRUE', nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_by_user_id', sa.Integer(), nullable=False),  
        sa.Column('state_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_foreign_key(
        'task_users_fk',
        source_table='Tasks', 
        referent_table='Users',
        local_cols=['created_by_user_id'],
        remote_cols=['id'],
        ondelete="CASCADE"
    )
    op.create_foreign_key(
        'task_projects_fk',
        source_table='Tasks', 
        referent_table='Projects',
        local_cols=['project_id'],
        remote_cols=['id'],
        ondelete="CASCADE"
    )
    op.create_foreign_key(
        'task_states_fk',
        source_table='Tasks', 
        referent_table='TaskStates',
        local_cols=['state_id'],
        remote_cols=['id'],
        ondelete="CASCADE"
    )
    pass


def downgrade():
    op.drop_constraint('task_states_fk', table_name='Tasks')
    op.drop_constraint('task_projects_fk', table_name='Tasks')
    op.drop_constraint('task_users_fk', table_name='Tasks')
    op.drop_table('Tasks')
    pass