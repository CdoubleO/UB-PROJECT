"""add foreign key to projects table from state table

Revision ID: e92f288fb6ee
Revises: 7947a7facf87
Create Date: 2022-12-06 01:26:13.810558

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e92f288fb6ee'
down_revision = '7947a7facf87'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'Projects', 
        sa.Column('state_id', sa.Integer(), nullable=False),
        )
    op.create_foreign_key(
        'project_states_fk',
        source_table='Projects', 
        referent_table='ProjectStates',
        local_cols=['state_id'],
        remote_cols=['id'],
        ondelete="CASCADE"
        )
    pass


def downgrade():
    op.drop_constraint('project_states_fk', table_name='Projects')
    op.drop_column('Projects','state_id')
    pass