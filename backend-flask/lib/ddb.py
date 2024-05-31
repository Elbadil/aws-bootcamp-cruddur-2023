import boto3


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
            'ScanIndexForward': True,
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
            'ScanIndexForward': True,
            'ExpressionAttributeValues': {
                ':pk': {'S': f'MSG-{message_group_uuid}'}
            },
            'ReturnConsumedCapacity': 'TOTAL'
        }
        response = self.client.query(**query_params)
        items = response['Items']
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


ddb = DDB()
