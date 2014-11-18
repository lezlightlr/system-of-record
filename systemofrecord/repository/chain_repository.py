from systemofrecord import configure_logging
from systemofrecord.models import Chain
from systemofrecord import db
from systemofrecord.models.blockchain_object import BlockchainObject


class ChainRepository(object):
    def __init__(self):
        self.logger = configure_logging(self)


    def load_chain_heads_for_object(self, object, chain_length_to_return=2):
        chains = object.chains
        result = {}
        blockchain_object = None

        if chains:
            for chain in chains:
                query = db.session.query(BlockchainObject) \
                    .filter(Chain.name == chain.name, Chain.value == chain.value) \
                    .filter(Chain.record_id == BlockchainObject.id) \
                    .order_by(BlockchainObject.blockchain_index.desc()) \
                    .limit(chain_length_to_return)

                for query_result in query:
                    if query_result:
                        blockchain_object = query_result

                    if blockchain_object:
                        if not result.has_key(chain.name):
                            result[chain.name] = []

                        print "*****Loaded [%s] ****** %s " % (chain.name, repr(blockchain_object))

                        result[chain.name].append(blockchain_object)

        return result