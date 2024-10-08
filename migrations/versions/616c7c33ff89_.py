"""empty message

Revision ID: 616c7c33ff89
Revises: 8c7d925f7dbd
Create Date: 2024-07-28 15:05:45.854156

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '616c7c33ff89'
down_revision = '8c7d925f7dbd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('is_active')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False))

    # ### end Alembic commands ###
