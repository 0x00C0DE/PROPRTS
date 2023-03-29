import json
from src.aws import init

def lambda_handler(event, context):
    init()

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from IRV LOCAL')
    }
