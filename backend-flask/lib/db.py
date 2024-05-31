from psycopg_pool import ConnectionPool
import psycopg
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# from flask import current_app as app


class DB:
    """Database Manager"""
    def __init__(self) -> None:
        self.connection_url = os.getenv('DB_CONNECTION_URL')
        self.pool = None
        self._initialize_pool()

    def _initialize_pool(self):
        """initialize a connection pool"""
        try:
            self.pool = ConnectionPool(self.connection_url)
            # print('--Successfully connected to the db--')
        except (Exception, psycopg.DatabaseError) as error:
            print(f"Error connecting to the database: {error}")

    def close(self):
        """Closes a database connection"""
        if self.pool:
            self.pool.close()
            print('---Database connection closed---')

    def execute_query_return_uuid(self, query, *args):
        """performs a query, commits changes to the database
        and returns the object's uuid"""
        query_return_uuid = f'{query} RETURNING uuid;'
        try:
            with self.pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query_return_uuid, args)
                    query_uuid = cur.fetchone()[0]
                    conn.commit()
                    return query_uuid
        except (Exception, psycopg.DatabaseError) as error:
            print(f"Error executing query: {error}")

    def execute_query(self, query, **kwargs):
        """performs a query and commits changes to the database"""
        try:
            with self.pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, kwargs)
                    conn.commit()
        except (Exception, psycopg.DatabaseError) as error:
            print(f"Error executing query: {error}")

    def fetch_all(self, query, params=None):
        """Retrieves data from the database"""
        try:
            with self.pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    results = cur.fetchall()
                    return results
        except (Exception, psycopg.DatabaseError) as error:
            print(f"Error fetching data: {error}")

    def get(self, query, *args):
        """returns a single search value"""
        try:
            with self.pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, args)
                    results = cur.fetchone()
                    return results[0]
        except (Exception, psycopg.DatabaseError) as error:
            print(f"Error fetching single value data: {error}")
    
    @staticmethod
    def sql_template(*file_path):
        """Reads from an sql template and returns the query"""
        from app import app

        # Creating a tuple with all sql file's parent folders
        # And adding the file's path args to the tuple
        pathing = (app.root_path, 'db', 'sql',) + file_path
        # Joining the folders and the file path in the pathing tuple
        file_full_path = os.path.join(*pathing)
        # Adding sql file's extension
        file_full_path += '.sql'
        delimiter = "/" if "/" in file_full_path else "\\"
        display_path = file_full_path.split(delimiter)
        print_with_coloring(f'Loading SQL Template {delimiter.join(display_path[4:])}')
        try:
            with open(file_full_path, "r") as sql_file:
                query = sql_file.read()
                return query
        except Exception as e:
            print(f'Error getting template: {e}')

    def query_wrap_object_json(self, template, *args):
        """Adds Json specifications to return the object
        query results in JSON Format"""
        query_json = f'''
            (SELECT COALESCE(row_to_json(object_row),'[]'::json) FROM (
            {template}
            ) object_row);
        '''
        try:
            with self.pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query_json, args)
                    results = cur.fetchone()
                    # print(results[0])
                    return results[0]
        except (Exception, psycopg.DatabaseError) as error:
            print(f"Error fetching object data: {error}")

    def query_wrap_list_json(self, template, *args):
        """Adds Json specifications to return the list
        query results in JSON Format"""
        query_json = f'''
        (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json)
        FROM (
            {template}
        ) array_row);
        '''
        try:
            with self.pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query_json, args)
                    results = cur.fetchone()
                    # print(results)
                    return results[0]
        except (Exception, psycopg.DatabaseError) as error:
            print(f"Error fetching array data: {error}")


def print_with_coloring(statement):
    """Adding coloring to print statements"""
    BLUE = '\033[94m'
    NDC = '\033[0m'
    print(f'{BLUE}== {statement} =={NDC}')


# Our DB Instance
db = DB()
