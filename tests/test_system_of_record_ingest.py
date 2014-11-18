from datatypes.exceptions import DataDoesNotMatchSchemaException

from commitbuffer import blockchain_ingestor
from systemofrecord.services import chain_queue
from system_of_record_message_fixtures import *
from tests.teardown_unittest import TeardownUnittest
from systemofrecord.repository import blockchain_object_repository

test_object_id = invalid_message_without_chains['object']['object_id']


class SystemOfRecordIngestTestCase(TeardownUnittest):
    def cannot_ingest_well_formed_record_without_chains(self):
        self.check_system_is_empty()

        self.assertRaises(DataDoesNotMatchSchemaException, blockchain_ingestor.ingest, invalid_message_without_chains)

    def test_can_ingest_well_formed_message_with_tags(self):
        self.check_system_is_empty()

        # Ingest a message with 2 tags.
        blockchain_ingestor.ingest(valid_system_of_record_input_message_with_two_tags)

        # However, as the system was empty we're not expecting any tag messages, only the feeder queue message
        self.check_system_contains_a_number_of_messages(1)
        self.check_chain_queue_contains_a_number_of_messages(2)
        loaded_object = blockchain_object_repository.load_most_recent_object_with_id(test_object_id)


        # Check the loaded object looks like the one that we ingested
        loaded_data = loaded_object.as_dict()
        self.assertEquals(loaded_data['object']['data'],
                          valid_system_of_record_input_message_with_two_tags['object']['data'])

        self.assertEquals(loaded_data['object']['object_id'],
                          valid_system_of_record_input_message_with_two_tags['object']['object_id'])

        self.assertEqual(len(loaded_object.chains),
                         len(valid_system_of_record_input_message_with_two_tags['object']['chains']))

        # Now we'll add a new message with the same 2 tags
        blockchain_ingestor.ingest(valid_system_of_record_input_message_with_two_tags)

        # Now, we're expecting 2 items on the chain queue & db
        self.check_system_contains_a_number_of_messages(2)
        # 6 messages - the previous 2, and the new 4
        # Why 4? It's 2 chains * 2 results per chain.
        self.check_chain_queue_contains_a_number_of_messages(6)

    def test_cant_ingest_bad_record(self):
        self.check_system_is_empty()

        self.assertRaises(DataDoesNotMatchSchemaException, blockchain_ingestor.ingest,
                          invalid_message_without_object)

        self.assertRaises(DataDoesNotMatchSchemaException, blockchain_ingestor.ingest,
                          invalid_message_without_data)

        self.assertRaises(DataDoesNotMatchSchemaException, blockchain_ingestor.ingest,
                          invalid_message_with_duplicate_tag_value)

        self.assertRaises(DataDoesNotMatchSchemaException, blockchain_ingestor.ingest,
                          another_invalid_message_with_duplicate_tag_value)

        self.check_system_contains_a_number_of_messages(0)


    def test_can_ingest_none(self):
        self.check_system_is_empty()

        blockchain_ingestor.ingest(None)

        self.check_system_is_empty()

    def check_system_is_empty(self):
        self.check_system_contains_a_number_of_messages(0)
        self.check_chain_queue_contains_a_number_of_messages(0)

    def check_chain_queue_contains_a_number_of_messages(self, number_of_messages):
        self.assertEqual(chain_queue.queue_size(), number_of_messages)

    def check_system_contains_a_number_of_messages(self, number_of_messages):
        self.assertEqual(blockchain_object_repository.count(), number_of_messages)
