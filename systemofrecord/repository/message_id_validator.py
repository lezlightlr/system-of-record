class InvalidTitleIdException(Exception):
    pass


def check_object_id_matches_id_in_message(data, object_id):
    try:
        object_id_in_message = data['object']['object_id']
        if object_id != object_id_in_message:
            raise InvalidTitleIdException(
                "Claimed object ID not equal to ID in message, %s : %s" % (object_id, object_id_in_message))
    except KeyError:
        raise InvalidTitleIdException("Object not found in message")