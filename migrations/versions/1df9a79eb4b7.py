"""

Revision ID: 1df9a79eb4b7
Revises: 1ffade2444f3
Create Date: 2014-09-11 11:56:38.611188

"""


# revision identifiers, used by Alembic.
from sqlalchemy import Integer, String, ForeignKey, Column

revision = '1df9a79eb4b7'
down_revision = '1ffade2444f3'

from alembic import op


def upgrade():
    op.create_table(
        'chain',
        Column('id', Integer(), primary_key=True),
        Column('name', String(), nullable=False),
        Column('value', String(), nullable=False),
        Column('record_id', Integer(), ForeignKey('blockchain.id', ondelete='CASCADE'), nullable=False),
    )

    op.create_unique_constraint('uq_chain_name_and_value', 'chain', ['name', 'value', 'record_id'])


def downgrade():
    op.dropTable('chain')
    op.drop_constraint('uq_chain_name_and_value')
