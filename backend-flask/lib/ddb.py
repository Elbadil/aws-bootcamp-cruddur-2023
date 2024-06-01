import boto3
import botocore
import uuid
from datetime import datetime, timezone

class DDB():
    """DynamoDB Tables Manager"""
    def __init__(self):
        self.client = boto3.client('dynamodb', endpoint_url="http://localhost:8000")
    
    def list_message_groups(self, user_uuid):
        """Returns a list of message groups object of a user"""
        query_params = {
            'TableName': 'cruddur_messages',
            'Limit': 10,
            'KeyConditionExpression': 'pk = :pk',
            'ScanIndexForward': False,
            'ExpressionAttributeValues': {
                ':pk': {'S': f'GRP-{user_uuid}'}
            },
            'ReturnConsumedCapacity': 'TOTAL'
        }
        response = self.client.query(**query_params)
        items = response['Items']
        message_groups = []
        for item in items:
            message_groups.append(
                {
                    'uuid': item['message_group_uuid']['S'],
                    'other_user_display_name': item['user_display_name']['S'],
                    'other_user_handle': item['user_handle']['S'],
                    'last_message': item['message']['S'],
                    'last_message_at': item['sk']['S']
                }
            )
        return message_groups

    def list_messages(self, message_group_uuid):
        """Returns a list of messages object of a conversation"""
        query_params = {
            'TableName': 'cruddur_messages',
            'Limit': 10,
            'KeyConditionExpression': 'pk = :pk',
            'ScanIndexForward': False,
            'ExpressionAttributeValues': {
                ':pk': {'S': f'MSG-{message_group_uuid}'}
            },
            'ReturnConsumedCapacity': 'TOTAL'
        }
        response = self.client.query(**query_params)
        items = response['Items'][::-1]
        # print(f'Items: {items}')
        messages = []
        for item in items:
            messages.append(
                {
                    'uuid': item['message_uuid']['S'],
                    'user_display_name': item['user_display_name']['S'],
                    'user_handle': item['user_handle']['S'],
                    'message': item['message']['S'],
                    'created_at': item['sk']['S']
                }
            )
        return messages

    def create_message(self, message_group_uuid, message, user_uuid, user_display_name, user_handle):
        """"""
        created_at = datetime.now(timezone.utc).astimezone().isoformat()
        message_uuid = str(uuid.uuid4())
        record = {
            'pk': {'S': f'MSG-{message_group_uuid}'},
            'sk': {'S': created_at},
            'message_group_uuid': {'S': message_group_uuid},
            'message_uuid': {'S': message_uuid},
            'message': {'S': message},
            'user_uuid': {'S': user_uuid},
            'user_handle': {'S': user_handle},
            'user_display_name': {'S': user_display_name},
        }

        response = self.client.put_item(
            TableName='cruddur_messages',
            Item=record 
        )

        created_message = {
            # 'message_group_uuid': message_group_uuid,
            'uuid': message_uuid,
            'user_display_name': user_display_name,
            'user_handle': user_handle,
            'message': message,
            'created_at': created_at
        }

        return created_message

    def create_message_group(self, 
                             user_uuid,
                             user_handle,
                             user_display_name,
                             other_user_uuid,
                             other_user_handle,
                             other_user_display_name,
                             last_message):
        """"""
        table_name = 'cruddur_messages'
        message_group_uuid = str(uuid.uuid4())
        message_uuid = str(uuid.uuid4())
        last_message_at = datetime.now(timezone.utc).astimezone().isoformat()
        # Defining request user's message group attributes
        user_message_group = {
            'pk': {'S': f'GRP-{user_uuid}'},
            'sk': {'S': last_message_at},
            'message_group_uuid': {'S': message_group_uuid},
            'user_uuid': {'S': other_user_uuid},
            'user_display_name': {'S': other_user_display_name},
            'user_handle': {'S': other_user_handle},
            'message': {'S': last_message},
        }
        # Defining other user's(receiver user) message group attributes
        other_user_message_group = {
            'pk': {'S': f'GRP-{other_user_uuid}'},
            'sk': {'S': last_message_at},
            'message_group_uuid': {'S': message_group_uuid},
            'user_uuid': {'S': user_uuid},
            'user_display_name': {'S': user_display_name},
            'user_handle': {'S': user_handle},
            'message': {'S': last_message},
        }
        # Defining user's message attributes
        user_message = {
            'pk': {'S': f'MSG-{message_group_uuid}'},
            'sk': {'S': last_message_at},
            'message_group_uuid': {'S': message_group_uuid},
            'message_uuid': {'S': message_uuid},
            'message': {'S': last_message},
            'user_uuid': {'S': user_uuid},
            'user_handle': {'S': user_handle},
            'user_display_name': {'S': user_display_name},
        }
        # Storing all these records objects in an items dictionary
        items = {
            table_name: [
                {'PutRequest': {'Item': user_message_group}},
                {'PutRequest': {'Item': other_user_message_group}},
                {'PutRequest': {'Item': user_message}},
            ]
        }

        try:
            print('== create_message_group.try')
            # Begin the transaction
            response = self.client.batch_write_item(RequestItems=items)
            return {
                'message_group_uuid': message_group_uuid
            }
        except botocore.exceptions.ClientError as e:
            print('== create_message_group.error')
            print(e)


ddb = DDB()
