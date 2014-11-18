from flask import jsonify, abort

from systemofrecord import app

from systemofrecord.repository import blockchain_object_repository


class LoadObjectController(object):
    def load_object(self, object_id):
        loaded_object = blockchain_object_repository.load_most_recent_object_with_id(object_id)

        if loaded_object:
            return jsonify(loaded_object.as_dict())

        app.logger.info("Could not find object with ID: %s" % object_id)
        return abort(404)