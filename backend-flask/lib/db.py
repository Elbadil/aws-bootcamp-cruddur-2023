from psycopg_pool import ConnectionPool
import os


def query_wrap_object(template):
    """Serializes an object into a json"""
    query = f'''
    (SELECT COALESCE(row_to_json(object_row),'[]'::json) FROM (
    {template}
    ) object_row);
    '''
    return query


def query_wrap_array(template):
    """Adds Json specifications to return the
    query results in JSON Format"""
    query = f'''
    (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json)
    FROM (
        {template}
    ) array_row);
    '''
    return query


connection_url = os.getenv('DB_CONNECTION_URL')
pool = ConnectionPool(connection_url)
