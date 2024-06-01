from lib.db import db


class UserShort:
    """"""
    def run(user_handle: str):
        """"""
        model = {
            'errors': None,
            'data': None
        }

        if user_handle == None or len(user_handle) < 1:
            model['errors'] = ['user_black']

        user_query = db.sql_template('users', 'user_by_handle')
        user = db.query_wrap_object_json(user_query, user_handle)
        model['data'] = user
        return model
