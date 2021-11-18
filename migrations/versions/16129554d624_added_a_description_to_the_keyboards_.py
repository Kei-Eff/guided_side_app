"""Added a description to the keyboards model

Revision ID: 16129554d624
Revises: 6830e02d17d1
Create Date: 2021-11-18 11:59:24.232516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16129554d624'
down_revision = '6830e02d17d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('keyboards', sa.Column('description', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('keyboards', 'description')
    # ### end Alembic commands ###
