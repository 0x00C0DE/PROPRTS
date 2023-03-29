import json
import sys
from os import environ

if not environ.get('AWS_LAMBDA_RUNTIME_API'):
    sys.path.insert(0, "./src")
    sys.path.insert(0, "./python/lib/python3.9/site-packages")

from aws.mainFunction import run
from dotenv import load_dotenv


def lambda_handler(event, context):
    run()

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from IRV LOCAL')
    }
if not environ.get('AWS_LAMBDA_RUNTIME_API'):

    load_dotenv()
    lambda_handler(None, None)
