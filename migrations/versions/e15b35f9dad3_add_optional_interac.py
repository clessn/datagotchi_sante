"""add optional interac

Revision ID: e15b35f9dad3
Revises: b9c9660bee03
Create Date: 2024-09-03 17:51:19.217336

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e15b35f9dad3'
down_revision = 'b9c9660bee03'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('interac',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
        batch_op.alter_column('condition_id',
               existing_type=sa.VARCHAR(length=64),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('condition_id',
               existing_type=sa.VARCHAR(length=64),
               nullable=False)
        batch_op.alter_column('interac',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)

    # ### end Alembic commands ###
