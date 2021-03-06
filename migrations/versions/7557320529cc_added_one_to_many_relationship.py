"""Added one-to-many relationship

Revision ID: 7557320529cc
Revises: dd8e86966ba4
Create Date: 2021-11-25 10:36:34.585394

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7557320529cc'
down_revision = 'dd8e86966ba4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('keyboards', sa.Column('creator_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'keyboards', 'flasklogin-users', ['creator_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'keyboards', type_='foreignkey')
    op.drop_column('keyboards', 'creator_id')
    # ### end Alembic commands ###
