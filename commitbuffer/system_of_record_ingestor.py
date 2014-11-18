from datatypes import system_of_record_request_validator

from systemofrecord import configure_logging
from systemofrecord.repository import blockchain_object_repository, chain_repo
from systemofrecord.services import chain_queue_producer


class SystemOfRecordIngestor(object):
    def __init__(self):
        self.logger = configure_logging(self)

    def ingest(self, message):
        self.logger.debug("Beginning blockchain append for: [%s]" % str(message))

        if message is not None:
            system_of_record_request_validator.validate(message)
            object_id = message['object']['object_id']
            self.logger.debug("Beginning blockchain append for: [%s]" % object_id)

            loaded_object_from_head_of_blockchain = self.store_in_database(object_id, message)

            if loaded_object_from_head_of_blockchain:
                self.send_chain_messages(loaded_object_from_head_of_blockchain, object_id)
            else:
                self.logger.error(
                    "Could not find object with ID [%s] so can't send message [%s]" % (object_id, repr(message)))

            self.logger.info("Finished blockchain append for object [%s]" % object_id)
        else:
            self.logger.warn("Attempted to ingest null message")


    def store_in_database(self, object_id, message):
        blockchain_object_repository.store_object(object_id, message)
        return blockchain_object_repository.load_most_recent_object_with_id(object_id)


    def send_chain_messages(self, blockchain_object, object_id):
        if len(blockchain_object.chains) > 0:
            chains_to_send = chain_repo.load_chain_heads_for_object(blockchain_object)

            if chains_to_send:
                chain_names = ', '.join(k for k in chains_to_send.iterkeys())
                self.logger.info("Sending message for chains [%s] from object [%s]" % (chain_names, object_id))
                chain_queue_producer.enqueue_for_object(blockchain_object, chains_to_send)
