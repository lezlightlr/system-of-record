from systemofrecord import app
from systemofrecord.services.queue_provider import RedisQueueProvider

ingest_queue = RedisQueueProvider(app.config.get('INGEST_QUEUE_NAME'))
chain_queue = RedisQueueProvider(app.config.get('CHAIN_QUEUE_NAME'))

from systemofrecord.services.ingest_queue_producer import IngestQueueProducer

ingest_queue_producer = IngestQueueProducer()

from systemofrecord.services.chain_queue_producer import ChainQueueProducer

chain_queue_producer = ChainQueueProducer()




