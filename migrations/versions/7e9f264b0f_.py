"""empty message

Revision ID: 7e9f264b0f
Revises: 2e59d536f50
Create Date: 2015-11-15 20:39:35.284700

"""

# revision identifiers, used by Alembic.
revision = '7e9f264b0f'
down_revision = '2e59d536f50'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    ### end Alembic commands ###
