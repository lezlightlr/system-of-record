from systemofrecord import app
from systemofrecord.services import ingest_queue
from commitbuffer.system_of_record_ingestor import SystemOfRecordIngestor

blockchain_ingestor = SystemOfRecordIngestor()

from commitbuffer.ingest_queue_consumer import IngestQueueConsumer

ingest_queue_consumer = IngestQueueConsumer(
    queue_key=app.config.get('INGEST_QUEUE_NAME'),
    queue=ingest_queue)