"""empty message

Revision ID: dd8e86966ba4
Revises: baecc9c49ca6
Create Date: 2021-11-20 09:43:47.695635

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd8e86966ba4'
down_revision = 'baecc9c49ca6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('flasklogin-users', sa.Column('is_admin', sa.Boolean(), server_default='False', nullable=False))
    op.add_column('flasklogin-users', sa.Column('is_superadmin', sa.Boolean(), server_default='False', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('flasklogin-users', 'is_superadmin')
    op.drop_column('flasklogin-users', 'is_admin')
    # ### end Alembic commands ###
