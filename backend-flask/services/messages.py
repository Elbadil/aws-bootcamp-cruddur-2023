from datetime import datetime, timedelta, timezone
from lib.ddb import ddb
# from lib.db import db


class Messages:
    """Users Messages Manager"""
    def run(message_group_uuid, cognito_user_id=None):
        """returns a list of messages objects based on the
        passed message_group_uuid"""
        model = {
            'errors': None,
            'data': None
        }
        now = datetime.now(timezone.utc).astimezone()
        # Extracting user's uuid
        # query_user = db.sql_template('users', 'user_by_cognito_id')
        # user_uuid = db.query_wrap_object_json(query_user, cognito_user_id)['uuid']
        results = ddb.list_messages(message_group_uuid)
        model['data'] = results
        return model
