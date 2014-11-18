"""empty message

Revision ID: 1ffade2444f3
Revises: None
Create Date: 2014-07-18 12:11:21.405386

"""

from sqlalchemy import Column, Integer, String, LargeBinary, Sequence, Index
from sqlalchemy.sql.ddl import CreateSequence, DropSequence, DropIndex

revision = '1ffade2444f3'
down_revision = None

from alembic import op


def upgrade():
    op.execute(CreateSequence(Sequence('object_id_seq')))
    op.execute(CreateSequence(Sequence('blockchain_index_seq')))

    op.create_table(
        'blockchain',
        Column('id', Integer(), Sequence('object_id_seq'), primary_key=True),
        Column('object_id', String(), nullable=False),
        Column('creation_timestamp', Integer(), nullable=False),
        Column('data', LargeBinary(), nullable=False),
        Column('blockchain_index',
               Integer(), Sequence('blockchain_index_seq'), nullable=False, unique=True),
        Index('idx_blockchain', 'id', 'object_id', 'blockchain_index', 'creation_timestamp', unique=True)
    )


def downgrade():
    op.drop_table('blockchain')
    op.execute(DropSequence('object_id_seq'))
    op.execute(DropSequence('blockchain_index_seq'))
    op.execute(DropIndex('idx_blockchain'))

