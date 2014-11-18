import mock

from tests.teardown_unittest import TeardownUnittest
from system_of_record_message_fixtures import valid_system_of_record_input_message_with_two_tags
import json


test_object_id = valid_system_of_record_input_message_with_two_tags['object']['object_id']


class SystemOfRecordTestCase(TeardownUnittest):
    @mock.patch("systemofrecord.services.IngestQueueProducer.enqueue")
    def test_add_title_should_put_to_db_and_queue_data(self, mock_enqueue):
        self.app.put("/titles/%s" % test_object_id,
                     data=(json.dumps(valid_system_of_record_input_message_with_two_tags)),
                     content_type="application/json")

        mock_enqueue.assert_called_with(valid_system_of_record_input_message_with_two_tags)

    @mock.patch("redis.Redis.info")
    def test_health_returns_200(self, mock_redis):
        response = self.app.get('/health')
        self.assertEqual(response.status, '200 OK')

    def test_get_known_title_gets_from_db(self):
        self.app.put("/titles/%s" % test_object_id,
                     data=json.dumps(valid_system_of_record_input_message_with_two_tags),
                     content_type="application/json")

        self.app.get("/titles/%s" % test_object_id)

    def test_get_returns_404_if_title_not_found(self):
        response = self.app.get("/titles/%s" % test_object_id)
        self.assertEqual(response.status_code, 404)
