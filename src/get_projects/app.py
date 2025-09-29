import json
import boto3
import os

#Initiliaze the DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME', 'portfolio-data') # Use an environment variable to store the table name
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    """
    This function scans the DynamoDB table for all project items and returns them as a JSON object.
    """
    try:
        # Scan the DynamoDB table for all project items
        # In a RL, high-traffic app, this would be a query with a Global Secondary Index
        response = table.scan(
            FilterExpression=boto3.dynamodb.conditions.Attr('type').eq('ProjectType')
        )

        items = response.get('Items', [])

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(items)
            }
            # Return the items as a JSON object
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'An error occurred fetching the project data.'})
        }