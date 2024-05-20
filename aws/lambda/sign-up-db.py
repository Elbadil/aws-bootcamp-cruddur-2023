import json
import psycopg2
import os


def lambda_handler(event, context):
    """Inserts user's data in our cruddur db after sign up"""
    print("Event data", event)
    user = event['request']['userAttributes']
    print('User Attributes:', user)
    try:
        conn = psycopg2.connect(os.getenv('DB_CONNECTION_URL'))
        cur = conn.cursor()
        query = f"""
            INSERT INTO users
                (display_name,
                handle,
                email,
                cognito_user_id)
            VALUES(
                '{user['name']}',
                '{user['preferred_username']}',
                '{user['email']}',
                '{user['sub']}')
            """
        cur.execute(query)
        conn.commit() 

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            cur.close()
            conn.close()
            print('Database connection closed.')

    return event



def lambda_handler(event, context):
    """Inserts user's data in our cruddur db after sign up"""
    print("Event data:", event)
    user = event['request']['userAttributes']
    print('User Attributes:', user)

    conn = None
    try:
        # Check if environment variable is set
        db_url = os.getenv('AWS_DB_CONNECTION_URL')
        if not db_url:
            raise ValueError("DB connection URL not set")

        print("Connecting to the database...")
        conn = psycopg2.connect(db_url)
        print("Connected to the database.")

        cur = conn.cursor()

        # Use parameterized query to prevent SQL injection
        query = """
            INSERT INTO users (display_name, handle, email, cognito_user_id)
            VALUES (%s, %s, %s, %s)
            """
        values = (user['name'], user['preferred_username'], user['email'], user['sub'])
        
        print("Executing query...")
        cur.execute(query, values)
        conn.commit()
        print("Data inserted successfully.")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Database error:", error)

    finally:
        if conn is not None:
            cur.close()
            conn.close()
            print('Database connection closed.')

    return event