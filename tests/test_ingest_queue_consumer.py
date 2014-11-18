from systemofrecord.services import ingest_queue_producer, ingest_queue
from system_of_record_message_fixtures import valid_system_of_record_input_message_with_two_tags
from tests.queue_unittest import QueueUnittest
from commitbuffer import ingest_queue_consumer


class IngestQueueConsumerTestCase(QueueUnittest):
    def test_can_run_items_through_queue_end_to_end(self):
        # Check the queue is empty
        self.assertEqual(ingest_queue.queue_size(), 0)

        # Place messages on the queue
        ingest_queue_producer.enqueue(valid_system_of_record_input_message_with_two_tags)
        ingest_queue_producer.enqueue(valid_system_of_record_input_message_with_two_tags)

        # Check the queue has something on it
        self.assertEqual(ingest_queue.queue_size(), 2)

        ingest_queue_consumer.process_queue()

        # Check we can process the queue
        self.assertEqual(ingest_queue.queue_size(), 0)