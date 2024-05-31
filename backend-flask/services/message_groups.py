from datetime import datetime, timedelta, timezone
from lib.ddb import ddb
from lib.db import db


class MessageGroups:
    """Message Groups Manager"""
    def run(cognito_user_id: str):
        """returns a list of message groups objects"""
        model = {
        'errors': None,
        'data': None
        }
        now = datetime.now(timezone.utc).astimezone()
        # Extracting user's uuid
        query_user = db.sql_template('users', 'user_by_cognito_id')
        user_uuid = db.query_wrap_object_json(query_user, cognito_user_id)['uuid']

        # Extracting the list of message groups of the user
        results = ddb.list_message_groups(user_uuid)
        model['data'] = results
        return model
