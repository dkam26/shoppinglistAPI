"""empty message

Revision ID: 362626a65949
Revises: 
Create Date: 2017-12-08 18:45:05.075968

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '362626a65949'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Shoppinglists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('shoppinglist_name', sa.String(length=255), nullable=True),
    sa.Column('user', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('shoppinglist_name')
    )
    op.create_table('User',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user', sa.String(length=255), nullable=True),
    sa.Column('Surname', sa.String(length=255), nullable=True),
    sa.Column('Firstname', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('Password', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product', sa.String(length=255), nullable=True),
    sa.Column('Quantity', sa.Integer(), nullable=True),
    sa.Column('AmountSpent', sa.Integer(), nullable=True),
    sa.Column('shoppinglist', sa.String(length=255), nullable=True),
    sa.Column('shoppinglist_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['shoppinglist_id'], ['Shoppinglists.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('product')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Product')
    op.drop_table('User')
    op.drop_table('Shoppinglists')
    # ### end Alembic commands ###
