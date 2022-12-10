"""add foreign key to Users(usergroups)

Revision ID: ffdbdd74085a
Revises: c9dd06739e31
Create Date: 2022-12-08 11:52:36.313710

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ffdbdd74085a'
down_revision = 'c9dd06739e31'
branch_labels = None
depends_on = None



def upgrade():
    op.add_column(
        'Users', 
        sa.Column('group_id', sa.Integer(), server_default="2", nullable=False),
    )
    t_users = sa.Table(
        'Users',
        sa.MetaData(),
        sa.Column('id', sa.Integer()),
        sa.Column('email', sa.String()),
        sa.Column('password', sa.String()),
        sa.Column('active', sa.Boolean()),
        sa.Column('group_id', sa.Integer()) # New Column
    )
    connection = op.get_bind()
    connection.execute(
        t_users.update().where(t_users.c.id==1).values({ "group_id": 1 })
    )

    op.create_foreign_key(
        'user_group_fk',
        source_table='Users', 
        referent_table='UserGroups',
        local_cols=['group_id'],
        remote_cols=['id'],
        ondelete="CASCADE"
    )
    pass


def downgrade():
    op.drop_constraint('user_group_fk', table_name='Users')
    op.drop_column('Users','group_id')
    pass
