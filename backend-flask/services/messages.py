from datetime import datetime, timedelta, timezone
from lib.ddb import ddb


class Messages:
    """Users Messages Manager"""
    def run(message_group_uuid):
        """returns a list of messages objects based on the
        passed message_group_uuid"""
        model = {
        'errors': None,
        'data': None
        }
        now = datetime.now(timezone.utc).astimezone()
        results = ddb.list_messages(message_group_uuid)
        model['data'] = results
        return model
