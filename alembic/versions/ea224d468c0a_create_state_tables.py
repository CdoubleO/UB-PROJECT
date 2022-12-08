"""create state tables

Revision ID: ea224d468c0a
Revises: ae70658fadcc
Create Date: 2022-12-06 00:33:26.300755

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea224d468c0a'
down_revision = 'ae70658fadcc'
branch_labels = None
depends_on = None


def upgrade():
    task_states = op.create_table(
        'TaskStates',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('active',sa.Boolean(), server_default='TRUE', nullable=False),
        sa.PrimaryKeyConstraint('id')
        )
    project_states = op.create_table(
        'ProjectStates',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('active',sa.Boolean(), server_default='TRUE', nullable=False),
        sa.PrimaryKeyConstraint('id')        
        )

    op.bulk_insert(
        task_states,
        [
            {'description':'Pendiente'},
            {'description':'En progreso'},
            {'description':'Revisar'},
            {'description':'Reveer'},
            {'description':'Completado Correctamente'},
            {'description':'Retrasado'},
            {'description':'Omitido'},
            {'description':'Cancelado'}
        ],
        multiinsert=False
        )
    op.bulk_insert(
        project_states,
        [
            {'description':'No Iniciado'},
            {'description':'En progreso'},
            {'description':'Testeo'},
            {'description':'Completado Correctamente'},
            {'description':'Retrasado'},
            {'description':'Cancelado'}
        ],
        multiinsert=False
        )
    pass


def downgrade():
    op.drop_table('TaskStates')
    op.drop_table('ProjectStates')
    pass
