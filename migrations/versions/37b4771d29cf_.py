"""empty message

Revision ID: 37b4771d29cf
Revises: 
Create Date: 2023-03-31 09:28:48.569432

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37b4771d29cf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role', sa.String(length=80), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['employees.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=45), nullable=False))
        batch_op.add_column(sa.Column('meal_used', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('user_type', sa.String(length=20), nullable=True))
        batch_op.create_unique_constraint(None, ['username'])
        batch_op.drop_column('is_admin')
        batch_op.drop_column('name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(length=45), nullable=False))
        batch_op.add_column(sa.Column('is_admin', sa.BOOLEAN(), nullable=True))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('user_type')
        batch_op.drop_column('meal_used')
        batch_op.drop_column('username')

    op.drop_table('admins')
    # ### end Alembic commands ###