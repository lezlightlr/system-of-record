from unittest import TestCase

from systemofrecord.services import ingest_queue


class QueueUnittest(TestCase):
    def setUp(self):
        super(QueueUnittest, self).setUp()
        self.consume_queue()

    def tearDown(self):
        super(QueueUnittest, self).tearDown()
        self.consume_queue()

    def consume_queue(self):
        while not ingest_queue.is_empty():
            ingest_queue.read_from_queue()