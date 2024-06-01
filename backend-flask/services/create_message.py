from lib.db import db
from lib.ddb import ddb


class CreateMessage:
    """Create Message Manager"""
    def run(message, cognito_user_id, message_group_uuid=None, user_receiver_handle=None):
        """Creates message for the user and returns the
        message object"""
        model = {
            'errors': None,
            'data': None
        }

        query_user = db.sql_template('users', 'user_by_cognito_id')
        user = db.query_wrap_object_json(query_user, cognito_user_id)

        if user_receiver_handle:
            other_user_query = db.sql_template('users', 'user_by_handle')
            other_user = db.query_wrap_object_json(other_user_query, user_receiver_handle)
            # Creating two message groups for the request user and the other user
            message_group_uuid = ddb.create_message_group(
                user_uuid=user['uuid'],
                user_handle=user['handle'],
                user_display_name=user['display_name'],
                other_user_uuid=other_user['uuid'],
                other_user_display_name=other_user['display_name'],
                other_user_handle=other_user['handle'],
                last_message=message,                                 
            )
            model['data'] = message_group_uuid
            return model

        if user == None or len(user) < 1:
            model['errors'] = ['user_blank']

        if message_group_uuid == None or len(message_group_uuid) < 1:
            model['errors'] = ['message_group_uuid_blank']

        if message == None or len(message) < 1:
            model['errors'] = ['message_blank']

        elif len(message) > 1024:
            model['errors'] = ['message_exceed_max_chars'] 

        if model['errors']:
            # return what we provided
            model['data'] = {
                'display_name': user['display_name'],
                'handle':  user['handle'],
                'message': message
            }
        else:
            created_message = ddb.create_message(
               message=message,
               message_group_uuid=message_group_uuid,
               user_uuid=user['uuid'],
               user_display_name=user['display_name'],
               user_handle=user['handle']
            )
            model['data'] = created_message
        return model
