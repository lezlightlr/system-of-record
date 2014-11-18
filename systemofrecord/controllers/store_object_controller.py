from flask import make_response

from systemofrecord.services import ingest_queue_producer
from datatypes import system_of_record_request_validator
from systemofrecord import configure_logging


class StoreObjectController(object):
    def __init__(self):
        self.logger = configure_logging(self)

    def store_object(self, object_id, message):
        system_of_record_request_validator.validate(message)

        if object_id != message['object']['object_id']:
            raise Exception("Object ID does not match message ID")

        ingest_queue_producer.enqueue(message)
        return make_response('OK', 201)