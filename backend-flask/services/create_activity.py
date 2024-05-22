from datetime import datetime, timedelta, timezone
from lib.db import db


class CreateActivity:
    """Create Activity Manager"""
    def create_activity(handle, message, expires_at):
        """Creates and inserts activity data in the db
        and returns the activity's uuid"""
        query = db.sql_template('activities', 'create')
        try:
            activity_uuid = db.execute_query_return_uuid(query, handle, message, expires_at)
            return activity_uuid
        except Exception as e:
            print(e)
            return "failed"

    def run(user_handle, message, ttl):
        """Runs the create_activity method and
        returns activity's data as an object"""
        model = {
            'errors': None,
            'data': None
        }

        now = datetime.now(timezone.utc).astimezone()
        period = None

        if ttl is None:
            model['errors'] = ['ttl_blank']
        elif 'day' in ttl:
            period = ttl.split('-')[0]
            ttl_offset = timedelta(days=int(period))
        elif 'hour' in ttl:
            period = ttl.split('-')[0]
            ttl_offset = timedelta(hours=int(period))

        if user_handle == None or len(user_handle) < 1:
            model['errors'] = ['user_handle_blank']

        if message == None or len(message) < 1:
            model['errors'] = ['message_blank'] 
        elif len(message) > 280:
            model['errors'] = ['message_exceed_max_chars'] 

        if model['errors']:
            model['data'] = {
                'handle': user_handle,
                'message': message
            }
        else:
            expires_at = (now + ttl_offset)
            activity_uuid = CreateActivity.create_activity(user_handle, message, expires_at)
            activity_query = db.sql_template('activities', 'object')
            activity_data = db.query_wrap_object_json(activity_query, activity_uuid)
            model['data'] = activity_data
        return model
