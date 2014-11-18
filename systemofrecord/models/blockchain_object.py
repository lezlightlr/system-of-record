from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Sequence, String

from systemofrecord.models import Chain
from systemofrecord.repository.message_id_validator import check_object_id_matches_id_in_message

from systemofrecord.services.compression_service import decompress, compress
from systemofrecord import db

import json


class BlockchainObject(db.Model):
    __tablename__ = 'blockchain'

    id = Column(Integer, Sequence('object_id_seq'), primary_key=True)
    object_id = Column(String)
    creation_timestamp = Column(Integer)
    data = Column('data', BYTEA)
    blockchain_index = Column(Integer, Sequence('blockchain_index_seq'))
    chains = relationship('Chain')

    @staticmethod
    def create(object_id, message):
        check_object_id_matches_id_in_message(message, object_id)

        def link_chains():
            try:
                return map(lambda x: Chain.create(x['chain_name'], x['chain_value']), message['object']['chains'])
            except KeyError:
                return []

        return BlockchainObject(
            object_id=object_id,
            creation_timestamp=1,  ## TODO
            data=compress(json.dumps(message)),
            chains=link_chains()
        )

    def __repr__(self):
        return repr(self.as_dict())

    def has_chains(self):
        return len(self.chains) > 0

    def as_dict(self):
        obj = json.loads(decompress(self.data))
        info = obj['object']
        assert info

        info['db_id'] = self.id
        info['creation_timestamp'] = self.creation_timestamp
        info['blockchain_index'] = self.blockchain_index
        obj['chains'] = map(lambda x: x.as_dict(), self.chains)

        return obj

