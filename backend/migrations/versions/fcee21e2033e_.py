"""empty message

Revision ID: fcee21e2033e
Revises: 860867bc6a85
Create Date: 2022-12-19 14:08:51.102710

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fcee21e2033e'
down_revision = '860867bc6a85'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('performance',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('actor_id', sa.Integer(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['actor_id'], ['actors.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], ondelete='CASCADE' ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('actors', schema=None) as batch_op:
        batch_op.alter_column('age',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('gender',
               existing_type=sa.VARCHAR(),
               nullable=False)

    with op.batch_alter_table('movies', schema=None) as batch_op:
        batch_op.add_column(sa.Column('release_date', sa.DateTime(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('movies', schema=None) as batch_op:
        batch_op.drop_column('release_date')

    with op.batch_alter_table('actors', schema=None) as batch_op:
        batch_op.alter_column('gender',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('age',
               existing_type=sa.INTEGER(),
               nullable=True)

    op.drop_table('performance')
    # ### end Alembic commands ###
