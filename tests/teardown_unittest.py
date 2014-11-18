from unittest import TestCase

from systemofrecord import server
from systemofrecord.services import ingest_queue, chain_queue
from systemofrecord.models import BlockchainObject, Chain


class TeardownUnittest(TestCase):
    def consume_queues(self):
        while not ingest_queue.is_empty():
            ingest_queue.read_from_queue()

        while not chain_queue.is_empty():
            chain_queue.read_from_queue()

    def setUp(self):
        super(TeardownUnittest, self).setUp()
        self.app = server.app.test_client()
        self.consume_queues()
        Chain.query.delete()
        BlockchainObject.query.delete()

    def tearDown(self):
        super(TeardownUnittest, self).tearDown()
        Chain.query.delete()
        BlockchainObject.query.delete()
        self.consume_queues()
