from datetime import datetime, timedelta, timezone


class CreateActivity:
    """Create Activity Manager"""
    def create_activity(cognito_user_id, message, expires_at):
        """Creates and inserts activity data in the db
        and returns the activity's uuid"""
        from lib.db import db

        query = db.sql_template('activities', 'create')
        try:
            activity_uuid = db.execute_query_return_uuid(query,
                                                         cognito_user_id=cognito_user_id,
                                                         message=message,
                                                         expires_at=expires_at)
            return activity_uuid
        except Exception as e:
            print(e)
            return "failed"

    def run(cognito_user_id, message, ttl):
        """Runs the create_activity method and
        returns activity's data as an object"""
        from lib.db import db

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

        if cognito_user_id == None or len(cognito_user_id) < 1:
            model['errors'] = ['cognito_user_id_blank']

        if message == None or len(message) < 1:
            model['errors'] = ['message_blank'] 
        elif len(message) > 280:
            model['errors'] = ['message_exceed_max_chars'] 

        if model['errors']:
            model['data'] = {
                'cognito_user_id': cognito_user_id,
                'message': message
            }
        else:
            expires_at = (now + ttl_offset)
            activity_uuid = CreateActivity.create_activity(cognito_user_id, message, expires_at)
            activity_query = db.sql_template('activities', 'object')
            activity_data = db.query_wrap_object_json(activity_query, activity_uuid)
            model['data'] = activity_data
        return model
