from datatypes import system_of_record_request_validator
from systemofrecord.services import ingest_queue
from systemofrecord import configure_logging

class IngestQueueProducer(object):
    def __init__(self):
        self.logger = configure_logging(self)

    def enqueue(self, message):
        try:
            system_of_record_request_validator.validate(message)
            ingest_queue.add_to_queue(system_of_record_request_validator.to_canonical_form(message))
        except Exception as e:
            self.logger.error("Could not enqueue message: [message: %s] [exception: %s]" % (message, e))
            # TODO: Store failures somewhere. Possible data loss!
            raise e



