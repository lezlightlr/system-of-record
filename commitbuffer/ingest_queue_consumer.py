from time import sleep

from systemofrecord import configure_logging
from systemofrecord.services import ingest_queue
from datatypes.exceptions import DataDoesNotMatchSchemaException
from commitbuffer import blockchain_ingestor


class IngestQueueConsumer(object):
    def __init__(self, queue, queue_key, poll_interval=60):
        self.queue_key = queue_key
        self.queue = queue
        self.sleep_time_in_seconds = poll_interval
        self.logger = configure_logging(self)

    def process_queue(self):
        if not ingest_queue.is_empty():
            self.logger.info("Processing %d messages in queue" % ingest_queue.queue_size())

            while not ingest_queue.is_empty():
                message = ingest_queue.read_from_queue()
                self.logger.debug("Message: %s" % repr(message))

                try:
                    blockchain_ingestor.ingest(message)
                except DataDoesNotMatchSchemaException as e:
                    self.logger.error("Could not process message: %s error: %s" % (repr(message), repr(e)))
        else:
            self.logger.info("Ingest queue is empty.")

    def run(self):
        while True:
            self.process_queue()
            sleep(self.sleep_time_in_seconds)