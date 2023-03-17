"""add timestamps Project(start_date&end_date)

Revision ID: ee6116165ff4
Revises: ffdbdd74085a
Create Date: 2023-03-14 20:01:02.030083

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee6116165ff4'
down_revision = 'ffdbdd74085a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'Projects',
        sa.Column('start_date', sa.TIMESTAMP(timezone=False), nullable=True)
        )
    op.add_column(
        'Projects',
        sa.Column('finish_date', sa.TIMESTAMP(timezone=False), nullable=True)
        )

    t_project = sa.Table(
        'Projects',
        sa.MetaData(),
        sa.Column('id', sa.Integer()),
        sa.Column('title', sa.String()),
        sa.Column('description', sa.String()),
        sa.Column('active', sa.Boolean()),
        sa.Column('created_at', sa.TIMESTAMP()),
        sa.Column('created_by_user_id', sa.Integer()),
        sa.Column('start_date', sa.TIMESTAMP()), #new column
        sa.Column('finish_date', sa.TIMESTAMP())  #new column
    )    
    connection = op.get_bind()
    connection.execute(
        t_project.update().where(t_project.c.start_date == None,).values({ "start_date": "1900-01-01 00:00:00.001 -0300" })
    )
    connection.execute(
        t_project.update().where(t_project.c.finish_date == None,).values({ "finish_date": "1900-01-01 00:00:00.001 -0300" })
    )
    pass


def downgrade():
    op.drop_column('Projects','finish_date')
    op.drop_column('Projects','start_date')
    pass
