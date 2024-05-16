#!/usr/bin/python3

import os
import psycopg
# from dotenv import load_dotenv

# load_dotenv()

# user_pool_id = os.getenv('AWS_USER_POOLS_ID')
# print(user_pool_id)

connection_url = os.getenv('DB_SG_ID')
print(connection_url)

# with psycopg.connect("host=localhost dbname=cruddur user=postgres password=password") as conn:
#     with conn.cursor() as cur:
#         cur.execute("""
#             SELECT * FROM users;
#             """)
#         records = cur.fetchall()
#         for record in records:
#             print(record)
