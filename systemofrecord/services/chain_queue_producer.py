from datatypes import system_of_record_chain_message_validator
from datatypes.core import unicoded

from systemofrecord import configure_logging
from systemofrecord.services import chain_queue


class ChainQueueProducer(object):
    def __init__(self):
        self.logger = configure_logging(self)


    def enqueue_for_object(self, originating_object, chains):
        for chain_name in chains.iterkeys():
            for chain_object in chains[chain_name]:
                message_to_send = self.create_chain_method(chain_name, chain_object, originating_object)

                system_of_record_chain_message_validator.validate(message_to_send)
                self.logger.info("Adding to chain queue: " + repr(message_to_send))
                chain_queue.add_to_queue(message_to_send)
                self.logger.debug("Chain message sent: " + repr(message_to_send))


    def create_chain_method(self, chain_name, chain_object, originating_object):
        return unicoded({
            'message_envelope': {
                'caused_by_blockchain_insert_id': int(
                    originating_object.as_dict()['object']['blockchain_index']),
                'message': {
                    'chain_name': str(chain_name),
                    'message': chain_object.as_dict(),
                }
            }
        })
