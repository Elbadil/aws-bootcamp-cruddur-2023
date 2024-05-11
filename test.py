import os
from dotenv import load_dotenv

load_dotenv()

user_pool_id = os.getenv('AWS_USER_POOLS_ID')
print(user_pool_id)
